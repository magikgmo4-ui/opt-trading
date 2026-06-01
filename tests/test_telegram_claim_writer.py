from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "modules" / "bot_vision" / "headless_capture" / "scripts"


def test_build_claim_from_chart_signals():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        from telegram_claim_writer import build_claim
    finally:
        sys.path.pop(0)

    result = build_claim(
        {
            "run_id": "run_001",
            "summary": "Support 65000, bullish trend",
            "signals": [
                {"type": "support_level", "value": 65000.0, "confidence": 0.81},
                {"type": "trend_direction", "value": "bullish", "confidence": 0.76},
            ],
        },
        screen_type="CHART_TECHNICAL",
        symbol="BTCUSDT.P",
        timeframe="15m",
        channel_id="-123",
        message_id="msg001",
    )
    assert result["input_class"] == "telegram_claim.v1"
    assert result["claim_type"] == "trade_context"
    assert result["symbol"] == "BTCUSDT.P"
    assert result["entities"]["direction"] == "long"
    assert 65000.0 in result["entities"]["levels"]


def test_build_claim_types_for_news_and_screener():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        from telegram_claim_writer import build_claim
    finally:
        sys.path.pop(0)

    news = build_claim({"summary": "news", "signals": []}, screen_type="NEWS_SENTIMENT", symbol="BTCUSDT.P", timeframe="6h")
    screener = build_claim({"summary": "screener", "signals": []}, screen_type="SCREENER_STOCKS", symbol="SCREENER_AI", timeframe="1d")
    assert news["claim_type"] == "news_alert"
    assert screener["claim_type"] == "alpha_signal"


def test_cli_dry_run_outputs_telegram_claim():
    payload = json.dumps(
        {
            "run_id": "run_001",
            "summary": "Support 65000",
            "signals": [{"type": "support_level", "value": 65000.0, "confidence": 0.81}],
        }
    )
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "telegram_claim_writer.py"),
        "--stdin",
        "--screen-type", "CHART_TECHNICAL",
        "--symbol", "BTCUSDT.P",
        "--timeframe", "15m",
        "--dry-run",
    ]
    result = subprocess.run(cmd, input=payload, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["input_class"] == "telegram_claim.v1"
    assert data["claim_type"] == "trade_context"
