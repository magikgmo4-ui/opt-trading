#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HEADLESS_REL = Path("modules/bot_vision/headless_capture")
RUNTIME_ITEMS = [
    "capture_headless.js",
    "README.md",
    "package.json",
    "capture_map.json",
    "screen_types.json",
    "trigger_config.json",
    "profiles.btcusdt_poc.json",
    "profiles.capture_map.p1.runtime.json",
    "profiles.coinglass.json",
    "profiles.example.json",
    "profiles.failure.classification.smoke.local.json",
    "profiles.macro_dashboard.json",
    "profiles.production.json",
    "profiles.source.stability.alt.smoke.local.json",
    "profiles.source.stability.smoke.local.json",
    "profiles.supplementary.json",
    "scripts",
    "systemd",
]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ts_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def _copy_item(src: Path, dst: Path) -> None:
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def build_plan(source_root: Path, runtime_root: Path, backup_root: Path) -> dict[str, Any]:
    source_headless = source_root / HEADLESS_REL
    runtime_headless = runtime_root / HEADLESS_REL
    backup_dir = backup_root / f"bot_vision_stabilization_backup_{_ts_slug()}"
    items = []
    for rel_name in RUNTIME_ITEMS:
        src = source_headless / rel_name
        dst = runtime_headless / rel_name
        items.append(
            {
                "relative": rel_name,
                "source": str(src),
                "destination": str(dst),
                "exists_in_source": src.exists(),
                "exists_in_runtime": dst.exists(),
            }
        )

    return {
        "ts": _utc_now_iso(),
        "source_root": str(source_root),
        "runtime_root": str(runtime_root),
        "backup_dir": str(backup_dir),
        "headless_source": str(source_headless),
        "headless_runtime": str(runtime_headless),
        "runtime_items": items,
        "systemd_plan": {
            "service": "/etc/systemd/system/bot-vision-orchestrator.service",
            "timer": "/etc/systemd/system/bot-vision-orchestrator.timer",
            "disable_timer": "bot-vision-headless-capture.timer",
            "enable_timer": "bot-vision-orchestrator.timer",
        },
    }


def apply_plan(source_root: Path, runtime_root: Path, backup_root: Path) -> dict[str, Any]:
    plan = build_plan(source_root, runtime_root, backup_root)
    backup_dir = Path(plan["backup_dir"])
    source_headless = source_root / HEADLESS_REL
    runtime_headless = runtime_root / HEADLESS_REL
    backup_dir.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    backed_up: list[str] = []

    for rel_name in RUNTIME_ITEMS:
        src = source_headless / rel_name
        dst = runtime_headless / rel_name
        if not src.exists():
            continue

        if dst.exists():
            backup_target = backup_dir / rel_name
            _copy_item(dst, backup_target)
            backed_up.append(rel_name)

        _copy_item(src, dst)
        copied.append(rel_name)

    plan["applied"] = True
    plan["copied"] = copied
    plan["backed_up"] = backed_up
    return plan


def main() -> int:
    ap = argparse.ArgumentParser(description="Stabilize mutable bot-vision runtime from a clean canonical checkout")
    ap.add_argument("--source-root", default="/home/ghost/opt-trading-mainline-clean")
    ap.add_argument("--runtime-root", default="/opt/trading")
    ap.add_argument("--backup-root", default="/opt/trading/_ops")
    ap.add_argument("--apply", action="store_true", help="Apply file sync and create backup")
    args = ap.parse_args()

    source_root = Path(args.source_root)
    runtime_root = Path(args.runtime_root)
    backup_root = Path(args.backup_root)

    if args.apply:
        result = apply_plan(source_root, runtime_root, backup_root)
    else:
        result = build_plan(source_root, runtime_root, backup_root)

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
