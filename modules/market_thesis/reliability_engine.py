"""
Reliability engine — PR10.

Computes a reliability_score (0-100) for each symbol
based on historical accuracy, sample size, and calibration quality.

Factors:
  - Sample size adequacy (0-30 points)
  - Historical accuracy (0-40 points)
  - Confidence calibration (0-20 points)
  - Probability calibration (0-10 points)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .calibration_engine import CalibrationResult, calibrate, calibrate_all
from .outcome_store import count_outcomes


@dataclass
class ReliabilityReport:
    """Reliability assessment for a symbol."""

    symbol: str
    reliability_score: int = 0  # 0-100
    grade: str = "unknown"  # excellent, good, fair, poor, insufficient

    # Components
    sample_size: int = 0
    sample_score: int = 0  # 0-30
    accuracy_score: int = 0  # 0-40
    calibration_score: int = 0  # 0-20
    probability_score: int = 0  # 0-10

    # Context
    calibration: Optional[CalibrationResult] = None


def evaluate_reliability(symbol: str) -> ReliabilityReport:
    """Compute reliability score for a symbol.

    Returns a ReliabilityReport with score 0-100.
    Low sample sizes are penalized but not zeroed.
    """
    result = calibrate(symbol)
    report = ReliabilityReport(symbol=symbol, calibration=result)
    report.sample_size = result.sample_size or count_outcomes(symbol)

    # ── Sample size adequacy (0-30) ───────────────────────────────────
    n = report.sample_size
    if n >= 200:
        report.sample_score = 30
    elif n >= 100:
        report.sample_score = 25
    elif n >= 50:
        report.sample_score = 20
    elif n >= 20:
        report.sample_score = 12
    elif n >= 5:
        report.sample_score = 5
    else:
        report.sample_score = 0

    # ── Accuracy (0-40) ───────────────────────────────────────────────
    acc = result.accuracy_pct
    if n >= 10:
        if acc >= 75:
            report.accuracy_score = 40
        elif acc >= 65:
            report.accuracy_score = 32
        elif acc >= 55:
            report.accuracy_score = 24
        elif acc >= 45:
            report.accuracy_score = 16
        else:
            report.accuracy_score = 8
    elif n >= 3:
        # Limited data: cap accuracy contribution
        report.accuracy_score = min(20, int(acc * 0.3))
    else:
        report.accuracy_score = 0

    # ── Confidence calibration (0-20) ─────────────────────────────────
    if n >= 10 and result.confidence_error != 0:
        err = abs(result.confidence_error)
        if err <= 5:
            report.calibration_score = 20
        elif err <= 10:
            report.calibration_score = 16
        elif err <= 20:
            report.calibration_score = 10
        elif err <= 30:
            report.calibration_score = 5
        else:
            report.calibration_score = 0
    elif n == 0:
        report.calibration_score = 0
    else:
        report.calibration_score = 10  # Neutral if insufficient data

    # ── Probability calibration (0-10) ────────────────────────────────
    if n >= 10:
        prob_err = result.probability_error
        if prob_err <= 15:
            report.probability_score = 10
        elif prob_err <= 25:
            report.probability_score = 7
        elif prob_err <= 40:
            report.probability_score = 4
        else:
            report.probability_score = 1
    elif n == 0:
        report.probability_score = 0
    else:
        report.probability_score = 5  # Neutral

    # ── Total ─────────────────────────────────────────────────────────
    report.reliability_score = (
        report.sample_score
        + report.accuracy_score
        + report.calibration_score
        + report.probability_score
    )
    report.reliability_score = max(0, min(100, report.reliability_score))

    # ── Grade ─────────────────────────────────────────────────────────
    if report.reliability_score >= 80:
        report.grade = "excellent"
    elif report.reliability_score >= 60:
        report.grade = "good"
    elif report.reliability_score >= 40:
        report.grade = "fair"
    elif report.reliability_score >= 20:
        report.grade = "poor"
    else:
        report.grade = "insufficient"

    return report


def evaluate_all_reliability() -> List[ReliabilityReport]:
    """Compute reliability for all canonical symbols."""
    from .config import CANONICAL_SYMBOLS
    return [evaluate_reliability(sym) for sym in CANONICAL_SYMBOLS]
