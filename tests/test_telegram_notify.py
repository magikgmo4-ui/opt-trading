from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

from shared.telegram_notify import send_telegram_with_metrics


def test_send_telegram_with_metrics_returns_real_message_refs(tmp_path, monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-123")
    monkeypatch.setenv("TELEGRAM_LATENCY_LOG_PATH", str(tmp_path / "telegram_send.jsonl"))

    response = Mock()
    response.status_code = 200
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "ok": True,
        "result": {
            "message_id": 456,
            "chat": {"id": -123},
        },
    }

    with patch("shared.telegram_notify.requests.post", return_value=response) as mock_post:
        result = send_telegram_with_metrics("hello", source="bot_vision")

    assert result["ok"] is True
    assert result["telegram_chat_id"] == "-123"
    assert result["telegram_message_id"] == "456"
    assert mock_post.called
    assert Path(tmp_path / "telegram_send.jsonl").exists()
