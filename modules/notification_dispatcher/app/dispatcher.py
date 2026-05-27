from __future__ import annotations
import logging
import os
from typing import Any

from modules.strategy.adapter import validate_strategy_id, log_unknown_strategy_id_warning
from shared.telegram_notify import send_telegram_html
from .events import PipelineEvent, format_message

log = logging.getLogger("notification_dispatcher")


def _get_telegram_config() -> tuple[str, str]:
    token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    return token, chat_id


class NotificationDispatcher:
    """Sends structured Telegram messages for each pipeline event type."""

    def dispatch(self, event: PipelineEvent, dry_run: bool = False) -> dict[str, Any]:
        event.validate()

        sid = event.payload.get("strategy_id", "")
        if sid and not validate_strategy_id(sid):
            log_unknown_strategy_id_warning(sid, "notification_dispatcher")

        message = format_message(event)

        if dry_run:
            log.info("dry_run dispatch event=%s message_len=%d", event.event_type, len(message))
            return {"ok": True, "dry_run": True, "event_type": event.event_type, "message": message}

        token, chat_id = _get_telegram_config()
        if not token or not chat_id:
            log.warning("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set — skipping dispatch")
            return {"ok": False, "error": "telegram config missing", "event_type": event.event_type}

        try:
            tags = {}
            strategy_id = event.payload.get("strategy_id")
            if strategy_id:
                tags["strategy_id"] = strategy_id
            strategy_version = event.payload.get("strategy_version")
            if strategy_version:
                tags["strategy_version"] = strategy_version
            send_telegram_html(message, source=f"notification_dispatcher:{event.event_type}", tags=tags)
            log.info("dispatched event=%s to telegram", event.event_type)
            return {"ok": True, "event_type": event.event_type}
        except Exception as exc:
            log.error("telegram dispatch failed: %s", exc)
            return {"ok": False, "error": str(exc), "event_type": event.event_type}
