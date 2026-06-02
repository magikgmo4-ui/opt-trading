from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Optional

from modules.vision.coinglass.telegram_summary import load_and_format

logger = logging.getLogger(__name__)

# Type alias for the send function — injectable for tests
SendFn = Callable[[str], None]


def _default_send_fn(message: str) -> None:
    from shared.telegram_channels import send_to_channel
    send_to_channel("push", message, source="coinglass_vision")


def send_vision_summary(
    path: Optional[Path] = None,
    send_fn: SendFn = _default_send_fn,
) -> bool:
    """Load latest vision context, format and send to Telegram.

    Returns True if message was sent, False on any failure (silent degradation).
    send_fn is injected — real impl calls send_telegram_html, mock in tests.
    Never raises.
    """
    message = load_and_format(path=path)
    if message is None:
        logger.warning("send_vision_summary: no message to send (load_and_format returned None)")
        return False

    try:
        send_fn(message)
        logger.info("send_vision_summary: message sent (%d chars)", len(message))
        return True
    except Exception:
        logger.exception("send_vision_summary: send_fn failed")
        return False
