from __future__ import annotations
import logging
import os
import html as html_lib
from typing import Any

import requests

from modules.strategy.adapter import validate_strategy_id
from .events import PipelineEvent, format_message

log = logging.getLogger("notification_dispatcher")

_TELEGRAM_URL = "https://api.telegram.org/bot{token}/sendMessage"


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
            log.warning("unknown strategy_id %r", sid)

        message = format_message(event)

        if dry_run:
            log.info("dry_run dispatch event=%s message_len=%d", event.event_type, len(message))
            return {"ok": True, "dry_run": True, "event_type": event.event_type, "message": message}

        token, chat_id = _get_telegram_config()
        if not token or not chat_id:
            log.warning("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set — skipping dispatch")
            return {"ok": False, "error": "telegram config missing", "event_type": event.event_type}

        url = _TELEGRAM_URL.format(token=token)
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        try:
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            log.info("dispatched event=%s to telegram", event.event_type)
            return {"ok": True, "event_type": event.event_type, "telegram_status": resp.status_code}
        except requests.RequestException as exc:
            log.error("telegram dispatch failed: %s", exc)
            return {"ok": False, "error": str(exc), "event_type": event.event_type}
