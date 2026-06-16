"""
Outcome models — PR10.

Defines the ThesisOutcome contract for storing and computing
historical outcome measurements of generated theses.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field


class OutcomeWindow(BaseModel):
    """Price and return at a specific time horizon."""

    hours: float = Field(..., description="Time horizon in hours (1, 4, 24, 48, 168)")
    price: Optional[float] = Field(default=None, description="Price at this horizon, if reached")
    return_pct: Optional[float] = Field(default=None, description="Return in percent from t0")
    resolved_at: Optional[datetime] = Field(default=None, description="When this window was resolved")


class ThesisOutcome(BaseModel):
    """Outcome of a single market thesis, tracked over time."""

    thesis_id: str = Field(..., description="References ThesisMetadata.thesis_id")
    symbol: str = Field(..., min_length=1, max_length=10)
    generated_at: datetime = Field(...)

    # Predicted values (from thesis)
    predicted_direction: str = Field(..., description="bullish, bearish, neutral, wait")
    predicted_confidence: int = Field(..., ge=0, le=100)
    predicted_prob_bull: int = Field(..., ge=0, le=100)
    predicted_prob_range: int = Field(..., ge=0, le=100)
    predicted_prob_bear: int = Field(..., ge=0, le=100)

    # Entry price (t0)
    price_t0: Optional[float] = Field(default=None, description="Price at thesis generation")

    # Outcome windows
    windows: List[OutcomeWindow] = Field(default_factory=list)

    # Computed fields (populated after resolution)
    actual_direction: Optional[str] = Field(default=None, description="bullish, bearish, neutral — based on return sign")
    correct: Optional[bool] = Field(default=None, description="Did predicted direction match actual?")
    resolved: bool = Field(default=False, description="All windows resolved?")
    resolved_at: Optional[datetime] = Field(default=None)

    # Tracking metadata
    tracked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: str = Field(default="market_thesis_outcome_tracker", description="Module that generated this outcome")


def determine_actual_direction(return_pct: Optional[float]) -> str:
    """Determine actual direction from return percentage."""
    if return_pct is None:
        return "unknown"
    if return_pct > 0.5:
        return "bullish"
    if return_pct < -0.5:
        return "bearish"
    return "neutral"


def is_prediction_correct(predicted: str, actual: str) -> bool:
    """Check if the predicted direction matches actual outcome."""
    if predicted == "wait" or actual == "unknown":
        return False  # can't evaluate wait or unknown
    if predicted == "neutral" and actual == "neutral":
        return True
    if predicted == "bullish" and actual == "bullish":
        return True
    if predicted == "bearish" and actual == "bearish":
        return True
    return False


# Time windows to track (in hours)
TRACKING_WINDOWS = [1, 4, 24, 48, 168]  # 1h, 4h, 24h, 48h, 7d
