#!/usr/bin/env bash
# Start all TMUX sessions — openclaw-core first
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== TMUX SPINE START ==="
echo "DRY_RUN=1 PAPER_MODE=1 enforced on all pipeline workers"
echo ""

# Critical sessions first
bash "$SCRIPT_DIR/sessions/openclaw-core.sh"
bash "$SCRIPT_DIR/sessions/screeners.sh"
bash "$SCRIPT_DIR/sessions/strict-workers.sh"

# Non-critical sessions
bash "$SCRIPT_DIR/sessions/trading-pipeline.sh"
bash "$SCRIPT_DIR/sessions/market-data.sh"
bash "$SCRIPT_DIR/sessions/apps-connectors.sh"
bash "$SCRIPT_DIR/sessions/desk-pro.sh"
bash "$SCRIPT_DIR/sessions/kg-repo.sh"
bash "$SCRIPT_DIR/sessions/localcms-ui.sh"

echo ""
echo "=== ALL SESSIONS STARTED ==="
python3 "$SCRIPT_DIR/health_check.py"
