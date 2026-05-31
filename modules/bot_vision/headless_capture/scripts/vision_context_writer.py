#!/usr/bin/env python3
"""
vision_context_writer — publishes vision_context.coinglass.v1
to DeskPro and Data Center consumer paths.

Usage:
  python3 scripts/vision_context_writer.py --input /path/to/vision_context.json
  python3 scripts/vision_context_writer.py --stdin                      # pipe from coinglass_ocr_analyzer
  python3 scripts/vision_context_writer.py --dry-run

Output:
  DeskPro  → data/deskpro/inputs/vision_context/coinglass/latest.json
  Data Center → data/data_center/views/vision_context/coinglass/latest.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]

DESKPRO_VISION_CONTEXT_DIR = REPO_ROOT / "data" / "deskpro" / "inputs" / "vision_context" / "coinglass"
DESKPRO_VISION_CONTEXT_PATH = DESKPRO_VISION_CONTEXT_DIR / "latest.json"

DC_VISION_CONTEXT_DIR = REPO_ROOT / "data" / "data_center" / "views" / "vision_context" / "coinglass"
DC_VISION_CONTEXT_HISTORY = DC_VISION_CONTEXT_DIR / "history"


def write_deskpro(data: dict[str, Any]) -> Path:
    DESKPRO_VISION_CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = DESKPRO_VISION_CONTEXT_PATH.with_suffix(".json.uploading")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, DESKPRO_VISION_CONTEXT_PATH)
    print(f"OK: DeskPro <- {DESKPRO_VISION_CONTEXT_PATH}")
    return DESKPRO_VISION_CONTEXT_PATH


def write_data_center(data: dict[str, Any]) -> Path:
    DC_VISION_CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
    DC_VISION_CONTEXT_HISTORY.mkdir(parents=True, exist_ok=True)

    path = DC_VISION_CONTEXT_DIR / "latest.json"
    tmp = path.with_suffix(".json.uploading")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)
    print(f"OK: DataCenter <- {path}")

    symbol = data.get("symbol", "UNKNOWN")
    ts = data.get("analysis_ts", datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
    history_path = DC_VISION_CONTEXT_HISTORY / f"{symbol}_{ts}.json"
    history_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK: DataCenter <- {history_path}")

    return path


def validate(data: dict[str, Any]) -> bool:
    if data.get("input_class") != "vision_context.coinglass.v1":
        print(f"ERROR: invalid input_class '{data.get('input_class')}'", file=sys.stderr)
        return False
    if not data.get("detections"):
        print("WARN: empty detections array", file=sys.stderr)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Publish vision_context.coinglass.v1 to DeskPro and Data Center")
    ap.add_argument("--input", help="Path to vision_context JSON file")
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
    print(f"OK: published {len(data.get('detections', []))} detections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
