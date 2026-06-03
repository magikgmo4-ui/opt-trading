from __future__ import annotations

from pathlib import Path

import shared.telegram_channels as telegram_channels


def test_get_chat_id_falls_back_to_env_files(tmp_path, monkeypatch):
    env_file = tmp_path / "bot_vision.env"
    env_file.write_text(
        "TELEGRAM_CHAT_ID=-100-default\n"
        "TELEGRAM_CHAT_ID_PUSH=-100-push\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(telegram_channels, "ENV_FILES", (env_file,))
    telegram_channels._file_env.cache_clear()
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID_PUSH", raising=False)

    assert telegram_channels.get_chat_id("push") == "-100-push"
    assert telegram_channels.get_chat_id("ops") == "-100-default"


def test_send_to_channel_uses_file_token_and_chat_id(tmp_path, monkeypatch):
    env_file = tmp_path / "bot_vision.env"
    env_file.write_text(
        "TELEGRAM_BOT_TOKEN=test-token\n"
        "TELEGRAM_CHAT_ID_OPS=-100-ops\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(telegram_channels, "ENV_FILES", (env_file,))
    telegram_channels._file_env.cache_clear()
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID_OPS", raising=False)

    captured: dict[str, str] = {}

    def fake_send(message: str, **kwargs):
        captured["message"] = message
        captured["token"] = kwargs["token"]
        captured["chat_id"] = kwargs["chat_id"]
        return {"ok": True}

    monkeypatch.setattr("shared.telegram_notify.send_telegram_with_metrics", fake_send)

    result = telegram_channels.send_to_channel("ops", "hello", source="test")

    assert result["ok"] is True
    assert captured["token"] == "test-token"
    assert captured["chat_id"] == "-100-ops"


def test_send_photo_to_channel_uses_file_token_and_chat_id(tmp_path, monkeypatch):
    env_file = tmp_path / "bot_vision.env"
    env_file.write_text(
        "TELEGRAM_BOT_TOKEN=test-token\n"
        "TELEGRAM_CHAT_ID_PUSH=-100-push\n",
        encoding="utf-8",
    )
    photo = tmp_path / "sample.png"
    photo.write_bytes(b"png")
    monkeypatch.setattr(telegram_channels, "ENV_FILES", (env_file,))
    telegram_channels._file_env.cache_clear()
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID_PUSH", raising=False)

    captured: dict[str, str] = {}

    def fake_send(photo_path: str, **kwargs):
        captured["photo_path"] = photo_path
        captured["token"] = kwargs["token"]
        captured["chat_id"] = kwargs["chat_id"]
        captured["caption"] = kwargs["caption"]
        return {"ok": True}

    monkeypatch.setattr("shared.telegram_notify.send_telegram_photo_with_metrics", fake_send)

    result = telegram_channels.send_photo_to_channel("push", str(photo), caption="cap", source="test")

    assert result["ok"] is True
    assert captured["token"] == "test-token"
    assert captured["chat_id"] == "-100-push"
    assert captured["photo_path"] == str(photo)
