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

# --- python full pipeline + stats + runners (K1-K7) ---
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

run_detect_range()
run_sample_pending()
run_build_stats()
run_show_stats()

shutil.rmtree(str(tmpdir))
print('PASS: K1-K7 full pipeline OK')
" || { echo "FAIL: python sanity K1-K7" >&2; exit 1; }

# --- python CSV replay (K8.1) ---
python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from app.data_provider import get_m1_bars, get_price_at
from app.models import Bar
from datetime import datetime
from zoneinfo import ZoneInfo

tz = ZoneInfo('America/Montreal')

# fixture mode still works
fix_cfg = {'provider': {'mode': 'fixture', 'fixture_file': 'fixture_no_event.json'}}
bars_fix = get_m1_bars('XAUUSD', datetime(2026, 3, 29, 18, 0, tzinfo=tz), datetime(2026, 3, 29, 18, 4, tzinfo=tz), fix_cfg)
assert len(bars_fix) == 5

# csv_replay mode
csv_cfg = {'provider': {'mode': 'csv_replay', 'csv_replay': {'path': 'fixtures/sample_xauusd_m1.csv'}}}
csv_start = datetime(2026, 3, 22, 18, 0, tzinfo=tz)
csv_end = datetime(2026, 3, 22, 18, 4, tzinfo=tz)
csv_bars = get_m1_bars('XAUUSD', csv_start, csv_end, csv_cfg)
assert len(csv_bars) == 5
assert csv_bars[0].open == 3025.10
csv_price = get_price_at('XAUUSD', csv_start, csv_cfg)
assert csv_price == 3025.90

# full hour
csv_full = get_m1_bars('XAUUSD', csv_start, datetime(2026, 3, 22, 18, 59, tzinfo=tz), csv_cfg)
assert len(csv_full) == 60

# empty range
csv_empty = get_m1_bars('XAUUSD', datetime(2026, 3, 22, 19, 0, tzinfo=tz), datetime(2026, 3, 22, 19, 30, tzinfo=tz), csv_cfg)
assert len(csv_empty) == 0

print('PASS: K8.1 CSV replay OK')
" || { echo "FAIL: python sanity K8.1" >&2; exit 1; }

# --- python replay pipeline (K8.4) ---
python3 -c "
import sys, tempfile, shutil
from pathlib import Path
sys.path.insert(0, '$SCRIPT_DIR')
from app.config import load_config, MODULE_DIR as ORIG_MODULE_DIR
from app.runner_detect import run_replay_csv
from app.event_journal import read_jsonl
from app.stats_builder import build_stats, write_reports

cfg = load_config()

# replay on sample CSV
ret = run_replay_csv('fixtures/sample_xauusd_m1.csv')
assert ret == 0

# verify raw event written
raw_path = ORIG_MODULE_DIR / cfg['paths']['raw_events']
raw_events = read_jsonl(str(raw_path))
assert len(raw_events) >= 1

# verify enriched written
enr_path = ORIG_MODULE_DIR / cfg['paths']['enriched_events']
enr_events = read_jsonl(str(enr_path))
assert len(enr_events) >= 1

# verify stats
reports_dir = ORIG_MODULE_DIR / cfg['paths']['reports_dir']
import os
report_files = os.listdir(str(reports_dir))
assert 'stats_summary.json' in report_files

print('PASS: K8.4 replay pipeline OK')
" || { echo "FAIL: python sanity K8.4" >&2; exit 1; }

# --- K8.1 replay data ---
[ -f "$SCRIPT_DIR/fixtures/sample_xauusd_m1.csv" ] || { echo "FAIL missing: sample CSV" >&2; exit 1; }

# --- K8.2 ccxt provider (soft check, requires network) ---
python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
try:
    import ccxt
    from app.data_provider import get_m1_bars
    from datetime import datetime, timezone

    cfg = {'provider': {'mode': 'ccxt', 'ccxt': {'exchange': 'binance', 'symbol': 'XAUUSDT', 'timeframe': '1m', 'limit': 5}}}
    end = datetime.now(timezone.utc)
    from datetime import timedelta
    start = end - timedelta(minutes=10)
    bars = get_m1_bars('XAUUSD', start, end, cfg)
    assert len(bars) >= 1
    assert bars[0].open > 0
    print(f'ccxt: PASS ({len(bars)} bars, close={bars[-1].close})')
except ImportError:
    print('ccxt: SKIP (not installed)')
except Exception as e:
    print(f'ccxt: WARN ({type(e).__name__}: {e})')
" || echo "ccxt: SKIP (soft check)"

# --- python calendar checks (K8.3) ---
python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from app.utils_time import is_market_open_day, get_enabled_windows, is_market_window, next_market_window
from app.config import load_config
from datetime import datetime
from zoneinfo import ZoneInfo

cfg = load_config()
tz = ZoneInfo('America/Montreal')

# is_market_open_day
assert is_market_open_day(datetime(2026, 3, 29, tzinfo=tz))      # Sunday
assert is_market_open_day(datetime(2026, 4, 2, tzinfo=tz))       # Thursday
assert not is_market_open_day(datetime(2026, 3, 27, tzinfo=tz))  # Friday
assert not is_market_open_day(datetime(2026, 3, 28, tzinfo=tz))  # Saturday

# get_enabled_windows
wins = get_enabled_windows(cfg)
assert len(wins) >= 1
assert wins[0]['name'] == 'open_1800'
assert wins[0]['hour'] == 18

# is_market_window
assert is_market_window(datetime(2026, 3, 29, 18, 0, tzinfo=tz), cfg)     # Sunday 18:00
assert is_market_window(datetime(2026, 3, 30, 18, 0, tzinfo=tz), cfg)     # Monday 18:00
assert not is_market_window(datetime(2026, 3, 27, 18, 0, tzinfo=tz), cfg) # Friday 18:00
assert not is_market_window(datetime(2026, 3, 29, 18, 1, tzinfo=tz), cfg) # Sunday 18:01

# next_market_window
nxt = next_market_window(datetime(2026, 3, 27, 19, 0, tzinfo=tz), cfg)
assert nxt is not None
assert nxt.day == 29 and nxt.hour == 18  # next Sunday 18:00

# check_window subcommand
from app.runner_detect import run_check_window
ret = run_check_window()
assert ret == 0

print('PASS: K8.3 calendar OK')
" || { echo "FAIL: python sanity K8.3" >&2; exit 1; }

# --- cmd.sh / menu.sh existence ---
[ -f "$SCRIPT_DIR/cmd.sh" ] || { echo "FAIL missing: cmd.sh" >&2; exit 1; }
[ -f "$SCRIPT_DIR/menu.sh" ] || { echo "FAIL missing: menu.sh" >&2; exit 1; }

echo "PASS: mimo_open_observer K8.3 sanity OK"
