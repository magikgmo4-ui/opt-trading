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

# --- K5 outcome sampler ---
k5_files=(
  "$SCRIPT_DIR/app/outcome_sampler.py"
)

for p in "${k5_files[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing K5: $p" >&2; exit 1; }
done

# --- K6 stats builder ---
k6_files=(
  "$SCRIPT_DIR/app/stats_builder.py"
)

for p in "${k6_files[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing K6: $p" >&2; exit 1; }
done

# --- python full pipeline + stats ---
python3 -c "
import sys, tempfile, os, shutil, json
sys.path.insert(0, '$SCRIPT_DIR')
from app.config import load_config
from app.models import Bar, RawEvent, EnrichedEvent
from app.data_provider import get_m1_bars, get_price_at
from app.utils_time import is_active_weekday, build_window_ts, add_minutes
from app.window_detector import detect_window, find_first_fvg, compute_sweep
from app.event_journal import ensure_parent_dir, read_jsonl, existing_ids, append_raw_event, append_enriched_event, tail_jsonl
from app.outcome_sampler import compute_outcome, enrich_event, sample_pending
from app.stats_builder import build_stats, write_reports
from datetime import datetime
from zoneinfo import ZoneInfo

cfg = load_config()
assert cfg['symbol'] == 'XAUUSD'

tz = ZoneInfo('America/Montreal')
cfg_base = {'scope': {'type': 'M1x5', 'bars': 5},
            'windows': {'open_1800': {'type': 'OPEN_1800'}},
            'timezone': 'America/Montreal'}

# build enriched test data
tmpdir = tempfile.mkdtemp()
events = [
    {'event_id': 't1', 'fvg_detected': False, 'weekday': 'Sunday'},
    {'event_id': 't2', 'fvg_detected': True, 'fvg_direction': 'bullish',
     'sweep': False, 'weekday': 'Sunday',
     'outcome_30m': 'win', 'delta_30m': 5.0},
    {'event_id': 't3', 'fvg_detected': True, 'fvg_direction': 'bearish',
     'sweep': True, 'weekday': 'Monday',
     'outcome_30m': 'win', 'delta_30m': 8.0,
     'outcome_60m': 'win', 'delta_60m': 12.0},
]

stats = build_stats(events)
assert stats['summary']['total_windows'] == 3
assert stats['summary']['total_signals'] == 2
assert stats['summary']['total_no_event'] == 1
assert stats['summary']['signal_rate'] == round(2/3, 4)
assert 'bullish' in stats['by_direction']
assert 'sweep_true' in stats['by_sweep']
assert 'Sunday' in stats['by_weekday']

reports_dir = os.path.join(tmpdir, 'reports')
write_reports(stats, reports_dir)
files = sorted(os.listdir(reports_dir))
assert 'stats_summary.json' in files
assert 'stats_by_direction.json' in files
assert 'stats_by_sweep.json' in files
assert 'stats_by_weekday.json' in files

shutil.rmtree(tmpdir)
print('PASS: K1..K6 full pipeline OK')
" || { echo "FAIL: python sanity" >&2; exit 1; }

echo "PASS: mimo_open_observer K6 sanity OK"
