"""Command line entrypoint for the static OpenClaw MCP policy validator."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .validator import validate_policy_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openclaw-mcp-policy-validator",
        description="Static read-only validation for OpenClaw MCP policy drafts.",
    )
    parser.add_argument("policy_file", help="Local policy YAML draft or test file to validate.")
    parser.add_argument(
        "--capability",
        help="Optional capability id to check against deny-by-default behavior.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format. JSON is deterministic and intended for tests.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    path = Path(args.policy_file)
    report = validate_policy_file(path, requested_capability=args.capability)
    if args.format == "json":
        print(report.to_json())
    else:
        print(f"verdict={report.verdict}")
        for error in report.errors:
            print(f"error={error.error_code} path={error.path} message={error.message}")
    sys.stdout.flush()
    return report.exit_code
