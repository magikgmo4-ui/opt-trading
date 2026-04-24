from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.rules import load_rules
from app.scanner import scan_repo
from app.report import write_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="naming_normalizer",
        description="Audit-only naming normalizer for opt-trading.",
    )
    sub = parser.add_subparsers(dest="command")

    help_cmd = sub.add_parser("help", help="Show help")
    help_cmd.set_defaults(command="help")

    sub.add_parser("explain-rules", help="Print loaded rules")

    audit_cmd = sub.add_parser("audit", help="Audit a repo root")
    audit_cmd.add_argument("repo_root", help="Path to the git repo root")
    audit_cmd.add_argument("--output-dir", default=None, help="Directory for markdown/json reports")
    audit_cmd.add_argument("--print-json", action="store_true", help="Also print findings as JSON")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    module_root = script_dir.parent
    config_dir = module_root / "config"

    if args.command in {None, "help"}:
        parser.print_help()
        print("\nUsage:")
        print("  cmd.sh explain-rules")
        print("  cmd.sh audit /path/to/repo [--output-dir DIR]")
        return 0

    surfaces, exceptions = load_rules(config_dir)

    if args.command == "explain-rules":
        payload = {
            "Surfaces": [
                {
                    "name": item.name,
                    "selector": item.selector,
                    "root": item.root,
                    "entry_kind": item.entry_kind,
                    "patterns": list(item.patterns),
                    "proposal_style": item.proposal_style,
                    "description": item.description,
                }
                for item in surfaces
            ],
            "Exceptions": exceptions,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    if args.command == "audit":
        repo_root = Path(args.repo_root).resolve()
        output_dir = Path(args.output_dir).resolve() if args.output_dir else module_root / "output"
        findings = scan_repo(repo_root, surfaces, exceptions)
        md_path, json_path = write_reports(findings, output_dir)
        print(f"Repo root: {repo_root}")
        print(f"Findings : {len(findings)}")
        print(f"Markdown : {md_path}")
        print(f"JSON     : {json_path}")
        if args.print_json:
            print(json.dumps([item.__dict__ for item in findings], indent=2, ensure_ascii=False))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
