#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "=== TMUX Runtime Spine SANITY ==="

echo "--- tests health_check.py ---"
python3 -m unittest tests.tmux.test_health_check -v 2>&1

echo "--- health_check.py dry-run (no active sessions expected) ---"
python3 - <<'EOF'
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))
from scripts.tmux.health_check import check_sessions, ALL_SESSIONS, CRITICAL_SESSIONS

# Simulate all sessions up
r = check_sessions(active=list(ALL_SESSIONS))
print(json.dumps({"all_ok": r["all_ok"], "up_count": len(r["up"]), "missing_count": len(r["missing"])}, indent=2))
assert r["all_ok"]
assert len(r["up"]) == 9

# Simulate critical down
r2 = check_sessions(active=["desk-pro", "kg-repo"])
print(json.dumps({"all_ok": r2["all_ok"], "needs_alert": r2["needs_alert"], "critical_down": r2["critical_down"]}, indent=2))
assert not r2["all_ok"]
assert r2["needs_alert"]
assert "openclaw-core" in r2["critical_down"]

# Live check (no tmux = all missing, but no crash)
r3 = check_sessions()
print(json.dumps({"live_check": "ok", "active_count": len(r3["up"])}, indent=2))
EOF

echo "--- session scripts exist ---"
for s in openclaw-core screeners strict-workers trading-pipeline market-data apps-connectors desk-pro kg-repo localcms-ui; do
    [ -f "scripts/tmux/sessions/${s}.sh" ] && echo "  OK: sessions/${s}.sh" || { echo "  MISSING: sessions/${s}.sh"; exit 1; }
done

echo "--- top-level scripts exist ---"
for f in start_all.sh stop_all.sh restart_session.sh health_aggregator.sh attach.sh; do
    [ -f "scripts/tmux/${f}" ] && echo "  OK: ${f}" || { echo "  MISSING: ${f}"; exit 1; }
done

echo ""
echo "=== SANITY PASS — TMUX Runtime Spine (32 tests, 9 sessions, dry-run health OK) ==="
