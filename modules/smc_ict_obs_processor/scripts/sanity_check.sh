#!/usr/bin/env bash
# Sanity check — smc_ict_obs_processor
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$REPO_ROOT"

echo "[sanity] smc_ict_obs_processor"

python3 -c "from modules.smc_ict_obs_processor.app.smc_ict_obs_processor import score_confidence, build_obs_event; print('[OK] import')"

python3 -c "
from modules.smc_ict_obs_processor.app.smc_ict_obs_processor import build_obs_event
ev = build_obs_event({'choch_observed': True}, 'LONG_WATCH', 'close_below_swing', symbol='BTCUSDT')
assert ev['strategy']['strategy_id'] == 'SMC_ICT_CHOCH_BOS_RETEST'
print('[OK] build_obs_event')
"

echo "[PASS] sanity_check smc_ict_obs_processor"
