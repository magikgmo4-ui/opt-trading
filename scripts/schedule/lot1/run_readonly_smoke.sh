#!/usr/bin/env bash
# Wrapper cron pour strict-worker-readonly-smoke via dispatcher.
# Stage les rapports avant le run (requis par runner_readonly.py _check_git_clean).
# Runs inside a named tmux window for live visibility: session=cron-workers window=readonly-smoke
set -euo pipefail

REPO=/opt/trading
PYTHON=$REPO/venv/bin/python3
LOG=$REPO/data/logs/cron/readonly_smoke.log
TMUX_SESSION="cron-workers"
TMUX_WINDOW="readonly-smoke"

# If already running inside tmux, skip the re-launch to avoid recursion
if [ -n "${TMUX:-}" ]; then
    _run_smoke() {
        cd "$REPO"
        echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] START strict-worker-readonly-smoke" | tee -a "$LOG"
        git add reports/ 2>/dev/null || true
        $PYTHON - 2>&1 | tee -a "$LOG" <<'PYEOF'
import sys
sys.path.insert(0, "/opt/trading/modules/openclaw_operator_bridge")
from app.schema import BridgeRequest
from app.bridge import OperatorBridge
resp = OperatorBridge().send(BridgeRequest(
    action="dispatch",
    instruction="scheduled readonly smoke",
    parameters={"packet_id": "GO_STRICT_WORKERS_READONLY_SMOKE_01", "dry_run": True}
))
print(f"status={resp.status} content={resp.content} error={resp.error}")
sys.exit(0 if resp.status == "ok" else 1)
PYEOF
        echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] END exit=$?" | tee -a "$LOG"
    }
    _run_smoke
    exit $?
fi

# Outside tmux — ensure session exists then run in named window
mkdir -p "$(dirname "$LOG")"

if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    tmux new-session -d -s "$TMUX_SESSION" -x 220 -y 50
fi

# Kill stale window if it exists (previous run may have left it)
tmux kill-window -t "$TMUX_SESSION:$TMUX_WINDOW" 2>/dev/null || true

# Launch smoke in a new window — window auto-closes when done
tmux new-window -t "$TMUX_SESSION" -n "$TMUX_WINDOW" \
    "bash $REPO/scripts/schedule/lot1/run_readonly_smoke.sh; sleep 30"
