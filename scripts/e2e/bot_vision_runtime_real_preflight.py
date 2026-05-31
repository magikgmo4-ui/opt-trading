#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
HEADLESS_DIR = REPO_ROOT / "modules" / "bot_vision" / "headless_capture"
STEP2_APP = REPO_ROOT / "modules" / "bot_vision_step2" / "app" / "bot_vision_step2.py"
STEP2_ENV_EXAMPLE = REPO_ROOT / "modules" / "bot_vision_step2" / "config" / "bot_vision.env.example"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def _run_ok(command: list[str], workdir: Path | None = None, timeout: int = 20) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(workdir) if workdir else None,
        )
    except Exception as exc:
        return False, str(exc)
    text = (result.stdout or result.stderr or "").strip()
    return result.returncode == 0, text[:300]


def build_report() -> dict[str, Any]:
    node_path = shutil.which("node")
    npm_path = shutil.which("npm")
    node_modules_playwright = HEADLESS_DIR / "node_modules" / "playwright"

    node_ok, node_out = _run_ok(["node", "--version"]) if node_path else (False, "node missing")
    npm_ok, npm_out = _run_ok(["npm", "--version"]) if npm_path else (False, "npm missing")
    npm_check_ok, npm_check_out = (
        _run_ok(["npm", "run", "check"], workdir=HEADLESS_DIR)
        if npm_path and (HEADLESS_DIR / "package.json").exists() and node_modules_playwright.exists()
        else (False, "playwright dependencies not installed")
    )

    checks = {
        "node": {"ok": bool(node_path and node_ok), "detail": node_out if node_path else "node missing"},
        "npm": {"ok": bool(npm_path and npm_ok), "detail": npm_out if npm_path else "npm missing"},
        "playwright_node_modules": {"ok": node_modules_playwright.exists(), "detail": str(node_modules_playwright)},
        "playwright_runtime_check": {"ok": npm_check_ok, "detail": npm_check_out},
        "python_pillow": {"ok": _module_available("PIL"), "detail": "PIL import"},
        "python_openai": {"ok": _module_available("openai"), "detail": "openai import"},
        "python_pytesseract": {"ok": _module_available("pytesseract"), "detail": "pytesseract import"},
        "env_openai_api_key": {"ok": bool(os.environ.get("OPENAI_API_KEY")), "detail": "OPENAI_API_KEY present" if os.environ.get("OPENAI_API_KEY") else "OPENAI_API_KEY missing"},
        "env_telegram_bot_token": {"ok": bool(os.environ.get("TELEGRAM_BOT_TOKEN")), "detail": "TELEGRAM_BOT_TOKEN present" if os.environ.get("TELEGRAM_BOT_TOKEN") else "TELEGRAM_BOT_TOKEN missing"},
        "env_telegram_chat_id": {"ok": bool(os.environ.get("TELEGRAM_CHAT_ID")), "detail": "TELEGRAM_CHAT_ID present" if os.environ.get("TELEGRAM_CHAT_ID") else "TELEGRAM_CHAT_ID missing"},
        "step2_app": {"ok": STEP2_APP.exists(), "detail": str(STEP2_APP)},
        "step2_env_example": {"ok": STEP2_ENV_EXAMPLE.exists(), "detail": str(STEP2_ENV_EXAMPLE)},
        "profiles_present": {"ok": any(HEADLESS_DIR.glob("profiles*.json")), "detail": "profiles*.json present"},
        "capture_script": {"ok": (HEADLESS_DIR / "capture_headless.js").exists(), "detail": str(HEADLESS_DIR / "capture_headless.js")},
        "pipeline_script": {"ok": (HEADLESS_DIR / "scripts" / "run_vision_pipeline.py").exists(), "detail": str(HEADLESS_DIR / "scripts" / "run_vision_pipeline.py")},
    }

    capture_ready = all(checks[key]["ok"] for key in ["node", "npm", "playwright_node_modules", "playwright_runtime_check", "capture_script"])  # type: ignore[index]
    analysis_ready = all(checks[key]["ok"] for key in ["python_pillow", "python_openai", "env_openai_api_key", "step2_app"])  # type: ignore[index]
    telegram_ready = all(checks[key]["ok"] for key in ["env_telegram_bot_token", "env_telegram_chat_id"])  # type: ignore[index]
    coinglass_real_ready = all(checks[key]["ok"] for key in ["python_pillow", "python_pytesseract"])  # type: ignore[index]

    blockers: list[str] = []
    if not capture_ready:
        blockers.append("real_capture_not_ready")
    if not analysis_ready:
        blockers.append("real_analysis_not_ready")
    if not telegram_ready:
        blockers.append("telegram_dispatch_not_ready")
    if not coinglass_real_ready:
        blockers.append("coinglass_real_ocr_not_ready")

    if capture_ready and analysis_ready and telegram_ready:
        max_stage = "full_runtime_ready"
        overall_status = "ready"
    elif capture_ready and analysis_ready:
        max_stage = "publish_validate_ready_telegram_blocked"
        overall_status = "blocked"
    elif capture_ready:
        max_stage = "capture_ready_analysis_blocked"
        overall_status = "blocked"
    else:
        max_stage = "preflight_only"
        overall_status = "blocked"

    return {
        "pipeline": "bot_vision_runtime_real_preflight",
        "ts": _utc_now_iso(),
        "overall_status": overall_status,
        "max_provable_stage": max_stage,
        "checks": checks,
        "blockers": blockers,
        "recommended_commands": [
            "cd modules/bot_vision/headless_capture && npm install && npx playwright install chromium",
            "source venv/bin/activate && pip install pillow openai pytesseract",
            "cp modules/bot_vision_step2/config/bot_vision.env.example /opt/trading/modules/bot_vision_step2/config/bot_vision.env",
            "export OPENAI_API_KEY=... TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=...",
        ],
    }


def main() -> int:
    report = build_report()
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["overall_status"] == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
