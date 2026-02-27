from __future__ import annotations
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field

TF = Literal["W", "D"]

class SRLevel(BaseModel):
    tf: TF = Field(...)
    kind: Literal["S", "R"] = Field(...)
    level: float = Field(..., gt=0)
    label: Optional[str] = None
    confidence: float = Field(default=0.7, ge=0, le=1)

class DeskForm(BaseModel):
    symbol: str = "BTC"
    ts_iso: Optional[str] = None
    sr: List[SRLevel] = Field(default_factory=list)

    bias: Literal["bull", "bear", "neutral"] = "neutral"
    vol_regime: Literal["low", "normal", "high"] = "normal"
    liquidity_note: Optional[str] = None

    etf_flow_bias: Optional[Literal["in", "out", "flat"]] = None
    onchain_flow_bias: Optional[Literal["in", "out", "flat"]] = None
    futures_flow_bias: Optional[Literal["in", "out", "flat"]] = None
    funding_bias: Optional[Literal["pos", "neg", "flat"]] = None
    fear_greed: Optional[int] = Field(default=None, ge=0, le=100)

    corr_xau_btc: Optional[float] = Field(default=None, ge=-1, le=1)
    dxy_trend: Optional[Literal["up", "down", "flat"]] = None

class Metric(BaseModel):
    source: str
    asset: str
    metric: str
    value: float | int | str
    unit: str = ""
    window: str = ""
    quality: float = Field(default=0.8, ge=0, le=1)
    notes: str = ""

class Snapshot(BaseModel):
    ts_iso: str
    metrics: List[Metric] = Field(default_factory=list)
    meta: Dict[str, str] = Field(default_factory=dict)

class ScoreReason(BaseModel):
    code: str
    weight: float
    detail: str

class ScoreResult(BaseModel):
    ts_iso: str
    symbol: str
    probability: float = Field(..., ge=0, le=1)
    score: float
    reasons: List[ScoreReason] = Field(default_factory=list)
    sr_summary: Dict[str, List[float]] = Field(default_factory=dict)
