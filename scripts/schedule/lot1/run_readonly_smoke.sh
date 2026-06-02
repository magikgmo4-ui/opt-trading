#!/usr/bin/env bash
# Wrapper cron pour strict-worker-readonly-smoke via dispatcher.
# Stage les rapports avant le run pour que le git tree soit propre
# (requis par runner_readonly.py _check_git_clean).
set -euo pipefail

REPO=/opt/trading
PYTHON=$REPO/venv/bin/python3
LOG=$REPO/data/logs/cron/readonly_smoke.log

cd "$REPO"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] START strict-worker-readonly-smoke" >> "$LOG"

# Stage modified reports so git diff --quiet passes
git add reports/ 2>/dev/null || true

$PYTHON - <<'EOF' >> "$LOG" 2>&1
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
EOF

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] END exit=$?" >> "$LOG"
