#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "=== learning_feeder SANITY ==="

echo "--- tests ---"
python3 -m unittest modules.learning_feeder.tests.test_feeder -v 2>&1

echo "--- dry-run feed (win BTCUSDT) ---"
python3 - <<'EOF'
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))

from modules.proposition_engine.app.schema import Proposition
from modules.result_tracker.app.schema import TradeRecord
from modules.learning_feeder.app.schema import FeedRequest
from modules.learning_feeder.app.feeder import LearningFeeder

prop = Proposition(
    request_id="sanity-req", signal_id="BTCUSDT-001",
    action="BUY", size_pct=0.5,
    entry=65000.0, sl=63000.0, tp=70000.0,
    confidence=0.85, rationale="strong breakout above resistance",
    engines_context={}, status="ok",
)
record = TradeRecord(
    trade_id="paper_BTCUSDT_sanity", request_id="sanity-req", signal_id="BTCUSDT-001",
    ticker="BTCUSDT", action="BUY",
    entry_price=65000.0, close_price=67000.0,
    fill_qty=0.5, size_pct=0.5,
    sl=63000.0, tp=70000.0,
    gross_pnl=1000.0, net_pnl=960.4, fees=39.6,
    duration_s=120.0, outcome="win",
    opened_at="2026-05-16T10:00:00+00:00",
    closed_at="2026-05-16T10:02:00+00:00",
    dry_run=True,
)
req = FeedRequest(signal_id="BTCUSDT-001", proposition=prop, trade_record=record, dry_run=True)
result = LearningFeeder().feed(req)
print(json.dumps({
    "bridge_status": result.bridge_status, "brick_stored": result.brick_stored,
    "dry_run": result.dry_run, "duration_ms": result.duration_ms,
    "summary_lines": len(result.summary.splitlines()),
}, indent=2))
assert result.bridge_status == "dry_run"
assert not result.brick_stored
assert "WIN" in result.summary
assert "Positive reinforcement" in result.summary
EOF

echo ""
echo "=== SANITY PASS — learning_feeder V1 (29 tests, dry-run feedback cycle OK) ==="
