from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Literal
import time
import uuid

Side = Literal["BUY", "SELL"]


@dataclass
class SignalIn:
    """Raw incoming webhook payload (TradingView or compatible)."""
    engine: str
    signal: str       # BUY | SELL
    symbol: str
    tf: str
    price: float
    tp: float | None = None
    sl: float | None = None
    reason: str = ""
    strategy_id: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedSignal:
    """Canonical signal JSON consumed by proposition_engine."""
    signal_id: str
    ticker: str
    side: Side
    price: float
    timestamp: float        # unix epoch
    strategy_id: str
    tf: str
    tp: float | None
    sl: float | None
    reason: str
    source: str = "tradingview"

    def to_dict(self) -> dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "ticker": self.ticker,
            "side": self.side,
            "price": self.price,
            "timestamp": self.timestamp,
            "strategy_id": self.strategy_id,
            "tf": self.tf,
            "tp": self.tp,
            "sl": self.sl,
            "reason": self.reason,
            "source": self.source,
        }


class SignalValidationError(ValueError):
    pass
