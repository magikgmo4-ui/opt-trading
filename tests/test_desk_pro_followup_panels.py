import json
from pathlib import Path

from modules.desk_pro.service.vision_panel import (
    read_news_panel_data,
    read_screener_panel_data,
    read_telegram_claim_panel_data,
)


FIX_CAPTURE = Path(__file__).parent / "fixtures" / "capture_mapping"
FIX_ADMIN = Path(__file__).parent / "fixtures" / "admin_trading_contract_smoke"


def _write(tmp_path: Path, payload: dict) -> Path:
    p = tmp_path / "latest.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


def test_news_panel_reads_valid_payload(tmp_path):
    payload = json.loads((FIX_CAPTURE / "vision_context_news_sentiment_v1_sample.json").read_text(encoding="utf-8"))
    result = read_news_panel_data(path=_write(tmp_path, payload))
    assert result["ok"] is True
    assert result["payload"]["input_class"] == "vision_context.news_sentiment.v1"


def test_screener_panel_reads_valid_payload(tmp_path):
    payload = json.loads((FIX_CAPTURE / "vision_context_screener_v1_sample.json").read_text(encoding="utf-8"))
    result = read_screener_panel_data(path=_write(tmp_path, payload))
    assert result["ok"] is True
    assert result["payload"]["input_class"] == "vision_context.screener.v1"


def test_telegram_claim_panel_reads_valid_payload(tmp_path):
    payload = json.loads((FIX_ADMIN / "telegram_claim_v1_minimal.json").read_text(encoding="utf-8"))
    result = read_telegram_claim_panel_data(path=_write(tmp_path, payload))
    assert result["ok"] is True
    assert result["payload"]["input_class"] == "telegram_claim.v1"


def test_wrong_input_class_returns_not_ok(tmp_path):
    result = read_news_panel_data(path=_write(tmp_path, {"input_class": "wrong"}))
    assert result["ok"] is False
    assert result["reason"] == "wrong_input_class"
