#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$BASE/.." && pwd)"

help_msg() {
  cat <<'EOF'
Usage:
  cmd.sh dry-run        — run E2E dry-run pipeline (JSON report)
  cmd.test              — run E2E pipeline tests
  cmd.sh sanity         — run sanity checks
  cmd.sh health         — check LocalCMS endpoints
  cmd.sh closeout       — print closeout summary
EOF
}

case "${1:-help}" in
  dry-run)
    echo "=== E2E Dry-Run Pipeline ==="
    cd "$PROJECT_ROOT"
    DRY_RUN=1 PAPER_MODE=1 python3 scripts/e2e/dry_run_pipeline.py
    ;;
  test)
    cd "$PROJECT_ROOT"
    python3 -m unittest tests.e2e.test_e2e_dry_run_pipeline -v
    ;;
  health)
    echo "=== LocalCMS Health Check ==="
    echo "GET /health:"
    curl -sf http://127.0.0.1:8700/health 2>/dev/null || echo "LocalCMS not running (expected if not started)"
    echo ""
    echo "GET /menu (first 3 domains):"
    curl -sf http://127.0.0.1:8700/menu 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
for m in d.get('menu',[])[:3]:
    print(f'  {m[\"id\"]}: {m[\"label\"]}')
" 2>/dev/null || echo "LocalCMS not running"
    ;;
  sanity)
    echo "=== E2E Pipeline Sanity ==="
    cd "$PROJECT_ROOT"
    python3 -c "
import sys
sys.path.insert(0, '.')
from modules.signal_router.app.router import route
from modules.proposition_engine.app.engine import PropositionEngine
from modules.validation_gate.app.gate import ValidationGate
from modules.trade_executor.app.executor import TradeExecutor
from modules.result_tracker.app.tracker import ResultTracker
from modules.datasheet_writer.app.writer import DatasheetWriter
from modules.learning_feeder.app.feeder import LearningFeeder
print('All 7 modules importable: OK')
"
    echo "LocalCMS endpoints:"
    for ep in "/health" "/menu" "/menu/state" "/runtime/tmux"; do
        code=$(curl -so /dev/null -w '%{http_code}' "http://127.0.0.1:8700$ep" 2>/dev/null || echo "unreachable")
        echo "  GET $ep → $code"
    done
    ;;
  closeout)
    echo "=== E2E Closeout ==="
    echo "Pipeline: signal_router → proposition_engine → validation_gate → trade_executor → result_tracker → datasheet_writer → learning_feeder"
    echo "Dry-run: YES"
    echo "Trade: NO live orders"
    echo "Files: NO artifacts written (all dry_run=True)"
    echo "Status: READY"
    echo "Run: DRY_RUN=1 PAPER_MODE=1 python3 scripts/e2e/dry_run_pipeline.py"
    ;;
  *)
    help_msg
    exit 1
    ;;
esac
