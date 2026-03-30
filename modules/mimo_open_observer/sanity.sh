#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

# --- doc pack files ---
required=(
  "$SCRIPT_DIR/README.md"
  "$SCRIPT_DIR/docs/00_SESSION_INDEX_MIMO_OPEN_OBSERVER_V0.txt"
  "$SCRIPT_DIR/docs/06_PSEUDOCODE_PACK_MIMO_OPEN_OBSERVER_V0.md"
  "$SCRIPT_DIR/config/mimo_open_observer.yaml"
  "$SCRIPT_DIR/registry_patch/modules_registry.entry.yaml"
  "$SCRIPT_DIR/registry_patch/wrappers_registry.entries.yaml"
)

for p in "${required[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing: $p" >&2; exit 1; }
done

# --- K1 app package ---
k1_files=(
  "$SCRIPT_DIR/app/__init__.py"
  "$SCRIPT_DIR/app/config.py"
  "$SCRIPT_DIR/app/models.py"
)

for p in "${k1_files[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing K1: $p" >&2; exit 1; }
done

# --- K2 data layer ---
k2_files=(
  "$SCRIPT_DIR/app/data_provider.py"
  "$SCRIPT_DIR/app/utils_time.py"
  "$SCRIPT_DIR/fixtures/fixture_no_event.json"
  "$SCRIPT_DIR/fixtures/fixture_bullish_no_sweep.json"
  "$SCRIPT_DIR/fixtures/fixture_bearish_sweep.json"
)

for p in "${k2_files[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing K2: $p" >&2; exit 1; }
done

# --- python import + config load ---
python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from app.config import load_config
from app.models import Bar, RawEvent, EnrichedEvent
from app.data_provider import get_m1_bars, get_price_at
from app.utils_time import is_active_weekday, build_window_ts, add_minutes
from datetime import datetime
from zoneinfo import ZoneInfo

cfg = load_config()
assert cfg['symbol'] == 'XAUUSD'
assert cfg['scope']['type'] == 'M1x5'

tz = ZoneInfo('America/Montreal')
start = datetime(2026, 3, 29, 18, 0, tzinfo=tz)
end = datetime(2026, 3, 29, 18, 4, tzinfo=tz)

# utils_time
assert is_active_weekday(start)
assert not is_active_weekday(datetime(2026, 3, 27, tzinfo=tz))

# data_provider fixture read
cfg_f = {'provider': {'mode': 'fixture', 'fixture_file': 'fixture_no_event.json'}}
bars = get_m1_bars('XAUUSD', start, end, cfg_f)
assert len(bars) == 5
assert isinstance(bars[0], Bar)
price = get_price_at('XAUUSD', start, cfg_f)
assert price is not None

print('PASS: K1 + K2 sanity OK')
" || { echo "FAIL: python sanity" >&2; exit 1; }

echo "PASS: mimo_open_observer K2 sanity OK"
