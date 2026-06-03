"""
Telegram channel routing — shared/telegram_channels.py

Résout le bon chat_id selon le canal logique déclaré dans
configs/telegram/channel_map.yaml.

Usage dans les callers :
    from shared.telegram_channels import send_to_channel
    send_to_channel("alerts", "🚨 <b>kill switch STOP</b>", source="kill_switch_check")

Fallback : si la var d'env du canal n'est pas définie → TELEGRAM_CHAT_ID.
"""
from __future__ import annotations
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

# Canal → variable d'environnement
# Source canonique : configs/telegram/channel_map.yaml
CHANNEL_ENV: dict[str, str] = {
    "alerts":   "TELEGRAM_CHAT_ID_ALERTS",
    "pipeline": "TELEGRAM_CHAT_ID_PIPELINE",
    "push":     "TELEGRAM_CHAT_ID_PUSH",
    "ops":      "TELEGRAM_CHAT_ID_OPS",
    "default":  "TELEGRAM_CHAT_ID",
}

ENV_FILES: tuple[Path, ...] = (
    Path("/opt/trading/.env"),
    Path("/opt/trading/modules/bot_vision_step2/config/bot_vision.env"),
    Path("/opt/trading/configs/env/roles/telegram_collector.env"),
)


def _read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


@lru_cache(maxsize=1)
def _file_env() -> dict[str, str]:
    merged: dict[str, str] = {}
    for path in ENV_FILES:
        merged.update(_read_env_file(path))
    return merged


def _getenv(name: str) -> str:
    return os.getenv(name) or _file_env().get(name, "")


def get_chat_id(channel: str = "default") -> str:
    """Return the chat_id for a named channel, falling back to TELEGRAM_CHAT_ID."""
    env_var = CHANNEL_ENV.get(channel, "TELEGRAM_CHAT_ID")
    return _getenv(env_var) or _getenv("TELEGRAM_CHAT_ID")


def send_to_channel(
    channel: str,
    message: str,
    *,
    source: str | None = None,
    tags: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Send an HTML Telegram message to a named channel.

    Falls back to TELEGRAM_CHAT_ID if the channel-specific var is not set.
    Returns the result dict from send_telegram_with_metrics.
    """
    from shared.telegram_notify import send_telegram_with_metrics

    token = _getenv("TELEGRAM_BOT_TOKEN") or _getenv("TELEGRAM_TOKEN")
    chat_id = get_chat_id(channel)

    if not token or not chat_id:
        return {"ok": False, "error": f"telegram config missing for channel={channel!r}"}

    return send_telegram_with_metrics(
        message,
        token=token,
        chat_id=chat_id,
        parse_mode="HTML",
        source=source,
        tags={**(tags or {}), "channel": channel},
    )


def send_photo_to_channel(
    channel: str,
    photo_path: str,
    *,
    caption: str = "",
    source: str | None = None,
    tags: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from shared.telegram_notify import send_telegram_photo_with_metrics

    token = _getenv("TELEGRAM_BOT_TOKEN") or _getenv("TELEGRAM_TOKEN")
    chat_id = get_chat_id(channel)

    if not token or not chat_id:
        return {"ok": False, "error": f"telegram config missing for channel={channel!r}"}

    return send_telegram_photo_with_metrics(
        photo_path,
        caption=caption,
        token=token,
        chat_id=chat_id,
        source=source,
        tags={**(tags or {}), "channel": channel},
    )
