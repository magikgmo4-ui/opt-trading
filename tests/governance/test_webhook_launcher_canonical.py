"""
GO_RUNTIME_WEBHOOK_LAUNCHER_CANONICAL_GUARD_01

Policy: runtime tmux session scripts must never call python3/python directly
on webhook_server.py. The canonical launcher is webhook_daemon.sh start,
which owns the PID file and port-conflict detection.

Root cause of guard: screeners.sh was using `python3 webhook_server.py`
which exits immediately (no __main__ block), leaving the webhook process
never started — fixed in sot/mainline 01c5190c.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SESSIONS_DIR = REPO_ROOT / "scripts" / "tmux" / "sessions"
TMUX_DIR = REPO_ROOT / "scripts" / "tmux"

# Pattern that must never appear in runtime session scripts
_BAD = re.compile(r"\bpython3?\s+webhook_server\.py\b")

# Canonical launcher that must be present in the screeners session script
_CANONICAL = "webhook_daemon.sh start"
_SCREENERS = SESSIONS_DIR / "screeners.sh"


def _runtime_scripts():
    """All .sh files under scripts/tmux/ (sessions + helpers)."""
    return sorted(TMUX_DIR.rglob("*.sh"))


def test_sessions_dir_exists():
    assert SESSIONS_DIR.is_dir(), f"sessions dir missing: {SESSIONS_DIR}"


def test_no_direct_python_webhook_in_session_scripts():
    """No session script may invoke webhook_server.py via python directly."""
    violations = []
    for script in _runtime_scripts():
        for lineno, line in enumerate(script.read_text(encoding="utf-8").splitlines(), 1):
            if _BAD.search(line):
                violations.append(f"{script.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}")

    assert not violations, (
        "Direct python invocation of webhook_server.py found in runtime scripts.\n"
        "Use 'bash scripts/webhook_daemon.sh start' instead.\n"
        "Violations:\n" + "\n".join(f"  {v}" for v in violations)
    )


def test_screeners_uses_canonical_launcher():
    """screeners.sh must use webhook_daemon.sh start for the webhook window."""
    assert _SCREENERS.exists(), f"screeners.sh not found: {_SCREENERS}"
    content = _SCREENERS.read_text(encoding="utf-8")
    assert _CANONICAL in content, (
        f"screeners.sh does not contain the canonical launcher '{_CANONICAL}'.\n"
        f"The webhook window must use: bash scripts/webhook_daemon.sh start"
    )


def test_webhook_daemon_script_exists():
    """The canonical launcher must exist."""
    daemon = REPO_ROOT / "scripts" / "webhook_daemon.sh"
    assert daemon.exists(), f"Canonical launcher missing: {daemon}"


def test_webhook_daemon_is_executable():
    """The canonical launcher must be executable."""
    import os
    daemon = REPO_ROOT / "scripts" / "webhook_daemon.sh"
    assert daemon.exists()
    assert os.access(daemon, os.X_OK), f"webhook_daemon.sh is not executable: {daemon}"
