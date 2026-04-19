from __future__ import annotations

import argparse
import json
from pathlib import Path

from .service import audit_campaign_integrity, load_spec, run_campaign


def main() -> int:
    parser = argparse.ArgumentParser(prog="kil_v1", add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("spec_path")
    run_parser.add_argument("--workspace", required=True)

    sample_parser = subparsers.add_parser("sample")
    sample_parser.add_argument("--workspace", required=True)

    audit_parser = subparsers.add_parser("audit")
    audit_parser.add_argument("workspace")
    audit_parser.add_argument("campaign_id")

    subparsers.add_parser("help")

    args = parser.parse_args()
    if args.command in {None, "help"}:
        _print_help()
        return 0

    if args.command == "run":
        spec = load_spec(Path(args.spec_path))
        result = run_campaign(spec, Path(args.workspace))
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 0

    if args.command == "sample":
        module_root = Path(__file__).resolve().parents[2]
        spec = load_spec(module_root / "examples" / "sample_campaign.json")
        result = run_campaign(spec, Path(args.workspace))
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 0

    if args.command == "audit":
        result = audit_campaign_integrity(Path(args.workspace), args.campaign_id)
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 0 if result["ok"] else 1

    _print_help()
    return 1


def _print_help() -> None:
    print("Usage:")
    print("  kil_v1 run <spec_path> --workspace <path>")
    print("  kil_v1 sample --workspace <path>")
    print("  kil_v1 audit <workspace> <campaign_id>")
    print("  kil_v1 help")


if __name__ == "__main__":
    raise SystemExit(main())
