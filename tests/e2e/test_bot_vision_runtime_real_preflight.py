from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_bot_vision_runtime_real_preflight_reports_runtime_state():
    env = {**os.environ}
    env.pop("OPENAI_API_KEY", None)
    env.pop("TELEGRAM_BOT_TOKEN", None)
    env.pop("TELEGRAM_CHAT_ID", None)

    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_runtime_real_preflight.py")],
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    assert result.returncode in (0, 2), result.stderr
    report = json.loads(result.stdout)

    assert report["pipeline"] == "bot_vision_runtime_real_preflight"
    assert report["overall_status"] in {"ready", "blocked"}
    assert report["max_provable_stage"] in {
        "full_runtime_ready",
        "publish_validate_ready_telegram_blocked",
        "capture_ready_analysis_blocked",
        "preflight_only",
    }
    assert isinstance(report["checks"], dict)
    assert "node" in report["checks"]
    assert "python_openai" in report["checks"]
    assert "playwright_runtime_check" in report["checks"]
    assert isinstance(report["blockers"], list)
    assert isinstance(report["recommended_commands"], list)


def test_bot_vision_runtime_real_preflight_detects_missing_env_in_clean_env():
    env = {k: v for k, v in os.environ.items() if k not in {"OPENAI_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"}}
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_runtime_real_preflight.py")],
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    report = json.loads(result.stdout)
    assert report["checks"]["env_openai_api_key"]["ok"] is False
    assert report["checks"]["env_telegram_bot_token"]["ok"] is False
    assert report["checks"]["env_telegram_chat_id"]["ok"] is False
