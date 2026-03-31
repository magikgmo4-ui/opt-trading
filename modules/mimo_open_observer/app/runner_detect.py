from __future__ import annotations

import csv
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from .config import load_config, MODULE_DIR
from .window_detector import detect_window
from .event_journal import append_raw_event, read_jsonl
from .outcome_sampler import sample_pending
from .stats_builder import build_stats, write_reports
from .utils_time import build_window_ts


FIXTURES_DIR = MODULE_DIR / "fixtures"

AVAILABLE_FIXTURES = [
    "fixture_no_event.json",
    "fixture_bullish_no_sweep.json",
    "fixture_bearish_sweep.json",
]


def _first_ts_from_csv(csv_path: Path) -> datetime:
    with open(csv_path, "r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        row = next(reader)
    return datetime.fromisoformat(row["ts_open"])


def _run_one(fixture_name: str, config: dict) -> dict:
    cfg = {**config, "provider": {"mode": "fixture", "fixture_file": fixture_name}}
    tz_name = config.get("timezone", "America/Montreal")
    tz = ZoneInfo(tz_name)
    window_open_ts = build_window_ts(datetime.now(tz), tz_name)

    raw_path = MODULE_DIR / config["paths"]["raw_events"]
    evt = detect_window("XAUUSD", window_open_ts, cfg)
    status = append_raw_event(evt, str(raw_path))

    return {
        "event_id": evt.event_id,
        "fvg_detected": evt.fvg_detected,
        "fvg_direction": evt.fvg_direction if evt.fvg_detected else "-",
        "sweep": evt.sweep if evt.fvg_detected else "-",
        "append_status": status,
    }


def run_detect_once(fixture: str | None = None) -> int:
    config = load_config()
    if fixture is None:
        fixture = AVAILABLE_FIXTURES[0]
    result = _run_one(fixture, config)
    print(f"  event_id:      {result['event_id']}")
    print(f"  fvg_detected:  {result['fvg_detected']}")
    print(f"  fvg_direction: {result['fvg_direction']}")
    print(f"  sweep:         {result['sweep']}")
    print(f"  append_status: {result['append_status']}")
    return 0


def run_detect_range() -> int:
    config = load_config()
    processed = 0
    appended = 0
    skipped = 0

    for fname in AVAILABLE_FIXTURES:
        result = _run_one(fname, config)
        processed += 1
        if result["append_status"] == "appended":
            appended += 1
        else:
            skipped += 1

    print(f"  processed: {processed}")
    print(f"  appended:  {appended}")
    print(f"  skipped:   {skipped}")
    return 0


def run_replay_csv(csv_path: str) -> int:
    config = load_config()

    csv_file = Path(csv_path)
    if not csv_file.is_absolute():
        csv_file = MODULE_DIR / csv_path
    if not csv_file.is_file():
        print(f"  ERROR: file not found: {csv_file}", file=sys.stderr)
        return 1

    window_open_ts = _first_ts_from_csv(csv_file)

    cfg = {**config, "provider": {"mode": "csv_replay", "csv_replay": {"path": str(csv_path)}}}

    raw_path = MODULE_DIR / config["paths"]["raw_events"]
    enriched_path = MODULE_DIR / config["paths"]["enriched_events"]
    reports_dir = MODULE_DIR / config["paths"]["reports_dir"]

    # --- detect ---
    evt = detect_window("XAUUSD", window_open_ts, cfg)
    status = append_raw_event(evt, str(raw_path))

    print(f"  === REPLAY DETECT ===")
    print(f"  csv:             {csv_path}")
    print(f"  window:          {window_open_ts.isoformat()}")
    print(f"  event_id:        {evt.event_id}")
    print(f"  fvg_detected:    {evt.fvg_detected}")
    print(f"  fvg_direction:   {evt.fvg_direction if evt.fvg_detected else '-'}")
    print(f"  sweep:           {evt.sweep if evt.fvg_detected else '-'}")
    print(f"  append_status:   {status}")

    # --- sample ---
    sample_result = sample_pending(str(raw_path), str(enriched_path), cfg)
    print(f"")
    print(f"  === REPLAY SAMPLE ===")
    print(f"  processed:       {sample_result['processed']}")
    print(f"  appended:        {sample_result['appended']}")
    print(f"  skipped:         {sample_result['skipped']}")

    # --- stats ---
    enriched_events = read_jsonl(str(enriched_path))
    if enriched_events:
        stats = build_stats(enriched_events)
        write_reports(stats, str(reports_dir))
        s = stats["summary"]
        print(f"")
        print(f"  === REPLAY STATS ===")
        print(f"  total_windows:   {s['total_windows']}")
        print(f"  total_signals:   {s['total_signals']}")
        print(f"  signal_rate:     {s['signal_rate']}")
        print(f"  winrate_30m:     {s['winrate_30m']}")
        print(f"  winrate_60m:     {s['winrate_60m']}")
        print(f"  reports_dir:     {reports_dir}")
    else:
        print(f"")
        print(f"  === REPLAY STATS ===")
        print(f"  no enriched events")

    return 0


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv or argv[0] in ("help", "--help"):
        print("runner_detect:")
        print("  detect_once [--fixture NAME]")
        print("  detect_range [--fixtures all]")
        print("  replay --csv <file>")
        return 0
    if argv[0] == "detect_once":
        fixture = None
        if "--fixture" in argv:
            idx = argv.index("--fixture")
            if idx + 1 < len(argv):
                fixture = argv[idx + 1]
        return run_detect_once(fixture)
    if argv[0] == "detect_range":
        return run_detect_range()
    if argv[0] == "replay":
        if "--csv" in argv:
            idx = argv.index("--csv")
            if idx + 1 < len(argv):
                return run_replay_csv(argv[idx + 1])
        print("usage: replay --csv <file>", file=sys.stderr)
        return 1
    print(f"unknown subcommand: {argv[0]}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
