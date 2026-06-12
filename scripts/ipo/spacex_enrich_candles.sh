#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT"
source venv/bin/activate 2>/dev/null || true

echo "=== SpaceX Candle Enrichment ==="
python3 -m modules.ipo_tracking.cli collect-once --offline > /dev/null
python3 -m modules.ipo_tracking.cli enrich | python3 -c "
import json,sys
d=json.load(sys.stdin)
ok = (
    d.get('schema') == 'spacex_enriched_candle.v1'
    and d['candle']['symbol'] == 'SPCX'
    and d['candle']['close'] is not None
    and len(d.get('indicators',{})) >= 20
    and 'smc_score' in d.get('smart_money',{})
    and d['consensus'].get('consensus_price') is not None
    and len(d.get('scores',{})) >= 8
)
if ok:
    print('SPACEX_ENRICH_OK')
else:
    print('SPACEX_ENRICH_FAIL')
    sys.exit(1)
"
