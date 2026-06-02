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


def get_chat_id(channel: str = "default") -> str:
    """Return the chat_id for a named channel, falling back to TELEGRAM_CHAT_ID."""
    env_var = CHANNEL_ENV.get(channel, "TELEGRAM_CHAT_ID")
    return os.getenv(env_var) or os.getenv("TELEGRAM_CHAT_ID", "")


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

    token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN", "")
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
