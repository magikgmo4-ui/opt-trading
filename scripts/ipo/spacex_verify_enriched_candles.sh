#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT"
source venv/bin/activate 2>/dev/null || true

echo "=== SpaceX Verify Enriched Candles ==="
python3 -c "
from modules.ipo_tracking.enrichment.feature_schema import CANDLE_SCHEMA, ENRICHED_CANDLE_FEATURES
import json

schema = CANDLE_SCHEMA
features = ENRICHED_CANDLE_FEATURES

checks = []
checks.append(('schema_valid', schema.get('\$schema') is not None))
checks.append(('required_fields', len(schema.get('required', [])) >= 5))
checks.append(('feature_count', len(features) >= 40))
checks.append(('candle_base', all(f in features for f in ['open','high','low','close','volume'])))
checks.append(('indicators', all(f in features for f in ['ema_20','rsi_14','macd_line','atr_14','vwap'])))
checks.append(('smart_money', all(f in features for f in ['fvg_bullish','bos','choch','smc_score'])))
checks.append(('consensus', all(f in features for f in ['consensus_price','source_disagreement_score'])))
checks.append(('scores', all(f in features for f in ['momentum_score','trade_ready_score','accumulation_score'])))

ok = all(v for _, v in checks)
for name, val in checks:
    print(f'  {name}: {\"OK\" if val else \"FAIL\"}')

if ok:
    print('SPACEX_VERIFY_ENRICHED_OK')
else:
    print('SPACEX_VERIFY_ENRICHED_FAIL')
    exit(1)
"
