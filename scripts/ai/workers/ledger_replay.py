#!/usr/bin/env python3
"""ledger_replay.py — replay and audit ledger events.

Usage:
  python3 scripts/ai/workers/ledger_replay.py [--status PASS] [--actor strict_worker]
  python3 scripts/ai/workers/ledger_replay.py --replay   # replay all events in order
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER_PATH = REPO_ROOT / "data/runtime_health" / "ledger" / "events.jsonl"


def _load_events():
    if not LEDGER_PATH.exists():
        print("LEDGER: no events found", file=sys.stderr)
        return []
    with open(LEDGER_PATH) as f:
        return [json.loads(line) for line in f if line.strip()]


def filter_events(events, status=None, actor=None, surface=None, event_type=None):
    result = events[:]
    if status:
        result = [e for e in result if e.get("status") == status]
    if actor:
        result = [e for e in result if e.get("actor_id") == actor]
    if surface:
        result = [e for e in result if e.get("surface_id") == surface]
    if event_type:
        result = [e for e in result if e.get("event_type") == event_type]
    return result


def replay_events(events):
    print(f"REPLAY: {len(events)} events")
    for i, e in enumerate(events, 1):
        print(f"  [{i}] {e['timestamp'][:19]} | {e['actor_id']:25s} | {e['action']:20s} | {e['status']}")
    print(f"REPLAY COMPLETE: {len(events)} events replayed in order")


def main():
    parser = argparse.ArgumentParser(description="Ledger replay and audit")
    parser.add_argument("--status", help="Filter by status")
    parser.add_argument("--actor", help="Filter by actor_id")
    parser.add_argument("--surface", help="Filter by surface_id")
    parser.add_argument("--event-type", help="Filter by event_type")
    parser.add_argument("--replay", action="store_true", help="Replay all events in order")
    args = parser.parse_args()

    events = _load_events()
    if not events:
        print("No events in ledger")
        return

    if args.replay:
        replay_events(events)
        return

    filtered = filter_events(events, args.status, args.actor, args.surface, args.event_type)
    for e in filtered:
        print(json.dumps(e, indent=2))

    print(f"\nTotal: {len(filtered)} events (of {len(events)} total)")


if __name__ == "__main__":
    main()
