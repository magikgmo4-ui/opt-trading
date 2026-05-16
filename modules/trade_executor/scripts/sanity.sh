#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "=== trade_executor SANITY ==="

echo "--- tests ---"
python3 -m unittest modules.trade_executor.tests.test_executor -v 2>&1

echo "--- dry-run full flow (gate APPROVED → BUY BTCUSDT) ---"
python3 - <<'EOF'
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))

from modules.proposition_engine.app.schema import Proposition
from modules.validation_gate.app.schema import GateDecision
from modules.trade_executor.app.schema import TradeRequest
from modules.trade_executor.app.executor import TradeExecutor

prop = Proposition(
    request_id="sanity-req", signal_id="BTCUSDT-001",
    action="BUY", size_pct=0.5,
    entry=65000.0, sl=63000.0, tp=70000.0,
    confidence=0.85, rationale="sanity test",
    engines_context={"ticker": "BTCUSDT"},
    status="ok",
)
gate = GateDecision(
    request_id="sanity-gate", signal_id="BTCUSDT-001",
    verdict="APPROVED", reason="dry_run_simulated_operator",
    risk_status="ALLOW", risk_reason="confidence=0.850 >= 0.8",
    operator_approved=True, dry_run=True,
)
req = TradeRequest(gate_decision=gate, proposition=prop, ticker="BTCUSDT", dry_run=True)
result = TradeExecutor().execute(req)
print(json.dumps({
    "status": result.status, "action": result.action,
    "ticker": result.ticker, "fill_price": result.fill_price,
    "fill_qty": result.fill_qty, "trade_id": result.trade_id,
    "dry_run": result.dry_run, "duration_ms": result.duration_ms,
}, indent=2))
assert result.status == "dry_run", f"expected dry_run got {result.status}"
assert result.fill_price == 65000.0
assert result.trade_id.startswith("paper_")
EOF

echo "--- gate not approved → REJECTED (no execution) ---"
python3 - <<'EOF'
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))

from modules.proposition_engine.app.schema import Proposition
from modules.validation_gate.app.schema import GateDecision
from modules.trade_executor.app.schema import TradeRequest
from modules.trade_executor.app.executor import TradeExecutor

prop = Proposition(
    request_id="sanity-ks", signal_id="ETHUSDT-001",
    action="SELL", size_pct=0.5,
    entry=3000.0, sl=3100.0, tp=2800.0,
    confidence=0.90, rationale="gate block test",
    engines_context={}, status="ok",
)
gate = GateDecision(
    request_id="sanity-gate-hold", signal_id="ETHUSDT-001",
    verdict="HOLD", reason="operator_timeout",
    risk_status="ALLOW", risk_reason="confidence=0.900 >= 0.8",
    operator_approved=None, dry_run=True,
)
req = TradeRequest(gate_decision=gate, proposition=prop, ticker="ETHUSDT", dry_run=True)
result = TradeExecutor().execute(req)
print(json.dumps({"status": result.status, "reason": result.reason}, indent=2))
assert result.status == "rejected"
assert result.fill_price == 0.0
EOF

echo ""
echo "=== SANITY PASS — trade_executor V1 (28 tests, dry-run paper fill OK) ==="
