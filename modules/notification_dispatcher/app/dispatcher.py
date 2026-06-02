from __future__ import annotations
import logging
import os
from typing import Any

from modules.strategy.adapter import validate_strategy_id, log_unknown_strategy_id_warning
from shared.telegram_channels import send_to_channel
from .events import PipelineEvent, format_message

log = logging.getLogger("notification_dispatcher")


class NotificationDispatcher:
    """Sends structured Telegram messages for each pipeline event type — routed to 'pipeline' channel."""

    def dispatch(self, event: PipelineEvent, dry_run: bool = False) -> dict[str, Any]:
        event.validate()

        sid = event.payload.get("strategy_id", "")
        if sid and not validate_strategy_id(sid):
            log_unknown_strategy_id_warning(sid, "notification_dispatcher")

        message = format_message(event)

        if dry_run:
            log.info("dry_run dispatch event=%s message_len=%d", event.event_type, len(message))
            return {"ok": True, "dry_run": True, "event_type": event.event_type, "message": message}

        try:
            tags: dict[str, Any] = {}
            if sid := event.payload.get("strategy_id"):
                tags["strategy_id"] = sid
            if sv := event.payload.get("strategy_version"):
                tags["strategy_version"] = sv
            result = send_to_channel(
                "pipeline",
                message,
                source=f"notification_dispatcher:{event.event_type}",
                tags=tags,
            )
            if not result.get("ok"):
                log.warning("telegram dispatch failed: %s", result.get("error"))
                return {"ok": False, "error": result.get("error"), "event_type": event.event_type}
            log.info("dispatched event=%s to pipeline channel", event.event_type)
            return {"ok": True, "event_type": event.event_type}
        except Exception as exc:
            log.error("telegram dispatch failed: %s", exc)
            return {"ok": False, "error": str(exc), "event_type": event.event_type}
