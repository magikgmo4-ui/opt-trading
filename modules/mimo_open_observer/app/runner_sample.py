from __future__ import annotations

import sys

from .config import load_config, MODULE_DIR
from .outcome_sampler import sample_pending


def run_sample_pending() -> int:
    config = load_config()
    raw_path = str(MODULE_DIR / config["paths"]["raw_events"])
    enriched_path = str(MODULE_DIR / config["paths"]["enriched_events"])

    result = sample_pending(raw_path, enriched_path, config)

    print(f"  processed: {result['processed']}")
    print(f"  appended:  {result['appended']}")
    print(f"  skipped:   {result['skipped']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv or argv[0] in ("help", "--help"):
        print("runner_sample: sample_pending")
        return 0
    if argv[0] == "sample_pending":
        return run_sample_pending()
    print(f"unknown subcommand: {argv[0]}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
