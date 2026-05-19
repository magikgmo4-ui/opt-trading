from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class TradePayload:
    symbol: str
    direction: str
    entry_price: float
    exit_price: Optional[float] = None
    quantity: Optional[float] = None
    pnl: Optional[float] = None
    status: str = "open"
    notes: str = ""
    tags: list[str] = field(default_factory=list)

    def to_fields(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class SignalPayload:
    source: str
    timestamp: str
    symbol: str
    signal: str
    confidence: Optional[float] = None
    reviewed_by: str = ""
    notes: str = ""

    def to_fields(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class BacktestPayload:
    strategy: str
    period: str
    sharpe: Optional[float] = None
    drawdown: Optional[float] = None
    trades_count: Optional[int] = None
    verdict: str = ""
    notes: str = ""

    def to_fields(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class GOStatusPayload:
    go_id: str
    status: str
    machine: str = "fantome"
    branch: str = ""
    next_go: str = ""
    updated_at: str = ""

    def to_fields(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}
