from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from modules.env.env import ensure_dirs, load_env

from .run import run_collection, run_sanity, status_as_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="collector_telegram")
    parser.add_argument("--module-dir", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--channel", default=None, help="Single channel alias override")
    parser.add_argument("--limit", type=int, default=100, help="Fetch limit per channel")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("sanity", help="Validate config and runtime requirements")
    subparsers.add_parser("run", help="Run live Telegram collection")
    subparsers.add_parser("status", help="Print outputs/status.json if available")
    return parser


def main(argv: list[str] | None = None) -> int:
    load_env()
    ensure_dirs()
    parser = build_parser()
    args = parser.parse_args(argv)
    module_dir = Path(args.module_dir).resolve()
    try:
        if args.command == "sanity":
            print(json.dumps(run_sanity(module_dir), indent=2))
            return 0
        if args.command == "run":
            print(json.dumps(run_collection(module_dir, channel_alias=args.channel, limit=args.limit), indent=2))
            return 0
        if args.command == "status":
            print(status_as_text(module_dir))
            return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
