"""TMUX session health checker — importable for tests, runnable as CLI."""
from __future__ import annotations
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CRITICAL_SESSIONS: frozenset[str] = frozenset({
    "openclaw-core",
    "screeners",
    "strict-workers",
})

ALL_SESSIONS: frozenset[str] = frozenset({
    "openclaw-core",
    "screeners",
    "strict-workers",
    "trading-pipeline",
    "market-data",
    "apps-connectors",
    "desk-pro",
    "kg-repo",
    "localcms-ui",
    "fleet-status",
})


def list_tmux_sessions() -> list[str]:
    """Return active tmux session names. Returns [] if tmux not running."""
    try:
        result = subprocess.run(
            ["tmux", "list-sessions", "-F", "#S"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode != 0:
            return []
        return [s.strip() for s in result.stdout.splitlines() if s.strip()]
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return []


def check_sessions(
    expected: frozenset[str] | None = None,
    active: list[str] | None = None,
) -> dict:
    """Return health report dict.

    Pass `active` explicitly to avoid subprocess calls (testing / dry-run).
    """
    if expected is None:
        expected = ALL_SESSIONS
    if active is None:
        active = list_tmux_sessions()

    active_set = frozenset(active)
    up = expected & active_set
    missing = expected - active_set
    critical_down = missing & CRITICAL_SESSIONS
    non_critical_down = missing - CRITICAL_SESSIONS

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "all_ok": len(missing) == 0,
        "needs_alert": len(critical_down) > 0,
        "up": sorted(up),
        "missing": sorted(missing),
        "critical_down": sorted(critical_down),
        "non_critical_down": sorted(non_critical_down),
        "summary": _format_summary(up, missing, critical_down),
    }


def _format_summary(up: frozenset, missing: frozenset, critical_down: frozenset) -> str:
    lines: list[str] = []
    for s in sorted(up):
        lines.append(f"SESSION_OK       {s}")
    for s in sorted(missing):
        tag = "CRITICAL_DOWN   " if s in critical_down else "SESSION_MISSING "
        lines.append(f"{tag}{s}")
    return "\n".join(lines)


def main() -> int:
    report = check_sessions()
    print(json.dumps(report, indent=2))
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
