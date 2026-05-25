from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

TELEGRAM_CLAIM_LATEST = Path(
    "data/deskpro/inputs/telegram_claim/latest.json"
)


def read_telegram_claim(path: Optional[Path] = None) -> Optional[dict]:
    """Read telegram_claim.v1 from a local JSON file.

    Default path: data/deskpro/inputs/telegram_claim/latest.json
    When path= is explicit, that path is used directly.

    Returns the payload dict if valid, None otherwise.
    Never raises. Never calls Telegram API, reads live channels, or sends messages.
    Absent or malformed file → None (caller treats as missing).
    """
    p = path or TELEGRAM_CLAIM_LATEST
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    if data.get("input_class") != "telegram_claim.v1":
        return None
    return data
