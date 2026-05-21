#!/usr/bin/env python3
"""ledger_writer.py — audit ledger for automated actions.

Usage:
  python3 scripts/ai/workers/ledger_writer.py \
      --event-type <type> \
      --actor-id <actor> \
      --surface-id <surface> \
      --action <action> \
      --status <status> \
      [--payload '{...}'] \
      [--trace-id <uuid>] \
      [--handoff-id <uuid>]

Output:
  Appends 1 JSON line to data/runtime_health/ledger/events.jsonl
  Creates the ledger file + archive dir if missing.
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LEDGER_DIR = REPO_ROOT / "data/runtime_health" / "ledger"
ARCHIVE_DIR = LEDGER_DIR / "archive"
MAX_BYTES = 100 * 1024 * 1024  # 100 MB rotation


def _rotate_if_needed(ledger_path: Path):
    if ledger_path.exists() and ledger_path.stat().st_size >= MAX_BYTES:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
        archive_name = f"events_{date_str}.jsonl"
        ledger_path.rename(ARCHIVE_DIR / archive_name)


def write_event(
    event_type: str,
    actor_id: str,
    surface_id: str,
    action: str,
    status: str,
    payload: dict = None,
    trace_id: str = None,
    handoff_id: str = None,
):
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    ledger_path = LEDGER_DIR / "events.jsonl"

    _rotate_if_needed(ledger_path)

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "actor_id": actor_id,
        "surface_id": surface_id,
        "action": action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "payload": payload or {},
        "trace_id": trace_id or str(uuid.uuid4()),
        "handoff_id": handoff_id,
    }

    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    return event


def main():
    parser = argparse.ArgumentParser(description="Ledger writer for automated actions")
    parser.add_argument("--event-type", required=True)
    parser.add_argument("--actor-id", required=True)
    parser.add_argument("--surface-id", required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--status", required=True, choices=["PASS", "FAIL", "BLOCKED", "WARN"])
    parser.add_argument("--payload", default="{}")
    parser.add_argument("--trace-id", default=None)
    parser.add_argument("--handoff-id", default=None)
    args = parser.parse_args()

    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid payload JSON: {e}", file=sys.stderr)
        sys.exit(1)

    event = write_event(
        event_type=args.event_type,
        actor_id=args.actor_id,
        surface_id=args.surface_id,
        action=args.action,
        status=args.status,
        payload=payload,
        trace_id=args.trace_id,
        handoff_id=args.handoff_id,
    )
    print(json.dumps(event, indent=2))


if __name__ == "__main__":
    main()
