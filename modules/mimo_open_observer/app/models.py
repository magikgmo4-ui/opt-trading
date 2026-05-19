from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Bar:
    ts_open: datetime
    ts_close: datetime
    open: float
    high: float
    low: float
    close: float
    timeframe: str = "M1"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["ts_open"] = self.ts_open.isoformat()
        d["ts_close"] = self.ts_close.isoformat()
        return d


@dataclass
class RawEvent:
    event_id: str = ""
    version: str = "v0"
    symbol: str = ""
    timezone: str = ""
    window_type: str = ""
    window_open_ts: Optional[datetime] = None
    scope: str = ""
    weekday: str = ""
    ref_open: float = 0.0
    ref_high: float = 0.0
    ref_low: float = 0.0
    ref_close: float = 0.0
    fvg_detected: bool = False
    fvg_direction: str = ""
    fvg_top: float = 0.0
    fvg_bottom: float = 0.0
    fvg_created_at: Optional[datetime] = None
    signal_ts: Optional[datetime] = None
    price_at_signal: float = 0.0
    sweep: bool = False
    sweep_side: str = "none"

    def to_dict(self) -> dict:
        d = asdict(self)
        for key in ("window_open_ts", "fvg_created_at", "signal_ts"):
            val = d.get(key)
            if isinstance(val, datetime):
                d[key] = val.isoformat()
        return d


@dataclass
class EnrichedEvent(RawEvent):
    price_plus_30m: Optional[float] = None
    price_plus_60m: Optional[float] = None
    delta_30m: Optional[float] = None
    delta_60m: Optional[float] = None
    outcome_30m: Optional[str] = None
    outcome_60m: Optional[str] = None
