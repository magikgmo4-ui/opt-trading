#!/usr/bin/env bash
# analysis_bundles CLI helper
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

CMD="${1:-help}"

case "$CMD" in
  sanity)
    bash "$SCRIPT_DIR/sanity_check.sh"
    ;;
  test)
    python3 -m pytest tests/test_bundle_contracts.py tests/test_verdict_consumer.py tests/test_asset_selector.py -v
    ;;
  validate)
    FILE="${2:-}"
    if [ -z "$FILE" ]; then
      echo "Usage: cmd.sh validate <bundle.json>"
      exit 1
    fi
    python3 -c "
import json, sys
sys.path.insert(0, '.')
from modules.analysis_bundles.app.contract_validator import validate_bundle
data = json.loads(open(sys.argv[1]).read())
errors = validate_bundle(data)
if errors:
    for e in errors:
        print(f'FAIL: {e}')
    sys.exit(1)
else:
    print('PASS: bundle validated')
" "$FILE"
    ;;
  btc)
    python3 -c "
import json, sys
sys.path.insert(0, '.')
from modules.analysis_bundles.app.btc_core_producer import produce_btc_core
bundle = produce_btc_core()
print(json.dumps(bundle.to_dict(), indent=2, default=str))
"
    ;;
  macro)
    python3 -c "
import json, sys
sys.path.insert(0, '.')
from modules.analysis_bundles.app.macro_producer import produce_macro
bundle = produce_macro()
print(json.dumps(bundle.to_dict(), indent=2, default=str))
"
    ;;
  verdict)
    python3 -c "
import json, sys
sys.path.insert(0, '.')
from modules.analysis_bundles.app.btc_core_producer import produce_btc_core
from modules.analysis_bundles.app.macro_producer import produce_macro
from modules.analysis_bundles.app.verdict_consumer import produce_verdict
btc = produce_btc_core()
macro = produce_macro()
verdict = produce_verdict(btc_bundle=btc.to_dict(), macro_bundle=macro.to_dict())
print(json.dumps(verdict.to_dict(), indent=2, default=str))
"
    ;;
  datacenter)
    python3 -c "
import json, sys
sys.path.insert(0, '.')
from modules.analysis_bundles.app.data_center_router import produce_data_center_coverage
coverage = produce_data_center_coverage()
print(json.dumps(coverage, indent=2, default=str))
"
    ;;
  tickets)
    python3 -c "
import json, sys
sys.path.insert(0, '.')
from modules.analysis_bundles.app.asset_selector import produce_summary_by_class
summary = produce_summary_by_class()
print(json.dumps(summary, indent=2, default=str))
"
    ;;
  status)
    python3 -c "
import sys; sys.path.insert(0, '.')
from modules.analysis_bundles.app.schema import BundleOutput
from modules.analysis_bundles.app.contract_validator import validate_bundle
from modules.analysis_bundles.app.verdict_consumer import produce_verdict
from modules.analysis_bundles.app.data_center_router import produce_data_center_coverage
print('analysis_bundles: OK')
print('BundleOutput schema: OK')
print('ContractValidator: OK')
print('VerdictConsumer: OK')
print('DataCenterRouter: OK')
"
    ;;
  help|*)
    echo "Usage: cmd.sh [sanity|test|validate <file>|btc|macro|verdict|datacenter|tickets|status|help]"
    ;;
esac
