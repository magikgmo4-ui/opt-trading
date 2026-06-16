#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

help_msg() {
  cat <<'EOF'
Usage:
  cmd.sh sanity      — run sanity check
  cmd.sh test        — run unit tests
  cmd.sh models      — validate models (import + canonical fixture)
  cmd.sh schema      — validate JSON Schema

Examples:
  cmd.sh sanity
  cmd.sh test
EOF
}

case "${1:-help}" in
  sanity)
    bash "$BASE/scripts/sanity_check.sh"
    ;;
  test)
    cd "$BASE/../.."
    python3 -m pytest tests/market_thesis -q
    ;;
  models)
    cd "$BASE"
    python3 -c "
from modules.market_thesis.models import CANONICAL_BTC_THESIS, MarketThesis, ProbabilitySet, FreshnessStatus, ThesisMetadata
t = CANONICAL_BTC_THESIS
assert t.symbol == 'BTC'
assert t.action.readiness == 'monitor_only'
assert t.probabilities.bull + t.probabilities.range + t.probabilities.bear == 100
print('Models OK')
"
    ;;
  schema)
    cd "$BASE/../.."
    python3 -c "
import json
from pathlib import Path
import jsonschema
schema = json.loads(Path('schemas/market_thesis_v1.json').read_text())
jsonschema.Draft202012Validator.check_schema(schema)
print('Schema OK')
"
    ;;
  help|--help|-h)
    help_msg
    ;;
  *)
    echo "unknown: ${1:-}" >&2; help_msg >&2; exit 1
    ;;
esac
