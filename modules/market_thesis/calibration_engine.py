"""
Calibration engine — PR10.

Computes accuracy, confidence error, and probability error
from historical thesis outcomes.

No trade execution. No broker. Read-only statistics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .outcome_models import ThesisOutcome
from .outcome_store import load_outcomes, count_outcomes


@dataclass
class CalibrationResult:
    """Calibration metrics for a single symbol."""

    symbol: str
    sample_size: int = 0

    # Accuracy
    accuracy_pct: float = 0.0  # % of correct predictions
    correct_count: int = 0
    incorrect_count: int = 0
    unevaluated_count: int = 0

    # Confidence calibration
    mean_confidence: float = 0.0  # Average announced confidence
    confidence_error: float = 0.0  # Mean confidence - actual accuracy (positive = overconfident)

    # Probability calibration
    mean_prob_bull: float = 0.0
    mean_prob_bear: float = 0.0
    prob_bull_actual: float = 0.0  # Actual % of bullish outcomes
    prob_bear_actual: float = 0.0  # Actual % of bearish outcomes
    probability_error: float = 0.0  # Mean absolute error between predicted and actual

    # Win rates by direction
    bullish_win_rate: Optional[float] = None
    bearish_win_rate: Optional[float] = None

    # Return stats
    mean_return_pct: float = 0.0
    median_return_pct: float = 0.0


@dataclass
class HistoricalStats:
    """Aggregated historical statistics across all symbols."""

    total_outcomes: int = 0
    total_correct: int = 0
    overall_accuracy_pct: float = 0.0
    by_symbol: List[CalibrationResult] = field(default_factory=list)


def calibrate(symbol: str, limit: int = 200) -> CalibrationResult:
    """Compute calibration metrics for a symbol.

    Args:
        symbol: Canonical symbol
        limit: Maximum number of outcomes to analyze

    Returns:
        CalibrationResult with accuracy, confidence error, probability error.
    """
    outcomes = load_outcomes(symbol, limit=limit)

    result = CalibrationResult(symbol=symbol)
    result.sample_size = len(outcomes)

    if not outcomes:
        return result

    # Evaluable outcomes (have correct/incorrect verdict)
    evaluated = [o for o in outcomes if o.correct is not None]

    correct = [o for o in evaluated if o.correct is True]
    incorrect = [o for o in evaluated if o.correct is False]
    unevaluated = [o for o in outcomes if o.correct is None]

    result.correct_count = len(correct)
    result.incorrect_count = len(incorrect)
    result.unevaluated_count = len(unevaluated)

    if evaluated:
        result.accuracy_pct = round(len(correct) / len(evaluated) * 100, 1)

    # Confidence calibration
    if evaluated:
        confidences = [o.predicted_confidence for o in evaluated]
        result.mean_confidence = round(sum(confidences) / len(confidences), 1)
        result.confidence_error = round(result.mean_confidence - result.accuracy_pct, 1)

    # Probability calibration
    if evaluated:
        bull_probs = [o.predicted_prob_bull for o in evaluated]
        bear_probs = [o.predicted_prob_bear for o in evaluated]
        result.mean_prob_bull = round(sum(bull_probs) / len(bull_probs), 1)
        result.mean_prob_bear = round(sum(bear_probs) / len(bear_probs), 1)

        # Actual outcomes
        actual_bull = sum(1 for o in evaluated if o.actual_direction == "bullish")
        actual_bear = sum(1 for o in evaluated if o.actual_direction == "bearish")
        result.prob_bull_actual = round(actual_bull / len(evaluated) * 100, 1)
        result.prob_bear_actual = round(actual_bear / len(evaluated) * 100, 1)

        # Mean absolute error
        errors = []
        for o in evaluated:
            if o.actual_direction == "bullish":
                errors.append(abs(o.predicted_prob_bull - 100))
            elif o.actual_direction == "bearish":
                errors.append(abs(o.predicted_prob_bear - 100))
            else:
                errors.append(abs(o.predicted_prob_range - 100))
        if errors:
            result.probability_error = round(sum(errors) / len(errors), 1)

    # Win rates by predicted direction
    bull_eval = [o for o in evaluated if o.predicted_direction == "bullish"]
    if bull_eval:
        result.bullish_win_rate = round(
            sum(1 for o in bull_eval if o.correct) / len(bull_eval) * 100, 1
        )
    bear_eval = [o for o in evaluated if o.predicted_direction == "bearish"]
    if bear_eval:
        result.bearish_win_rate = round(
            sum(1 for o in bear_eval if o.correct) / len(bear_eval) * 100, 1
        )

    # Return stats
    returns = []
    for o in evaluated:
        for w in o.windows:
            if w.return_pct is not None:
                returns.append(w.return_pct)
    if returns:
        result.mean_return_pct = round(sum(returns) / len(returns), 2)
        sorted_returns = sorted(returns)
        mid = len(sorted_returns) // 2
        result.median_return_pct = round(sorted_returns[mid], 2)

    return result


def calibrate_all(limit: int = 200) -> HistoricalStats:
    """Compute calibration for all canonical symbols."""
    from .config import CANONICAL_SYMBOLS

    stats = HistoricalStats()
    for sym in CANONICAL_SYMBOLS:
        result = calibrate(sym, limit=limit)
        stats.by_symbol.append(result)
        stats.total_outcomes += result.sample_size
        stats.total_correct += result.correct_count

    if stats.total_outcomes > 0:
        evaluated_total = stats.total_correct + sum(
            r.incorrect_count for r in stats.by_symbol
        )
        if evaluated_total > 0:
            stats.overall_accuracy_pct = round(
                stats.total_correct / evaluated_total * 100, 1
            )

    return stats
