from __future__ import annotations
from typing import Any
from ..io import utc_now

def normalize_tradingview_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "tradingview_webhook",
        "collected_at": utc_now(),
        "ok": True,
        "symbol": payload.get("symbol") or payload.get("ticker") or "SPCX",
        "timeframe": payload.get("timeframe") or payload.get("tf"),
        "event": payload.get("event") or payload.get("alert_name") or payload.get("setup"),
        "price": _num(payload.get("price") or payload.get("close")),
        "volume": _num(payload.get("volume")),
        "vwap": _num(payload.get("vwap")),
        "flags": {
            "fvg": _bool(payload.get("fvg")),
            "bos": _bool(payload.get("bos")),
            "choch": _bool(payload.get("choch")),
            "orb_break": _bool(payload.get("orb_break")),
            "vwap_reclaim": _bool(payload.get("vwap_reclaim")),
        },
        "raw": payload,
    }

def _num(v):
    try:
        return float(v) if v not in (None, "") else None
    except Exception:
        return None

def _bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        return v.lower() in {"1", "true", "yes", "y", "on"}
    return False
