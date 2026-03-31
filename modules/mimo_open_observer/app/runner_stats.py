from __future__ import annotations

import json
import sys
from pathlib import Path

from .config import load_config, MODULE_DIR
from .event_journal import read_jsonl
from .stats_builder import build_stats, write_reports


def run_build_stats() -> int:
    config = load_config()
    enriched_path = MODULE_DIR / config["paths"]["enriched_events"]
    reports_dir = MODULE_DIR / config["paths"]["reports_dir"]

    events = read_jsonl(str(enriched_path))
    if not events:
        print("  no enriched events found")
        return 1

    stats = build_stats(events)
    write_reports(stats, str(reports_dir))

    s = stats["summary"]
    print(f"  total_windows: {s['total_windows']}")
    print(f"  total_signals: {s['total_signals']}")
    print(f"  signal_rate:   {s['signal_rate']}")
    print(f"  reports_dir:   {reports_dir}")
    return 0


def run_show_stats() -> int:
    config = load_config()
    reports_dir = MODULE_DIR / config["paths"]["reports_dir"]
    summary_path = reports_dir / "stats_summary.json"

    if not summary_path.is_file():
        print("  no stats found (run build_stats first)")
        return 1

    with open(summary_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    print("  === MIMO OPEN OBSERVER — STATS SUMMARY ===")
    for key, val in data.items():
        print(f"  {key}: {val}")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv or argv[0] in ("help", "--help"):
        print("runner_stats: build_stats | show_stats")
        return 0
    if argv[0] == "build_stats":
        return run_build_stats()
    if argv[0] == "show_stats":
        return run_show_stats()
    print(f"unknown subcommand: {argv[0]}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
