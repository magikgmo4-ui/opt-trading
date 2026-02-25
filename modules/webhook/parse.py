from __future__ import annotations
from typing import Any, Mapping

from modules.webhook.schema import WebhookPayload

def _as_str(v: Any) -> str:
    if v is None:
        return ""
    return str(v).strip()

def _as_float(v: Any) -> float:
    if v is None or v == "":
        raise ValueError("missing numeric value")
    try:
        return float(v)
    except Exception as e:
        raise ValueError(f"invalid number: {v!r}") from e

def parse_payload(d: Mapping[str, Any]) -> WebhookPayload:
    """
    Normalize incoming webhook JSON to a stable payload.
    Required: engine, signal, symbol, tf, price
    Optional: key, tp, sl, reason
    """
    out: WebhookPayload = {}

    # Keep raw copy for journaling/debug
    out["raw"] = dict(d)

    # auth (optional)
    k = _as_str(d.get("key"))
    if k:
        out["key"] = k

    # required routing/market
    out["engine"] = _as_str(d.get("engine"))
    out["signal"] = _as_str(d.get("signal")).upper()  # type: ignore[assignment]
    out["symbol"] = _as_str(d.get("symbol"))
    out["tf"] = _as_str(d.get("tf"))
    out["price"] = _as_float(d.get("price"))

    # optional numbers
    tp = d.get("tp")
    if tp not in (None, ""):
        out["tp"] = _as_float(tp)
    sl = d.get("sl")
    if sl not in (None, ""):
        out["sl"] = _as_float(sl)

    reason = _as_str(d.get("reason"))
    if reason:
        out["reason"] = reason

    # minimal validation
    missing = [k for k in ("engine", "signal", "symbol", "tf") if not out.get(k)]
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")
    if out["signal"] not in ("BUY", "SELL"):
        raise ValueError(f"invalid signal: {out['signal']!r}")

    return out
