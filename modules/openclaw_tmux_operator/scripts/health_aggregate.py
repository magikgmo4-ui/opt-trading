#!/usr/bin/env python3
"""
health_aggregate.py — multi-machine tmux + runtime-health aggregation.

READ_ONLY: collects status via SSH or local reads, no writes, no session modifications.

Usage:
    python3 modules/openclaw_tmux_operator/scripts/health_aggregate.py
    python3 modules/openclaw_tmux_operator/scripts/health_aggregate.py --machines db-layer,admin-trading
    python3 modules/openclaw_tmux_operator/scripts/health_aggregate.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_MAP = _REPO_ROOT / "config" / "machine_runtime_map.yml"
_RUNTIME_HEALTH_PATH = "/opt/trading/data/runtime_health/latest.json"
_FLEET_STATUS_PATH = _REPO_ROOT / "data" / "runtime_health" / "fleet_status.json"


def _load_map(path: str) -> Dict[str, Any]:
    try:
        import yaml
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def _run_ssh(host: str, cmd: str, timeout: int = 8) -> Tuple[int, str]:
    try:
        r = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", host, cmd],
            capture_output=True, text=True, timeout=timeout,
        )
        return r.returncode, r.stdout.strip()
    except subprocess.TimeoutExpired:
        return -1, "timeout"
    except Exception as e:
        return -1, str(e)


def collect_tmux_sessions(machine: str, hostname: str) -> Dict[str, Any]:
    """Return tmux session list for a machine. Local or via SSH."""
    if machine == hostname:
        try:
            r = subprocess.run(
                ["tmux", "list-sessions", "-F", "#S"],
                capture_output=True, text=True, timeout=5,
            )
            sessions = (
                [s.strip() for s in r.stdout.splitlines() if s.strip()]
                if r.returncode == 0 else []
            )
            return {"reachable": True, "source": "local", "sessions": sessions}
        except Exception:
            return {"reachable": True, "source": "local", "sessions": []}
    else:
        rc, out = _run_ssh(machine, "tmux list-sessions -F '#S' 2>/dev/null || true")
        if rc == -1:
            return {"reachable": False, "source": "ssh", "sessions": []}
        sessions = [s.strip() for s in out.splitlines() if s.strip()]
        return {"reachable": True, "source": "ssh", "sessions": sessions}


def collect_runtime_health(machine: str, hostname: str) -> Optional[Dict[str, Any]]:
    """Return parsed latest.json for a machine, or None if unavailable."""
    if machine == hostname:
        p = Path(_RUNTIME_HEALTH_PATH)
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                pass
        return None
    else:
        rc, out = _run_ssh(machine, f"cat {_RUNTIME_HEALTH_PATH} 2>/dev/null || true")
        if rc != -1 and out.startswith("{"):
            try:
                return json.loads(out)
            except Exception:
                pass
        return None


def collect_fleet_entry(machine: str) -> Optional[Dict[str, Any]]:
    """Return per-machine entry from local fleet_status.json (orchestrator output)."""
    if not _FLEET_STATUS_PATH.exists():
        return None
    try:
        data = json.loads(_FLEET_STATUS_PATH.read_text(encoding="utf-8"))
        return data.get("machines", {}).get(machine)
    except Exception:
        return None


def aggregate_machine(
    machine: str,
    hostname: str,
    injected: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Aggregate tmux + health + fleet for one machine.

    Pass ``injected`` to bypass SSH (tests / dry-run):
        {"tmux": {"reachable": True, "source": "injected", "sessions": [...]},
         "health": None | {...},
         "fleet": None | {"overall_status": ..., "stale": ...}}
    """
    if injected is not None:
        tmux_info = injected.get(
            "tmux", {"reachable": True, "source": "injected", "sessions": []}
        )
        health_info = injected.get("health")
        fleet_entry = injected.get("fleet")
    else:
        tmux_info = collect_tmux_sessions(machine, hostname)
        health_info = collect_runtime_health(machine, hostname)
        fleet_entry = collect_fleet_entry(machine)

    result: Dict[str, Any] = {
        "machine": machine,
        "reachable": tmux_info.get("reachable", False),
        "tmux_source": tmux_info.get("source", "unknown"),
        "tmux_sessions": sorted(tmux_info.get("sessions", [])),
        "runtime_health_status": None,
        "runtime_health_age_minutes": None,
        "fleet_status": None,
        "fleet_stale": None,
    }

    if health_info:
        result["runtime_health_status"] = health_info.get("overall_status")
        ts_str = health_info.get("timestamp", "")
        if ts_str:
            try:
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                age = (datetime.now(timezone.utc) - ts).total_seconds() / 60.0
                result["runtime_health_age_minutes"] = round(age, 1)
            except Exception:
                pass

    if fleet_entry:
        result["fleet_status"] = fleet_entry.get("overall_status")
        result["fleet_stale"] = fleet_entry.get("stale", False)

    return result


def run_aggregate(
    machines: List[str],
    hostname: Optional[str] = None,
    injected_map: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Aggregate health for all given machines."""
    if hostname is None:
        hostname = socket.gethostname()

    results: List[Dict[str, Any]] = []
    for machine in machines:
        injected = (injected_map or {}).get(machine)
        result = aggregate_machine(machine, hostname, injected=injected)
        results.append(result)

    reachable = [r["machine"] for r in results if r["reachable"]]
    unreachable = [r["machine"] for r in results if not r["reachable"]]

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "orchestrator_host": hostname,
        "machines": {r["machine"]: r for r in results},
        "reachable_machines": reachable,
        "unreachable_machines": unreachable,
        "total": len(machines),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="openclaw_tmux_operator — multi-machine health aggregator"
    )
    parser.add_argument("--map", default=str(_DEFAULT_MAP), help="Path to machine_runtime_map.yml")
    parser.add_argument(
        "--machines",
        default="",
        help="Comma-separated machine names (default: all Linux machines from map)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip SSH, return empty sessions (for CI / local testing)",
    )
    args = parser.parse_args()

    if args.machines:
        machine_list = [m.strip() for m in args.machines.split(",") if m.strip()]
    else:
        map_data = _load_map(args.map)
        all_machines = map_data.get("machines", {})
        machine_list = [
            m
            for m, cfg in all_machines.items()
            if cfg.get("os_family", "linux").lower() != "windows"
        ]

    hostname = socket.gethostname()

    if args.dry_run:
        injected: Dict[str, Dict[str, Any]] = {
            m: {
                "tmux": {"reachable": True, "source": "dry-run", "sessions": []},
                "health": None,
                "fleet": None,
            }
            for m in machine_list
        }
        report = run_aggregate(machine_list, hostname=hostname, injected_map=injected)
    else:
        report = run_aggregate(machine_list, hostname=hostname)

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
