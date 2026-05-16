"""python -m app <event_type> [--dry-run] [key=value ...]"""
from __future__ import annotations
import argparse
import json
import sys
from .dispatcher import NotificationDispatcher
from .events import PipelineEvent, ALL_EVENT_TYPES


def main() -> None:
    parser = argparse.ArgumentParser(description="Notification Dispatcher CLI")
    parser.add_argument("event_type", choices=sorted(ALL_EVENT_TYPES))
    parser.add_argument("--dry-run", action="store_true", default=False)
    parser.add_argument("payload", nargs="*", help="key=value pairs")
    args = parser.parse_args()

    payload: dict = {}
    for kv in args.payload:
        if "=" in kv:
            k, _, v = kv.partition("=")
            payload[k.strip()] = v.strip()

    event = PipelineEvent(event_type=args.event_type, payload=payload)  # type: ignore[arg-type]
    result = NotificationDispatcher().dispatch(event, dry_run=args.dry_run)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
