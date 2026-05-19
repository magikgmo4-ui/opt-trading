#!/usr/bin/env bash
# fleet_start.sh — démarre les sessions tmux de monitoring sur db-layer et admin-trading
# Deux modes :
#   --monitoring  : sessions read-only seulement (fleet-status, health)
#   --full        : toutes les sessions (start_all.sh local + sessions admin-trading)
#   --dry-run     : affiche ce qui serait lancé, sans lancer
# Usage: bash scripts/tmux/fleet_start.sh [--monitoring|--full|--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MODE="${1:---monitoring}"

run() {
    if [ "$MODE" = "--dry-run" ]; then
        echo "  [DRY] $*"
    else
        eval "$@"
    fi
}

remote_run() {
    local host="$1"; shift
    if [ "$MODE" = "--dry-run" ]; then
        echo "  [DRY] ssh $host: $*"
    else
        ssh -o BatchMode=yes -o ConnectTimeout=5 "$host" "cd /opt/trading && $*"
    fi
}

echo "=== Fleet tmux Start ($MODE) ==="
echo "Host: $(hostname)"
echo ""

# ── db-layer — sessions monitoring ────────────────────────────────────────
echo "--- db-layer ---"

if [ "$MODE" = "--monitoring" ] || [ "$MODE" = "--full" ] || [ "$MODE" = "--dry-run" ]; then
    # fleet-status: monitoring read-only, toujours safe
    run "bash '$SCRIPT_DIR/sessions/fleet-status.sh'"
fi

if [ "$MODE" = "--full" ]; then
    run "bash '$SCRIPT_DIR/sessions/openclaw-core.sh'"
    run "bash '$SCRIPT_DIR/sessions/strict-workers.sh'"
    run "bash '$SCRIPT_DIR/sessions/kg-repo.sh'"
    run "bash '$SCRIPT_DIR/sessions/localcms-ui.sh'"
fi

echo ""

# ── admin-trading — sessions services ─────────────────────────────────────
echo "--- admin-trading ---"

if [ "$MODE" = "--full" ]; then
    remote_run admin-trading "bash scripts/tmux/sessions/screeners.sh"
    remote_run admin-trading "bash scripts/tmux/sessions/desk-pro.sh"
    remote_run admin-trading "bash scripts/tmux/sessions/trading-pipeline.sh"
    remote_run admin-trading "bash scripts/tmux/sessions/market-data.sh"
    remote_run admin-trading "bash scripts/tmux/sessions/apps-connectors.sh"
elif [ "$MODE" = "--dry-run" ]; then
    remote_run admin-trading "bash scripts/tmux/sessions/screeners.sh"
    remote_run admin-trading "bash scripts/tmux/sessions/desk-pro.sh"
fi

echo ""

# ── Health check ──────────────────────────────────────────────────────────
if [ "$MODE" != "--dry-run" ]; then
    echo "--- health check ---"
    sleep 1
    python3 "$SCRIPT_DIR/health_check.py"
    echo ""
    echo "--- admin-trading sessions ---"
    ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading \
        "tmux ls 2>/dev/null || echo 'no sessions'" || true
fi

echo ""
echo "=== Fleet tmux Start done ($MODE) ==="
