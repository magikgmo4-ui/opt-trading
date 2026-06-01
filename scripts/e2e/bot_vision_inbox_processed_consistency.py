#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _safe_load_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def build_report(inbox: Path, processed: Path) -> dict[str, Any]:
    inbox_json = sorted(inbox.glob("screen_*.json")) if inbox.exists() else []
    inbox_png = sorted(inbox.glob("screen_*.png")) if inbox.exists() else []
    processed_png = sorted(processed.glob("screen_*.png")) if processed.exists() else []

    inbox_png_names = {p.name for p in inbox_png}
    processed_png_names = {p.name for p in processed_png}
    matched_inbox = 0
    matched_processed = 0
    missing_png = 0
    blocked_or_invalid_without_png = 0
    malformed_json = 0
    orphan_examples: list[str] = []

    for sidecar in inbox_json:
        data = _safe_load_json(sidecar)
        png_name = sidecar.with_suffix(".png").name
        if data is None:
            malformed_json += 1
            orphan_examples.append(sidecar.name)
            continue

        if png_name in inbox_png_names:
            matched_inbox += 1
            continue
        if png_name in processed_png_names:
            matched_processed += 1
            continue

        missing_png += 1
        if data.get("status") in {"blocked", "invalid_visual"}:
            blocked_or_invalid_without_png += 1
        if len(orphan_examples) < 10:
            orphan_examples.append(sidecar.name)

    referenced_png_names = {p.with_suffix(".png").name for p in inbox_json}
    inbox_png_without_json = sorted(p.name for p in inbox_png if p.name not in referenced_png_names)
    processed_png_without_json = sorted(p.name for p in processed_png if p.name not in referenced_png_names)

    orphan_json = max(0, missing_png - blocked_or_invalid_without_png - malformed_json)
    overall_status = "PASS"
    if malformed_json > 0 or orphan_json > 0:
        overall_status = "FAIL"
    elif missing_png > 0 or inbox_png_without_json or processed_png_without_json:
        overall_status = "WARN"

    return {
        "pipeline": "bot_vision_inbox_processed_consistency",
        "ts": _utc_now_iso(),
        "overall_status": overall_status,
        "paths": {
            "vision_inbox": str(inbox),
            "vision_processed": str(processed),
        },
        "counts": {
            "inbox_json": len(inbox_json),
            "inbox_png": len(inbox_png),
            "processed_png": len(processed_png),
            "json_with_png_in_inbox": matched_inbox,
            "json_with_png_in_processed": matched_processed,
            "json_missing_png_anywhere": missing_png,
            "blocked_or_invalid_without_png": blocked_or_invalid_without_png,
            "malformed_json": malformed_json,
            "true_orphan_json": orphan_json,
            "inbox_png_without_json": len(inbox_png_without_json),
            "processed_png_without_json": len(processed_png_without_json),
        },
        "examples": {
            "orphan_json": orphan_examples,
            "inbox_png_without_json": inbox_png_without_json[:10],
            "processed_png_without_json": processed_png_without_json[:10],
        },
        "interpretation": {
            "normal_flow": "JSON may remain in vision_inbox while PNG is moved to vision_processed.",
            "warn_condition": "Missing PNG can still be expected for blocked/invalid captures.",
            "fail_condition": "Malformed sidecars or true orphan JSON without PNG anywhere and not blocked/invalid_visual.",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Check bot-vision inbox/processed flow consistency")
    ap.add_argument("--inbox", default="/srv/sftp/shared_files/shared/vision_inbox")
    ap.add_argument("--processed", default="/srv/sftp/shared_files/shared/vision_processed")
    args = ap.parse_args()

    report = build_report(Path(args.inbox), Path(args.processed))
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["overall_status"] == "PASS" else 1 if report["overall_status"] == "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
