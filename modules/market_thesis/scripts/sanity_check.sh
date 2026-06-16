#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*" >&2; exit 1; }

echo "MODULE=market_thesis"
echo "SANITY_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

python3 --version >/dev/null 2>&1 || fail "python3 not found"
pass "python3 available"

for f in models.py README.md __init__.py scripts/cmd.sh config.py source_status.py source_readers.py context_aggregator.py context_builder.py narrative.py builders/__init__.py builders/technique_builder.py builders/flows_builder.py builders/news_builder.py builders/risks_builder.py builders/probabilities_builder.py; do
  [ -f "$BASE/$f" ] || fail "missing: $f"
done
pass "module structure complete"

python3 -c "from modules.market_thesis.models import MarketThesis" 2>/dev/null \
  || (cd "$BASE/../.." && python3 -c "from modules.market_thesis.models import MarketThesis") \
  || fail "models import FAIL"
pass "models import PASS"

python3 -c "
from modules.market_thesis.models import CANONICAL_BTC_THESIS
t = CANONICAL_BTC_THESIS
assert t.symbol == 'BTC'
assert t.metadata.contract == 'market_thesis.v1'
assert t.action.readiness == 'monitor_only'
assert 0 <= t.confidence <= 100
assert t.probabilities.bull + t.probabilities.range + t.probabilities.bear == 100
" 2>/dev/null || fail "canonical fixture FAIL"
pass "canonical fixture PASS"

python3 -c "
import json
from pathlib import Path
import jsonschema
schema_path = Path('$BASE/../..') / 'schemas' / 'market_thesis_v1.json'
schema = json.loads(schema_path.read_text())
jsonschema.Draft202012Validator.check_schema(schema)
" 2>/dev/null || fail "json schema validation FAIL"
pass "json schema validation PASS"

cd "$BASE/../.."
python3 -m pytest tests/market_thesis -q 2>/dev/null || fail "unit tests FAIL"
pass "unit tests PASS"

echo ""
echo "SANITY=PASS"
echo "SANITY_END=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
