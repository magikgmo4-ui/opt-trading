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

# --- K3 window detector ---
k3_files=(
  "$SCRIPT_DIR/app/window_detector.py"
)

for p in "${k3_files[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing K3: $p" >&2; exit 1; }
done

# --- K4 event journal ---
k4_files=(
  "$SCRIPT_DIR/app/event_journal.py"
)

for p in "${k4_files[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing K4: $p" >&2; exit 1; }
done

# --- python import + config load + window detection + journal ---
python3 -c "
import sys, tempfile, os, shutil
sys.path.insert(0, '$SCRIPT_DIR')
from app.config import load_config
from app.models import Bar, RawEvent, EnrichedEvent
from app.data_provider import get_m1_bars, get_price_at
from app.utils_time import is_active_weekday, build_window_ts, add_minutes
from app.window_detector import detect_window, find_first_fvg, compute_sweep
from app.event_journal import ensure_parent_dir, read_jsonl, existing_ids, append_raw_event, tail_jsonl
from datetime import datetime
from zoneinfo import ZoneInfo

cfg = load_config()
assert cfg['symbol'] == 'XAUUSD'
assert cfg['scope']['type'] == 'M1x5'

tz = ZoneInfo('America/Montreal')
window_ts = datetime(2026, 3, 29, 18, 0, tzinfo=tz)
end = datetime(2026, 3, 29, 18, 4, tzinfo=tz)
cfg_base = {'scope': {'type': 'M1x5', 'bars': 5},
            'windows': {'open_1800': {'type': 'OPEN_1800'}},
            'timezone': 'America/Montreal'}

# K3 window detection
cfg_b = {**cfg_base, 'provider': {'mode': 'fixture', 'fixture_file': 'fixture_bullish_no_sweep.json'}}
evt_b = detect_window('XAUUSD', window_ts, cfg_b)
assert evt_b.fvg_detected and evt_b.fvg_direction == 'bullish'

# K4 journal: append
tmpdir = tempfile.mkdtemp()
jpath = os.path.join(tmpdir, 'test.jsonl')
assert read_jsonl(jpath) == []
r1 = append_raw_event(evt_b, jpath)
assert r1 == 'appended'
assert len(read_jsonl(jpath)) == 1

# K4 journal: anti-doublon
r2 = append_raw_event(evt_b, jpath)
assert r2 == 'skipped_duplicate'
assert len(read_jsonl(jpath)) == 1

# K4 journal: tail
tail = tail_jsonl(jpath, 5)
assert len(tail) == 1
assert tail[0]['event_id'] == evt_b.event_id

shutil.rmtree(tmpdir)
print('PASS: K1 + K2 + K3 + K4 sanity OK')
" || { echo "FAIL: python sanity" >&2; exit 1; }

echo "PASS: mimo_open_observer K4 sanity OK"
