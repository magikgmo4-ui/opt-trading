from __future__ import annotations
import logging
import time
import uuid
from typing import Any, Mapping

from modules.strategy.adapter import validate_strategy_id, log_unknown_strategy_id_warning
from .schema import SignalIn, NormalizedSignal, SignalValidationError, Side

log = logging.getLogger("signal_router")

VALID_SIDES: set[str] = {"BUY", "SELL"}


def _as_float(v: Any, field: str) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        raise SignalValidationError(f"invalid numeric value for '{field}': {v!r}")


def parse_incoming(raw: Mapping[str, Any]) -> SignalIn:
    missing = [f for f in ("engine", "signal", "symbol", "tf", "price") if not raw.get(f)]
    if missing:
        raise SignalValidationError(f"missing required fields: {', '.join(missing)}")

    side = str(raw["signal"]).upper()
    if side not in VALID_SIDES:
        raise SignalValidationError(f"invalid signal '{side}', expected BUY or SELL")

    price = _as_float(raw["price"], "price")

    tp = _as_float(raw["tp"], "tp") if raw.get("tp") not in (None, "") else None
    sl = _as_float(raw["sl"], "sl") if raw.get("sl") not in (None, "") else None

    return SignalIn(
        engine=str(raw["engine"]).strip(),
        signal=side,
        symbol=str(raw["symbol"]).strip().upper(),
        tf=str(raw["tf"]).strip(),
        price=price,
        tp=tp,
        sl=sl,
        reason=str(raw.get("reason", "")).strip(),
        strategy_id=str(raw.get("strategy_id", raw.get("engine", ""))).strip(),
        raw=dict(raw),
    )


def normalize(signal_in: SignalIn) -> NormalizedSignal:
    return NormalizedSignal(
        signal_id=str(uuid.uuid4()),
        ticker=signal_in.symbol,
        side=signal_in.signal,  # type: ignore[arg-type]
        price=signal_in.price,
        timestamp=time.time(),
        strategy_id=signal_in.strategy_id or signal_in.engine,
        tf=signal_in.tf,
        tp=signal_in.tp,
        sl=signal_in.sl,
        reason=signal_in.reason,
    )


def route(raw: Mapping[str, Any]) -> NormalizedSignal:
    """Parse, validate and normalize an incoming webhook payload."""
    signal_in = parse_incoming(raw)
    normalized = normalize(signal_in)
    if not validate_strategy_id(normalized.strategy_id):
        log_unknown_strategy_id_warning(normalized.strategy_id, "signal_router")
    log.info(
        "signal routed signal_id=%s ticker=%s side=%s price=%s",
        normalized.signal_id, normalized.ticker, normalized.side, normalized.price,
    )
    return normalized
