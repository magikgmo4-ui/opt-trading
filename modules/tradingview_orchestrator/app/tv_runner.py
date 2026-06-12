#!/usr/bin/env python3
"""
TradingView Orchestrator — job runner.
Reads a tv_job_v1 JSON packet, executes via SSH → cursor-ai → tradingview-mcp CLI.

Usage:
  python3 tv_runner.py <job_packet.json>              # read-only (snapshot, alert.list, screenshot)
  python3 tv_runner.py <job_packet.json> --gate-approved   # mutation (alerts, indicators, pine, etc.)
  python3 tv_runner.py <job_packet.json> --dry-run    # show commands without executing

Exit codes: 0=PASS, 1=INVALID_INPUT, 3=REJECTED(no gate), 4=REFUSED(wrong type), 5=RUNNER_ERROR
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parents[3]
REPORTS_DIR = REPO_ROOT / "reports" / "tradingview"
JOBS_DONE   = REPO_ROOT / "modules" / "tradingview_orchestrator" / "jobs" / "done"
JOBS_FAILED = REPO_ROOT / "modules" / "tradingview_orchestrator" / "jobs" / "failed"

SSH_HOST       = "cursor-ai"
TV_MODULE_WIN  = r"C:\Users\ghost\opt-trading\modules\tradingview_observer"
TV_CLI_WIN     = r"C:\Users\ghost\.claude\tools\tradingview-mcp\src\cli\index.js"
EXECUTOR_WIN   = rf"{TV_MODULE_WIN}\app\job_executor.ps1"

READ_ONLY_TYPES = {"snapshot", "alert.list", "screenshot"}
MUTATION_TYPES  = {
    "alert.create", "alert.delete", "alert.rotate_webhook_key",
    "indicator.add", "indicator.remove", "indicator.set",
    "symbol.set", "timeframe.set", "pine.set", "pine.save",
    "layout.switch"
}


def ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def load_env_var(name: str) -> str:
    val = os.environ.get(name, "")
    if not val:
        env_path = REPO_ROOT / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if line.startswith(f"{name}=") and not line.startswith("#"):
                    val = line.split("=", 1)[1].strip().strip('"\'')
                    break
    return val


def ssh_run_ps(ps_command: str, timeout: int = 60) -> tuple[int, str, str]:
    cmd = ["ssh", "-o", "BatchMode=yes", "-o", f"ConnectTimeout={timeout}", SSH_HOST,
           f"powershell -NoProfile -NonInteractive -Command \"{ps_command}\""]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return 5, "", "SSH command timed out"
    except Exception as e:
        return 5, "", str(e)


def ssh_run_ps_file(local_ps1: Path, timeout: int = 90) -> tuple[int, str, str]:
    """SCP a PS1 script to cursor-ai, execute it, return output."""
    remote_tmp = rf"C:\Users\ghost\AppData\Local\Temp\tv_job_{ts()}.ps1"
    scp_cmd = ["scp", "-o", "BatchMode=yes", str(local_ps1),
               f"{SSH_HOST}:{remote_tmp}"]
    try:
        r = subprocess.run(scp_cmd, capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            return 5, "", f"SCP failed: {r.stderr}"
    except Exception as e:
        return 5, "", f"SCP error: {e}"

    rc, out, err = ssh_run_ps(
        f"& '{remote_tmp}'; Remove-Item -Force '{remote_tmp}' -ErrorAction SilentlyContinue",
        timeout=timeout
    )
    return rc, out, err


def build_ps1_for_job(job: dict, creds: dict | None = None) -> str:
    """Generate a PS1 script for the given job packet."""
    jtype  = job["type"]
    params = job.get("params", {})
    cli    = TV_CLI_WIN.replace("\\", "\\\\")

    lines = [
        "$ErrorActionPreference = 'Stop'",
        f"$TV_CLI = '{TV_CLI_WIN}'",
        "function tv { $raw = & node $TV_CLI @args 2>&1 | Out-String; "
        "try { $raw | ConvertFrom-Json } catch { @{success=$false;raw=$raw} } }",
        "",
    ]

    if jtype == "snapshot":
        lines += [
            "$out = @{}",
            "$out.status = tv status",
            "$out.quote  = tv quote",
            "$out.state  = tv state",
            "$out.alerts = tv alert list",
            "$out.values = tv values",
            "$out | ConvertTo-Json -Depth 10",
        ]
    elif jtype == "alert.list":
        lines.append("tv alert list | ConvertTo-Json -Depth 10")
    elif jtype == "alert.create":
        price     = params.get("price", "")
        condition = params.get("condition", "crossing")
        message   = json.dumps(params.get("message", "")).replace('"', '\\"')
        flags = f"-c {condition} -m \\\"{message}\\\""
        if price:
            flags = f"-p {price} {flags}"
        lines.append(f"tv alert create {flags} | ConvertTo-Json -Depth 10")
    elif jtype == "alert.delete":
        alert_id = params.get("alert_id", "")
        lines.append(f"tv alert delete --id {alert_id} | ConvertTo-Json -Depth 10")
    elif jtype == "alert.rotate_webhook_key":
        new_key = creds.get("TV_WEBHOOK_KEY", "") if creds else ""
        new_key_escaped = new_key.replace("'", "''")
        lines += [
            "$newKey = '" + new_key_escaped + "'",
            "$alerts = tv alert list",
            "$rotated = 0; $skipped = 0",
            "foreach ($a in $alerts.alerts) {",
            "  try {",
            "    $msg = $a.message | ConvertFrom-Json -ErrorAction Stop",
            "    if ($msg.PSObject.Properties.Name -contains 'key') {",
            "      $msg.key = $newKey",
            "      $newMsg = $msg | ConvertTo-Json -Compress",
            "      tv alert delete --id $a.id | Out-Null",
            "      tv alert create -c crossing -m $newMsg | Out-Null",
            "      $rotated++",
            "    } else { $skipped++ }",
            "  } catch { $skipped++ }",
            "}",
            "@{success=$true; rotated=$rotated; skipped=$skipped} | ConvertTo-Json",
        ]
    elif jtype == "indicator.add":
        name = params.get("name", "")
        pane = params.get("pane", "")
        pane_flag = f"--pane {pane}" if pane else ""
        lines.append(f"tv indicator add \"{name}\" {pane_flag} | ConvertTo-Json -Depth 10")
    elif jtype == "indicator.remove":
        entity_id = params.get("entity_id", "")
        lines.append(f"tv indicator remove {entity_id} | ConvertTo-Json -Depth 10")
    elif jtype == "indicator.set":
        entity_id = params.get("entity_id", "")
        inputs = params.get("inputs", {})
        input_flags = " ".join(f'--input "{k}={v}"' for k, v in inputs.items())
        lines.append(f"tv indicator set {entity_id} {input_flags} | ConvertTo-Json -Depth 10")
    elif jtype == "symbol.set":
        symbol = params.get("symbol", "")
        lines.append(f"tv symbol {symbol} | ConvertTo-Json -Depth 10")
    elif jtype == "timeframe.set":
        tf = params.get("timeframe", "")
        lines.append(f"tv timeframe {tf} | ConvertTo-Json -Depth 10")
    elif jtype == "pine.set":
        source = params.get("source", "")
        tmp_pine = r"C:\Users\ghost\AppData\Local\Temp\tv_pine_src.pine"
        escaped = source.replace("'", "''")
        lines += [
            f"Set-Content -Path '{tmp_pine}' -Value '{escaped}' -Encoding UTF8",
            f"tv pine set --file '{tmp_pine}' | ConvertTo-Json -Depth 10",
            f"Remove-Item -Force '{tmp_pine}' -ErrorAction SilentlyContinue",
        ]
    elif jtype == "pine.save":
        lines.append("tv pine save | ConvertTo-Json -Depth 10")
    elif jtype == "screenshot":
        out_path = params.get("output_path",
                              r"C:\Users\ghost\opt-trading\modules\tradingview_observer\output\screenshot.png")
        lines.append(f"tv screenshot --file '{out_path}' | ConvertTo-Json -Depth 10")
    elif jtype == "layout.switch":
        name = params.get("name", "")
        lines.append(f"tv layout switch \"{name}\" | ConvertTo-Json -Depth 10")

    return "\n".join(lines)


def run_job(job: dict, gate_approved: bool, dry_run: bool) -> dict:
    jtype = job["type"]
    is_mutation = jtype in MUTATION_TYPES

    if is_mutation and not gate_approved:
        print(f"REFUSED: {jtype} is a mutation — requires --gate-approved", file=sys.stderr)
        sys.exit(3)

    creds = None
    if jtype == "alert.rotate_webhook_key":
        key = load_env_var("TV_WEBHOOK_KEY")
        if not key:
            print("RUNNER_ERROR: TV_WEBHOOK_KEY not found in environment or .env", file=sys.stderr)
            sys.exit(5)
        creds = {"TV_WEBHOOK_KEY": key}

    ps1_script = build_ps1_for_job(job, creds)

    if dry_run:
        print("=== DRY RUN — PS1 script that would execute on cursor-ai ===")
        print(ps1_script.replace(creds["TV_WEBHOOK_KEY"] if creds else "", "<TV_WEBHOOK_KEY_MASKED>")
              if creds else ps1_script)
        return {"status": "dry_run", "job_type": jtype}

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".ps1", delete=False) as f:
        f.write(ps1_script)
        tmp_ps1 = Path(f.name)

    try:
        rc, out, err = ssh_run_ps_file(tmp_ps1)
    finally:
        tmp_ps1.unlink(missing_ok=True)

    result = {
        "job_id":    job["id"],
        "job_type":  jtype,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "exit_code": rc,
        "success":   rc == 0,
        "stderr":    err if err else None,
    }

    try:
        result["output"] = json.loads(out) if out else None
    except json.JSONDecodeError:
        result["output_raw"] = out

    report_path = REPORTS_DIR / f"{job['id']}_{ts()}.json"
    report_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"Report: {report_path}")

    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("packet", help="Path to tv_job_v1 JSON packet")
    ap.add_argument("--gate-approved", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    packet_path = Path(args.packet)
    if not packet_path.exists():
        print(f"INVALID_INPUT: packet file not found: {packet_path}", file=sys.stderr)
        sys.exit(1)

    try:
        job = json.loads(packet_path.read_text())
    except json.JSONDecodeError as e:
        print(f"INVALID_INPUT: JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if job.get("schema") != "tv_job_v1":
        print("INVALID_INPUT: expected schema=tv_job_v1", file=sys.stderr)
        sys.exit(1)

    result = run_job(job, args.gate_approved, args.dry_run)

    if result.get("success"):
        print(f"PASS: {job['type']} executed")
        sys.exit(0)
    else:
        print(f"RUNNER_ERROR: {result.get('stderr','unknown')}", file=sys.stderr)
        sys.exit(5)


if __name__ == "__main__":
    main()
