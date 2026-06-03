from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class SignalCandidate:
    raw_message: str
    source_channel: str
    asset: Optional[str] = None
    symbol: Optional[str] = None
    direction: Optional[str] = None
    entry_min: Optional[float] = None
    entry_max: Optional[float] = None
    tp: list[float] = field(default_factory=list)
    sl: Optional[float] = None
    leverage: Optional[int] = None
    timeframe: Optional[str] = None
    parse_status: str = "UNKNOWN_FORMAT"
    parse_confidence: str = "LOW"
    parse_errors: list[str] = field(default_factory=list)
    message_ref: str = ""
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if not self.symbol and self.asset:
            self.symbol = self.asset

    def to_dict(self) -> dict:
        return {
            "raw_message": self.raw_message,
            "source_channel": self.source_channel,
            "asset": self.asset,
            "symbol": self.symbol,
            "direction": self.direction,
            "entry_min": self.entry_min,
            "entry_max": self.entry_max,
            "tp": list(self.tp),
            "sl": self.sl,
            "leverage": self.leverage,
            "timeframe": self.timeframe,
            "parse_status": self.parse_status,
            "parse_confidence": self.parse_confidence,
            "parse_errors": list(self.parse_errors),
            "message_ref": self.message_ref,
            "created_at": self.created_at,
        }
