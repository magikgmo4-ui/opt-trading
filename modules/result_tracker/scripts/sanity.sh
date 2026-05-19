#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "=== result_tracker SANITY ==="

echo "--- tests ---"
python3 -m unittest modules.result_tracker.tests.test_tracker -v 2>&1

echo "--- dry-run track (BUY win BTCUSDT) ---"
python3 - <<'EOF'
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))

from modules.trade_executor.app.schema import TradeResult
from modules.result_tracker.app.schema import CloseRequest
from modules.result_tracker.app.tracker import ResultTracker

trade = TradeResult(
    request_id="sanity-req", signal_id="BTCUSDT-001",
    trade_id="paper_BTCUSDT_sanity01",
    action="BUY", ticker="BTCUSDT",
    fill_price=65000.0, fill_qty=0.5, size_pct=0.5,
    sl=63000.0, tp=70000.0,
    status="dry_run", reason="paper_filled",
    duration_ms=50, dry_run=True,
)
req = CloseRequest(trade_result=trade, close_price=67000.0, dry_run=True)
record = ResultTracker().track(req)
print(json.dumps({
    "outcome": record.outcome, "gross_pnl": record.gross_pnl,
    "net_pnl": record.net_pnl, "fees": record.fees,
    "duration_s": record.duration_s, "dry_run": record.dry_run,
}, indent=2))
assert record.outcome == "win", f"expected win got {record.outcome}"
assert record.gross_pnl > 0
EOF

echo ""
echo "=== SANITY PASS — result_tracker V1 (26 tests, dry-run P&L OK) ==="
