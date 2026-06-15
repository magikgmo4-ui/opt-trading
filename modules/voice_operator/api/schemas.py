"""
Voice Operator API Schemas
GO_DESKPRO_VOICE_OPERATOR_01 — Lot B

Stable JSON contracts for /read/* endpoints.
These are read-only views — no trading logic, no score computation.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SystemState:
    """GET /read/system"""
    status: str                          # "ok" | "degraded" | "down"
    services_running: int                # count of accessible services
    services: list[dict] = field(default_factory=list)
    critical_alerts: int = 0
    pipeline_state: str = "unknown"      # "healthy" | "warning" | "degraded"
    timers_active: int = 0
    stale_sources: list[str] = field(default_factory=list)
    one_line: str = ""                   # voice-friendly summary


@dataclass
class SpaceXSummary:
    """GET /read/spacex"""
    symbol: str = "SPCX"
    price: Optional[float] = None
    vwap: Optional[float] = None
    vwap_state: str = "NO_DATA"          # "BULLISH" | "BEARISH" | "NEUTRAL" | "NO_DATA"
    vwap_score: int = 0
    gap_ipo_pct: Optional[float] = None
    trend: str = "neutral"               # "bullish" | "bearish" | "neutral"
    trade_ready: int = 0
    top_setup: Optional[str] = None
    setup_grade: str = "reject"           # "A+" | "A" | "B" | "reject"
    confidence: float = 0.0
    orderflow_score: Optional[float] = None
    ownership_pressure_score: Optional[float] = None
    pipeline_state: str = "unknown"
    source_quality: str = "unknown"
    summary: str = ""                     # voice-friendly one-liner


@dataclass
class AlertItem:
    """Single alert entry for /read/alerts"""
    ts: str = ""
    source: str = ""                      # "deskpro" | "telegram" | "tradingview" | "spcx"
    severity: str = "info"                # "critical" | "warning" | "info"
    message: str = ""


@dataclass
class AlertsSummary:
    """GET /read/alerts"""
    total: int = 0
    critical: int = 0
    items: list[dict] = field(default_factory=list)
    one_line: str = ""


@dataclass
class SetupItem:
    """Single setup for /read/setups or /read/setup"""
    symbol: str = ""
    setup_type: str = ""
    direction: str = "neutral"            # "LONG" | "SHORT" | "neutral"
    grade: str = ""                       # "A+" | "A" | "B" | "CANDIDATE"
    trade_ready: int = 0
    confidence: float = 0.0
    entry_zone: Optional[str] = None
    invalidation: Optional[str] = None
    target_1: Optional[float] = None
    source: str = ""                      # "spcx_v2" | "tv_webhook" | "deskpro_form"


@dataclass
class SetupsSummary:
    """GET /read/setups"""
    active: int = 0
    a_plus: int = 0
    a_grade: int = 0
    items: list[dict] = field(default_factory=list)
    one_line: str = ""


@dataclass
class ScoreDetail:
    """GET /read/score?symbol=X"""
    symbol: str = ""
    trade_ready: int = 0
    momentum: Optional[float] = None
    risk: Optional[float] = None
    smart_money: int = 0
    liquidity: int = 0
    vwap_score: Optional[int] = None
    orderflow_score: Optional[float] = None
    ownership_pressure_score: Optional[float] = None
    probability: float = 0.0
    one_line: str = ""


@dataclass
class MarketReport:
    """GET /read/market / /read/report"""
    generated_at: str = ""
    symbols: list[dict] = field(default_factory=list)
    top_setups: list[dict] = field(default_factory=list)
    active_alerts: list[dict] = field(default_factory=list)
    one_line: str = ""
