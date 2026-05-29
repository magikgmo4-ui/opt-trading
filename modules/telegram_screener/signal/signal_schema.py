from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ScreenerProducedSignal:
    id: str
    source: str
    signal_type: str
    channel: str
    parsed_at: str
    produced_at: str
    pair: Optional[str] = None
    direction: Optional[str] = None
    entry_price: Optional[float] = None
    sl: Optional[float] = None
    tp: Optional[float] = None
    size: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[str] = None
    raw_text: str = ""
    summary: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source": self.source,
            "signal_type": self.signal_type,
            "channel": self.channel,
            "parsed_at": self.parsed_at,
            "produced_at": self.produced_at,
            "payload": {
                "pair": self.pair,
                "direction": self.direction,
                "entry_price": self.entry_price,
                "sl": self.sl,
                "tp": self.tp,
                "size": self.size,
                "category": self.category,
                "confidence": self.confidence,
                "raw_text": self.raw_text,
                "summary": self.summary,
            },
        }
