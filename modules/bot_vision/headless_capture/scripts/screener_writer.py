#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]

DESKPRO_SCREENER_DIR = REPO_ROOT / "data" / "deskpro" / "inputs" / "vision_context" / "screener"
DESKPRO_SCREENER_PATH = DESKPRO_SCREENER_DIR / "latest.json"

DC_SCREENER_DIR = REPO_ROOT / "data" / "data_center" / "views" / "vision_context" / "screener"
DC_SCREENER_HISTORY = DC_SCREENER_DIR / "history"


def write_deskpro(data: dict[str, Any]) -> Path:
    DESKPRO_SCREENER_DIR.mkdir(parents=True, exist_ok=True)
    tmp = DESKPRO_SCREENER_PATH.with_suffix(".json.uploading")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, DESKPRO_SCREENER_PATH)
    print(f"OK: DeskPro <- {DESKPRO_SCREENER_PATH}")
    return DESKPRO_SCREENER_PATH


def write_data_center(data: dict[str, Any]) -> Path:
    DC_SCREENER_DIR.mkdir(parents=True, exist_ok=True)
    DC_SCREENER_HISTORY.mkdir(parents=True, exist_ok=True)

    path = DC_SCREENER_DIR / "latest.json"
    tmp = path.with_suffix(".json.uploading")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)
    print(f"OK: DataCenter <- {path}")

    symbol = data.get("screener_symbol", "UNKNOWN")
    ts = data.get("analysis_ts", datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
    history_path = DC_SCREENER_HISTORY / f"{symbol}_{ts}.json"
    history_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK: DataCenter <- {history_path}")

    return path


def validate(data: dict[str, Any]) -> bool:
    if data.get("input_class") != "vision_context.screener.v1":
        print(f"ERROR: invalid input_class '{data.get('input_class')}'", file=sys.stderr)
        return False
    if not data.get("stocks"):
        print("WARN: empty stocks array", file=sys.stderr)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Publish vision_context.screener.v1 to DeskPro and Data Center")
    ap.add_argument("--input", help="Path to screener context JSON file")
    ap.add_argument("--stdin", action="store_true", help="Read from stdin")
    ap.add_argument("--dry-run", action="store_true", help="Validate only, no write")
    args = ap.parse_args()

    data: dict[str, Any] | None = None
    if args.stdin:
        try:
            data = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            print(f"ERROR: invalid JSON from stdin: {e}", file=sys.stderr)
            return 1
    elif args.input:
        try:
            data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR: cannot read input: {e}", file=sys.stderr)
            return 1
    else:
        print("ERROR: provide --input or --stdin", file=sys.stderr)
        return 1

    if not validate(data):
        return 1

    if args.dry_run:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    write_deskpro(data)
    write_data_center(data)
    print(f"OK: published {data.get('stock_count', 0)} stocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
