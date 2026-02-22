from __future__ import annotations
from typing import Any, Mapping, Optional, Dict

from modules.webhook.parse import parse_payload

def handle_payload(raw: Mapping[str, Any], client_ip: Optional[str], legacy) -> Dict[str, Any]:
    """
    legacy: module-like object providing require_key, enforce_lock, write_journal_entry.
    """
    evt = parse_payload(raw)

    # security + lock + journal (legacy for now)
    legacy.require_key(dict(evt), client_ip)
    legacy.enforce_lock(str(evt.get("engine", "")))
    legacy.write_journal_entry(dict(evt))

    return {
        "ok": True,
        "engine": evt.get("engine"),
        "signal": evt.get("signal"),
        "symbol": evt.get("symbol"),
        "tf": evt.get("tf"),
        "price": evt.get("price"),
    }
