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

# --- K7 runners ---
k7_files=(
  "$SCRIPT_DIR/app/runner_detect.py"
  "$SCRIPT_DIR/app/runner_sample.py"
  "$SCRIPT_DIR/app/runner_stats.py"
)

for p in "${k7_files[@]}"; do
  [ -f "$p" ] || { echo "FAIL missing K7: $p" >&2; exit 1; }
done

# --- python full pipeline + stats + runners ---
python3 -c "
import sys, tempfile, os, shutil, json
from pathlib import Path
sys.path.insert(0, '$SCRIPT_DIR')
from app.config import load_config, MODULE_DIR as ORIG_MODULE_DIR
from app.models import Bar, RawEvent, EnrichedEvent
from app.data_provider import get_m1_bars, get_price_at, FIXTURES_DIR
from app.utils_time import is_active_weekday, build_window_ts, add_minutes
from app.window_detector import detect_window, find_first_fvg, compute_sweep
from app.event_journal import ensure_parent_dir, read_jsonl, existing_ids, append_raw_event, append_enriched_event, tail_jsonl
from app.outcome_sampler import compute_outcome, enrich_event, sample_pending
from app.stats_builder import build_stats, write_reports
from app.runner_detect import run_detect_once, run_detect_range
from app.runner_sample import run_sample_pending
from app.runner_stats import run_build_stats, run_show_stats
from datetime import datetime
from zoneinfo import ZoneInfo

cfg = load_config()
assert cfg['symbol'] == 'XAUUSD'

# K6 stats test
events = [
    {'event_id': 's1', 'fvg_detected': False, 'weekday': 'Sunday'},
    {'event_id': 's2', 'fvg_detected': True, 'fvg_direction': 'bullish',
     'sweep': False, 'weekday': 'Sunday',
     'outcome_30m': 'win', 'delta_30m': 5.0},
]
stats = build_stats(events)
assert stats['summary']['total_windows'] == 2

# K7 runners: patch data to tmpdir
tmpdir = Path(tempfile.mkdtemp())
import app.config
app.config.MODULE_DIR = tmpdir
import app.runner_detect as rd, app.runner_sample as rs, app.runner_stats as rst
rd.MODULE_DIR = tmpdir; rs.MODULE_DIR = tmpdir; rst.MODULE_DIR = tmpdir

# detect_range
run_detect_range()

# sample_pending
run_sample_pending()

# build_stats + show_stats
run_build_stats()
run_show_stats()

# cleanup
shutil.rmtree(str(tmpdir))
print('PASS: K1..K7 full pipeline OK')
" || { echo "FAIL: python sanity" >&2; exit 1; }

# --- cmd.sh / menu.sh existence ---
[ -f "$SCRIPT_DIR/cmd.sh" ] || { echo "FAIL missing: cmd.sh" >&2; exit 1; }
[ -f "$SCRIPT_DIR/menu.sh" ] || { echo "FAIL missing: menu.sh" >&2; exit 1; }

echo "PASS: mimo_open_observer K7 sanity OK"
