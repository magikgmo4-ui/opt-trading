#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
echo "=== sanity: analysis_bundles ==="
[ -f "$MODULE_DIR/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }
[ -f "$APP_DIR/__main__.py" ] || { echo "FAIL: __main__.py missing"; exit 1; }
command -v python3 &>/dev/null || { echo "FAIL: python3 not found"; exit 1; }
cd "$ROOT_DIR"
python3 -c "import modules.analysis_bundles.app" 2>&1 || { echo "FAIL: import analysis_bundles failed"; exit 1; }
echo "OK: import analysis_bundles"
python3 -c "
import sys; sys.path.insert(0, '.')
from modules.analysis_bundles.app.contract_validator import validate_bundle
from modules.analysis_bundles.app.schema import BundleOutput
# smoke: validate a minimal valid bundle
b = BundleOutput(
    contract='bundle.test.v1', bundle_id='test.v1',
    produced_at='2026-01-01T00:00:00Z', freshness_state='FRESH',
    assets=['BTC'], inputs={}, analysis={},
    missing_inputs=[], source_refs=[],
)
errors = validate_bundle(b.to_dict())
if errors:
    print('FAIL:', errors)
    sys.exit(1)
print('OK: validate_bundle smoke')
" || { echo "FAIL: validate_bundle smoke failed"; exit 1; }
echo "PASS: analysis_bundles sanity OK"
