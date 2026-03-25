from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from collectors_core import CollectorsCoreError

from .run import run_collection, run_sanity, status_as_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="collector_coingecko")
    parser.add_argument(
        "--module-dir",
        default=str(Path(__file__).resolve().parents[2]),
        help="Path to the collector_coingecko module directory",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("sanity", help="Run config checks and CoinGecko /ping")
    subparsers.add_parser("run", help="Run the oneshot CoinGecko collection")
    subparsers.add_parser("status", help="Print the current status.json if available")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    module_dir = Path(args.module_dir).resolve()

    try:
        if args.command == "sanity":
            result = run_sanity(module_dir)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "run":
            result = run_collection(module_dir)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "status":
            print(status_as_text(module_dir))
            return 0
    except CollectorsCoreError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
