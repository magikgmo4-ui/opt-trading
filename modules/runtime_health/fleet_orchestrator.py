#!/usr/bin/env python3
"""
fleet_orchestrator.py — aggregate latest.json from all machines, produce fleet_status.json.

Usage (standalone):
    python3 modules/runtime_health/fleet_orchestrator.py [--map config/machine_runtime_map.yml]

The orchestrator reads latest.json from each known machine.
Collection strategy (in order of preference):
  1. Shared SSHFS mount: /shared/<machine>/runtime_health/latest.json
  2. SSH pull: ssh <machine> cat /opt/trading/data/runtime_health/latest.json
  3. Local file: /opt/trading/data/runtime_health/latest.json (self)

Output:
  /opt/trading/data/runtime_health/fleet_status.json
  /opt/trading/data/runtime_health/fleet_status.jsonl
"""

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"

_STALE_THRESHOLD_MINUTES = 15
_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_MAP = _REPO_ROOT / "config" / "machine_runtime_map.yml"


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def _load_map(path: str) -> Dict[str, Any]:
    try:
        import yaml
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def _run(cmd: List[str], timeout: int = 8) -> Tuple[int, str, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)


# ---------------------------------------------------------------------------
# Machine status collection
# ---------------------------------------------------------------------------

def _collect_via_sshfs(machine: str, data_dir: str) -> Optional[Dict]:
    candidates = [
        Path(f"/shared/{machine}/runtime_health/latest.json"),
        Path(f"/opt/trading/data/shared/{machine}/runtime_health/latest.json"),
        Path(f"/srv/sftp/shared_files/{machine}/runtime_health/latest.json"),
    ]
    for p in candidates:
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                pass
    return None


def _collect_via_ssh(machine: str) -> Optional[Dict]:
    rc, out, err = _run(
        ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5",
         machine, "cat /opt/trading/data/runtime_health/latest.json"],
        timeout=10,
    )
    if rc == 0 and out.startswith("{"):
        try:
            return json.loads(out)
        except Exception:
            pass
    return None


def _collect_local(data_dir: str) -> Optional[Dict]:
    p = Path(data_dir) / "latest.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def collect_machine_status(
    machine: str,
    hostname: str,
    data_dir: str,
) -> Dict[str, Any]:
    """Collect latest.json for a machine. Try sshfs, then ssh, then local."""
    collected: Optional[Dict] = None
    source = "none"

    if machine == hostname:
        collected = _collect_local(data_dir)
        if collected:
            source = "local"
    else:
        collected = _collect_via_sshfs(machine, data_dir)
        if collected:
            source = "sshfs"
        else:
            collected = _collect_via_ssh(machine)
            if collected:
                source = "ssh"

    if collected is None:
        return {
            "machine": machine,
            "source": "none",
            "reachable": False,
            "status": WARN,
            "detail": "no latest.json found (sshfs, ssh, local all failed)",
            "overall_status": None,
            "timestamp": None,
            "age_minutes": None,
        }

    ts_str = collected.get("timestamp", "")
    age_min: Optional[float] = None
    stale = False
    if ts_str:
        try:
            from datetime import datetime, timezone
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            age_min = (datetime.now(timezone.utc) - ts).total_seconds() / 60.0
            stale = age_min > _STALE_THRESHOLD_MINUTES
        except Exception:
            pass

    machine_status = collected.get("overall_status", WARN)

    if stale:
        fleet_status = WARN
        detail = f"stale ({age_min:.1f}m > {_STALE_THRESHOLD_MINUTES}m threshold)"
    else:
        fleet_status = machine_status
        detail = f"age={age_min:.1f}m" if age_min is not None else "age unknown"

    return {
        "machine": machine,
        "source": source,
        "reachable": True,
        "status": fleet_status,
        "overall_status": machine_status,
        "timestamp": ts_str,
        "age_minutes": round(age_min, 1) if age_min is not None else None,
        "stale": stale,
        "block_statuses": collected.get("block_statuses", {}),
        "detail": detail,
    }


# ---------------------------------------------------------------------------
# Fleet aggregation
# ---------------------------------------------------------------------------

def run_fleet(
    map_path: str,
    data_dir: str,
    dry_run: bool = False,
) -> Dict[str, Any]:
    map_data = _load_map(map_path)
    known_machines = list(map_data.get("machines", {}).keys())
    hostname = socket.gethostname()

    machine_results: List[Dict] = []
    for machine in known_machines:
        result = collect_machine_status(machine, hostname, data_dir)
        machine_results.append(result)

    healthy = [r["machine"] for r in machine_results if r["status"] == PASS]
    warning = [r["machine"] for r in machine_results if r["status"] == WARN]
    failing = [r["machine"] for r in machine_results if r["status"] == FAIL]
    unreachable = [r["machine"] for r in machine_results if not r["reachable"]]
    stale = [r["machine"] for r in machine_results if r.get("stale", False)]

    if failing:
        fleet_overall = FAIL
    elif warning or unreachable or stale:
        fleet_overall = WARN
    else:
        fleet_overall = PASS

    run_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    report: Dict[str, Any] = {
        "timestamp": timestamp,
        "orchestrator_host": hostname,
        "run_id": run_id,
        "fleet_status": fleet_overall,
        "known_machines": known_machines,
        "healthy_machines": healthy,
        "warning_machines": warning,
        "failing_machines": failing,
        "unreachable_machines": unreachable,
        "stale_machines": stale,
        "machines": {r["machine"]: r for r in machine_results},
    }

    if not dry_run:
        out_dir = Path(data_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        (out_dir / "fleet_status.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )

        line = {
            "timestamp": timestamp,
            "run_id": run_id,
            "orchestrator_host": hostname,
            "fleet_status": fleet_overall,
            "healthy": healthy,
            "warning": warning,
            "failing": failing,
            "unreachable": unreachable,
            "stale": stale,
        }
        with open(out_dir / "fleet_status.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(line) + "\n")

    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="opt-trading Fleet Orchestrator")
    parser.add_argument("--map", default=str(_DEFAULT_MAP), help="Path to machine_runtime_map.yml")
    parser.add_argument("--data-dir", default="/opt/trading/data/runtime_health",
                        help="Output data directory")
    parser.add_argument("--dry-run", action="store_true", help="Print results, do not write files")
    args = parser.parse_args()

    t0 = time.monotonic()
    report = run_fleet(args.map, args.data_dir, dry_run=args.dry_run)
    elapsed = round(time.monotonic() - t0, 3)

    summary = {
        "timestamp": report["timestamp"],
        "run_id": report["run_id"],
        "fleet_status": report["fleet_status"],
        "healthy": report["healthy_machines"],
        "warning": report["warning_machines"],
        "failing": report["failing_machines"],
        "unreachable": report["unreachable_machines"],
        "stale": report["stale_machines"],
        "elapsed_seconds": elapsed,
    }
    print(json.dumps(summary, indent=2))

    return 0 if report["fleet_status"] in (PASS, WARN) else 1


if __name__ == "__main__":
    sys.exit(main())
