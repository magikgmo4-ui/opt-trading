#!/usr/bin/env python3
"""Backtest stats from signal journal.

Usage:
  python3 scripts/ai/workers/signal_stats.py [--journal data/signals/journal/]
"""

import argparse
import json
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def load_journal(journal_dir: Path):
    events = []
    for f in sorted(journal_dir.glob("*.jsonl")):
        with open(f) as fh:
            for line in fh:
                if line.strip():
                    events.append(json.loads(line))
    return events


def compute_stats(events):
    if not events:
        return {"total_signals": 0, "note": "no signals in journal"}

    total = len(events)
    confirmed = sum(1 for e in events if e["cross_validation"]["status"] == "confirmed")
    rejected = sum(1 for e in events if e["journal"]["status"] == "rejected")
    pending = sum(1 for e in events if e["cross_validation"]["status"] == "pending")
    blocked = sum(1 for e in events if e["dry_run"].get("order_blocked", False))

    sources = Counter(e["source"] for e in events)
    symbols = Counter(e["payload"]["symbol"] for e in events)

    return {
        "total_signals": total,
        "confirmed": confirmed,
        "confirmation_rate": round(confirmed / total * 100, 1) if total else 0,
        "rejected": rejected,
        "rejection_rate": round(rejected / total * 100, 1) if total else 0,
        "pending": pending,
        "orders_blocked": blocked,
        "top_sources": sources.most_common(5),
        "top_symbols": symbols.most_common(5),
        "avg_processing_ms": round(
            sum(e["journal"]["processing_time_ms"] for e in events) / total
        ) if total else 0,
    }


def main():
    parser = argparse.ArgumentParser(description="Signal backtest stats")
    parser.add_argument("--journal", default=None)
    args = parser.parse_args()

    journal_dir = Path(args.journal) if args.journal else REPO_ROOT / "data" / "signals" / "journal"
    if not journal_dir.exists():
        print(json.dumps({"error": f"journal dir not found: {journal_dir}"}, indent=2))
        return

    events = load_journal(journal_dir)
    stats = compute_stats(events)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
