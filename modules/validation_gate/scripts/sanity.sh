#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "=== validation_gate SANITY ==="

echo "--- tests ---"
python3 -m unittest modules.validation_gate.tests.test_gate -v 2>&1
echo "--- dry-run gate (high confidence → APPROVED) ---"
python3 - <<'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))
from modules.proposition_engine.app.schema import Proposition
from modules.validation_gate.app.schema import GateRequest
from modules.validation_gate.app.gate import ValidationGate
import json

prop = Proposition(
    request_id="sanity-req", signal_id="BTCUSDT-001",
    action="BUY", size_pct=0.5,
    entry=65000.0, sl=63000.0, tp=70000.0,
    confidence=0.85, rationale="sanity test",
    engines_context={"ticker": "BTCUSDT"},
    status="ok",
)
gate = ValidationGate()
req = GateRequest(proposition=prop, ticker="BTCUSDT", dry_run=True)
dec = gate.gate(req)
print(json.dumps({
    "verdict": dec.verdict,
    "reason": dec.reason,
    "risk_status": dec.risk_status,
    "operator_approved": dec.operator_approved,
    "dry_run": dec.dry_run,
    "duration_ms": dec.duration_ms,
}, indent=2))
assert dec.verdict == "APPROVED", f"expected APPROVED got {dec.verdict}"
EOF

echo "--- dry-run gate (kill switch → REJECTED) ---"
TRADING_KILL_SWITCH=1 python3 - <<'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))
from modules.proposition_engine.app.schema import Proposition
from modules.validation_gate.app.schema import GateRequest
from modules.validation_gate.app.gate import ValidationGate
import json

prop = Proposition(
    request_id="sanity-ks", signal_id="ETHUSDT-001",
    action="SELL", size_pct=0.5,
    entry=3000.0, sl=3100.0, tp=2800.0,
    confidence=0.90, rationale="kill switch test",
    engines_context={}, status="ok",
)
gate = ValidationGate()
req = GateRequest(proposition=prop, dry_run=True)
dec = gate.gate(req)
print(json.dumps({"verdict": dec.verdict, "reason": dec.reason}, indent=2))
assert dec.verdict == "REJECTED", f"expected REJECTED got {dec.verdict}"
assert dec.reason == "kill_switch_active"
EOF

echo ""
echo "=== SANITY PASS — validation_gate V1 (30 tests, dry-run gate OK) ==="
