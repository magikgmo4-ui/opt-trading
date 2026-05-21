#!/usr/bin/env python3
"""Generate a LocalCMS automation status snapshot.

This Phase 01 runner is intentionally local-only:
- reads repo/menu/ledger/report state
- writes a consolidated JSON snapshot to tmp/localcms_latest.json
- writes a report artifact to reports/ai/localcms_automation_status_sync.json
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MENU_FILE = REPO_ROOT / "scripts" / "ai" / "menu" / "opt_trading_menu.json"
STATE_CACHE = REPO_ROOT / "scripts" / "ai" / "menu" / "state_cache.json"
LEDGER_FILE = REPO_ROOT / "data" / "runtime_health" / "ledger" / "events.jsonl"
HEALTH_STATUS_FILE = REPO_ROOT / "reports" / "ai" / "health_status.json"
LOCALCMS_LATEST_JSON = REPO_ROOT / "tmp" / "localcms_latest.json"
REPORT_FILE = REPO_ROOT / "reports" / "ai" / "localcms_automation_status_sync.json"


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def git_info() -> dict:
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=False,
        ).stdout.strip()
        commit = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=False,
        ).stdout.strip()
        return {"branch": branch or "unknown", "commit": commit or "unknown"}
    except Exception:
        return {"branch": "unknown", "commit": "unknown"}


def tmux_sessions() -> dict:
    try:
        result = subprocess.run(
            ["tmux", "list-sessions", "-F", "#S"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode != 0:
            return {"available": False, "sessions": []}
        sessions = sorted(s.strip() for s in result.stdout.splitlines() if s.strip())
        return {"available": True, "sessions": sessions, "count": len(sessions)}
    except Exception:
        return {"available": False, "sessions": [], "count": 0}


def ledger_summary() -> dict:
    if not LEDGER_FILE.exists():
        return {"exists": False, "event_count": 0, "last_event": None}
    try:
        lines = [line for line in LEDGER_FILE.read_text().splitlines() if line.strip()]
        last_event = json.loads(lines[-1]) if lines else None
        return {
            "exists": True,
            "event_count": len(lines),
            "last_event": {
                "event_type": last_event.get("event_type"),
                "status": last_event.get("status"),
                "timestamp": last_event.get("timestamp"),
            } if last_event else None,
        }
    except Exception:
        return {"exists": True, "event_count": -1, "last_event": None}


def build_snapshot() -> dict:
    menu = read_json(MENU_FILE)
    state = read_json(STATE_CACHE)
    health = read_json(HEALTH_STATUS_FILE)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git": git_info(),
        "menu_loaded": menu is not None,
        "menu_domains": len(menu.get("menu", [])) if isinstance(menu, dict) else 0,
        "state_cache_loaded": state is not None,
        "health_status_loaded": health is not None,
        "health_status": health,
        "ledger": ledger_summary(),
        "tmux": tmux_sessions(),
        "phase": "PHASE_01",
        "job_id": "localcms-automation-status-sync",
        "mode": "write-gated/local",
        "allowed_writes": [
            str(LOCALCMS_LATEST_JSON.relative_to(REPO_ROOT)),
            str(REPORT_FILE.relative_to(REPO_ROOT)),
        ],
        "status": "PASS",
    }


def main() -> int:
    snapshot = build_snapshot()
    LOCALCMS_LATEST_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCALCMS_LATEST_JSON.write_text(json.dumps(snapshot, indent=2) + "\n")
    REPORT_FILE.write_text(json.dumps(snapshot, indent=2) + "\n")
    print(f"LocalCMS snapshot written to {LOCALCMS_LATEST_JSON}")
    print(f"Report written to {REPORT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
