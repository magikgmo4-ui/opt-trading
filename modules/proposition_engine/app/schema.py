from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class NormalizedSignal:
    signal_id: str
    ticker: str
    side: str        # BUY | SELL
    price: float
    timestamp: float
    strategy_id: str
    tf: str
    tp: float | None = None
    sl: float | None = None
    reason: str = ""
    source: str = "tradingview"

    @classmethod
    def from_dict(cls, d: dict) -> "NormalizedSignal":
        return cls(
            signal_id=d["signal_id"],
            ticker=d["ticker"],
            side=d["side"],
            price=float(d["price"]),
            timestamp=float(d["timestamp"]),
            strategy_id=d.get("strategy_id", ""),
            tf=d.get("tf", ""),
            tp=float(d["tp"]) if d.get("tp") is not None else None,
            sl=float(d["sl"]) if d.get("sl") is not None else None,
            reason=d.get("reason", ""),
            source=d.get("source", "tradingview"),
        )


@dataclass
class PropositionRequest:
    signal: NormalizedSignal
    request_id: str = ""
    dry_run: bool = False
    timeout_s: int = 90


@dataclass
class Proposition:
    request_id: str
    signal_id: str
    action: str         # BUY | SELL | HOLD | SKIP
    size_pct: float     # 0.0–1.0
    entry: float
    sl: float | None
    tp: float | None
    confidence: float   # 0.0–1.0
    rationale: str
    engines_context: dict = field(default_factory=dict)
    duration_ms: int = 0
    dry_run: bool = False
    status: str = "ok"  # ok | error | timeout | skipped
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "signal_id": self.signal_id,
            "action": self.action,
            "size_pct": self.size_pct,
            "entry": self.entry,
            "sl": self.sl,
            "tp": self.tp,
            "confidence": self.confidence,
            "rationale": self.rationale,
            "engines_context": self.engines_context,
            "duration_ms": self.duration_ms,
            "dry_run": self.dry_run,
            "status": self.status,
            "error": self.error,
        }


class PropositionError(Exception):
    pass


class EngineError(PropositionError):
    pass


class BridgeCallError(PropositionError):
    pass
