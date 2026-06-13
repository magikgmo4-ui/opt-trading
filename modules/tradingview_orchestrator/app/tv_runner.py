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
import base64
import copy
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parents[3]
REPORTS_DIR = REPO_ROOT / "reports" / "tradingview"

SSH_HOST        = "cursor-ai"
TV_OBS_WIN      = r"C:\Users\ghost\opt-trading\modules\tradingview_observer"
TV_PENDING_WIN  = rf"{TV_OBS_WIN}\jobs\pending"
TV_DONE_WIN     = rf"{TV_OBS_WIN}\jobs\done"
TV_CLI_WIN      = r"C:\Users\ghost\.claude\tools\tradingview-mcp\src\cli\index.js"

AGENT_POLL_TIMEOUT = 120   # max seconds to wait for agent result
AGENT_POLL_INTERVAL = 2

READ_ONLY_TYPES = {"snapshot", "alert.list", "screenshot"}
MUTATION_TYPES  = {
    "alert.create", "alert.delete", "alert.rotate_webhook_key",
    "indicator.add", "indicator.remove", "indicator.set",
    "symbol.set", "timeframe.set", "pine.set", "pine.save",
    "layout.switch"
}
SUPPORTED_ALERT_FREQUENCIES = {"on_bar_close", "on_first_fire"}
TV_WEBHOOK_KEY_PLACEHOLDERS = ("__TV_WEBHOOK_KEY__", "<TV_WEBHOOK_KEY>")
TV_WEBHOOK_KEY_MASK = "<TV_WEBHOOK_KEY_MASKED>"


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


def contains_webhook_key_placeholder(value) -> bool:
    if isinstance(value, str):
        return any(p in value for p in TV_WEBHOOK_KEY_PLACEHOLDERS)
    if isinstance(value, dict):
        return any(contains_webhook_key_placeholder(v) for v in value.values())
    if isinstance(value, list):
        return any(contains_webhook_key_placeholder(v) for v in value)
    return False


def replace_webhook_key_placeholders(value, key: str):
    if isinstance(value, str):
        for placeholder in TV_WEBHOOK_KEY_PLACEHOLDERS:
            value = value.replace(placeholder, key)
        return value
    if isinstance(value, dict):
        return {k: replace_webhook_key_placeholders(v, key) for k, v in value.items()}
    if isinstance(value, list):
        return [replace_webhook_key_placeholders(v, key) for v in value]
    return value


def mask_webhook_key(value, key: str = ""):
    if isinstance(value, str):
        if key:
            value = value.replace(key, TV_WEBHOOK_KEY_MASK)
        for placeholder in TV_WEBHOOK_KEY_PLACEHOLDERS:
            value = value.replace(placeholder, TV_WEBHOOK_KEY_MASK)
        return value
    if isinstance(value, dict):
        return {k: mask_webhook_key(v, key) for k, v in value.items()}
    if isinstance(value, list):
        return [mask_webhook_key(v, key) for v in value]
    return value


def prepare_job_for_dispatch(job: dict, require_secrets: bool) -> dict:
    """Validate job packet and materialize runtime-only secrets before dispatch."""
    job = copy.deepcopy(job)
    jtype = job["type"]
    params = job.setdefault("params", {})

    if jtype == "alert.create":
        if "webhook" in params and "webhook_url" not in params:
            raise ValueError("alert.create params must use webhook_url, not legacy webhook")
        if not params.get("webhook_url"):
            raise ValueError("alert.create requires params.webhook_url")
        if not params.get("message"):
            raise ValueError("alert.create requires params.message")

        frequency = params.get("frequency") or "on_bar_close"
        if frequency not in SUPPORTED_ALERT_FREQUENCIES:
            allowed = ", ".join(sorted(SUPPORTED_ALERT_FREQUENCIES))
            raise ValueError(f"alert.create frequency '{frequency}' is unsupported; allowed: {allowed}")
        params["frequency"] = frequency

        if contains_webhook_key_placeholder(params.get("message")):
            if not require_secrets:
                return job
            key = load_env_var("TV_WEBHOOK_KEY")
            if not key:
                raise ValueError("TV_WEBHOOK_KEY not found in environment or .env")
            params["message"] = replace_webhook_key_placeholders(params["message"], key)

        if require_secrets and contains_webhook_key_placeholder(params.get("message")):
            raise ValueError("alert.create message still contains TV webhook key placeholder")

    elif jtype == "alert.rotate_webhook_key":
        if require_secrets:
            key = load_env_var("TV_WEBHOOK_KEY")
            if not key:
                raise ValueError("TV_WEBHOOK_KEY not found in environment or .env")
            params["new_key_value"] = key  # agent reads this; never committed

    return job


def ssh_simple(cmd_str: str, timeout: int = 15) -> tuple[int, str, str]:
    """Run a simple shell command on cursor-ai via SSH."""
    cmd = ["ssh", "-o", "BatchMode=yes", "-o", f"ConnectTimeout={timeout}", SSH_HOST, cmd_str]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 5)
        out = r.stdout.decode("utf-8", errors="replace").strip()
        err = r.stderr.decode("utf-8", errors="replace").strip()
        return r.returncode, out, err
    except subprocess.TimeoutExpired:
        return 5, "", f"SSH timed out after {timeout}s"
    except Exception as e:
        return 5, "", str(e)


def _win_to_scp(win_path: str) -> str:
    """Convert Windows path (C:\foo\bar) to SCP POSIX form (/C:/foo/bar)."""
    p = win_path.replace("\\", "/")
    if len(p) >= 2 and p[1] == ":":
        p = "/" + p
    return p


def scp_to_cursor(local_path: Path, remote_win_path: str, timeout: int = 20) -> tuple[int, str]:
    """SCP a local file to cursor-ai Windows path."""
    remote = f"{SSH_HOST}:{_win_to_scp(remote_win_path)}"
    cmd = ["scp", "-o", "BatchMode=yes", str(local_path), remote]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
        err = r.stderr.decode("utf-8", errors="replace").strip()
        return r.returncode, err
    except subprocess.TimeoutExpired:
        return 5, f"SCP timed out after {timeout}s"
    except Exception as e:
        return 5, str(e)


def scp_from_cursor(remote_win_path: str, local_path: Path, timeout: int = 20) -> tuple[int, str]:
    """SCP a file from cursor-ai Windows path to local."""
    remote = f"{SSH_HOST}:{_win_to_scp(remote_win_path)}"
    cmd = ["scp", "-o", "BatchMode=yes", remote, str(local_path)]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
        err = r.stderr.decode("utf-8", errors="replace").strip()
        return r.returncode, err
    except subprocess.TimeoutExpired:
        return 5, f"SCP timed out after {timeout}s"
    except Exception as e:
        return 5, str(e)


def poll_for_result(job_id: str, timeout: int = AGENT_POLL_TIMEOUT) -> dict | None:
    """Poll cursor-ai jobs/done/<job_id>.result.json — SCP attempt each interval (fast)."""
    remote_result = rf"{TV_DONE_WIN}\{job_id}.result.json"
    local_tmp = REPORTS_DIR / f"_result_{job_id}.json"
    deadline = time.time() + timeout
    while time.time() < deadline:
        rc, _ = scp_from_cursor(remote_result, local_tmp, timeout=8)
        if rc == 0 and local_tmp.exists() and local_tmp.stat().st_size > 0:
            try:
                # utf-8-sig strips BOM that PowerShell Set-Content -Encoding UTF8 adds
                data = json.loads(local_tmp.read_text(encoding="utf-8-sig", errors="replace"))
                local_tmp.unlink(missing_ok=True)
                return data
            except json.JSONDecodeError:
                raw = local_tmp.read_text(encoding="utf-8-sig", errors="replace")
                local_tmp.unlink(missing_ok=True)
                return {"success": False, "error": "result JSON parse failed", "raw": raw}
        local_tmp.unlink(missing_ok=True)
        time.sleep(AGENT_POLL_INTERVAL)
    return None


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
        if params.get("webhook_url"):
            flags = f"{flags} --webhook \\\"{params['webhook_url']}\\\""
        if params.get("name"):
            flags = f"{flags} --name \\\"{params['name']}\\\""
        if params.get("frequency"):
            flags = f"{flags} --frequency {params['frequency']}"
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

    try:
        job = prepare_job_for_dispatch(job, require_secrets=not dry_run)
    except ValueError as e:
        print(f"INVALID_INPUT: {e}", file=sys.stderr)
        sys.exit(1)

    if dry_run:
        print(f"=== DRY RUN — job packet that would be submitted to cursor-ai agent ===")
        display = mask_webhook_key(copy.deepcopy(job), load_env_var("TV_WEBHOOK_KEY"))
        if "params" in display and "new_key_value" in display["params"]:
            display["params"]["new_key_value"] = TV_WEBHOOK_KEY_MASK
        print(json.dumps(display, indent=2))
        return {"success": True, "status": "dry_run", "job_type": jtype}

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Write job packet locally, SCP to cursor-ai jobs/pending/
    job_id = job["id"]
    local_packet = REPORTS_DIR / f"_pending_{job_id}.json"
    local_packet.write_text(json.dumps(job, indent=2, ensure_ascii=False))

    remote_pending = rf"{TV_PENDING_WIN}\{job_id}.json"
    rc, err = scp_to_cursor(local_packet, remote_pending)
    local_packet.unlink(missing_ok=True)

    if rc != 0:
        result = {"job_id": job_id, "job_type": jtype, "success": False,
                  "error": f"SCP to cursor-ai failed: {err}",
                  "executed_at": datetime.now(timezone.utc).isoformat()}
        report_path = REPORTS_DIR / f"{job_id}_{ts()}.json"
        report_path.write_text(json.dumps(result, indent=2))
        print(f"Report: {report_path}")
        return result

    print(f"Job dispatched to cursor-ai agent: {job_id} (type={jtype})")
    print(f"Waiting for result (timeout={AGENT_POLL_TIMEOUT}s)...")

    agent_result = poll_for_result(job_id)

    if agent_result is None:
        result = {"job_id": job_id, "job_type": jtype, "success": False,
                  "error": f"Agent timeout after {AGENT_POLL_TIMEOUT}s — agent running?",
                  "executed_at": datetime.now(timezone.utc).isoformat()}
    else:
        result = agent_result
        result["job_id"]      = job_id
        result["job_type"]    = jtype
        result["executed_at"] = result.get("executed_at", datetime.now(timezone.utc).isoformat())

    report_path = REPORTS_DIR / f"{job_id}_{ts()}.json"
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
