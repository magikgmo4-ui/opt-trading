"""
Outcome tracker — PR10.

Tracks thesis outcomes over time:
  - At +1h, +4h, +24h, +48h, +7d
  - Computes returns and determines if prediction was correct
  - Uses market_metrics DC views for current prices (no broker)

No trade execution. No broker. Read-only price lookup.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

from .archive import load_latest
from .config import CANONICAL_SYMBOLS, normalize_symbol, source_path_for_symbol
from .outcome_models import (
    TRACKING_WINDOWS,
    OutcomeWindow,
    ThesisOutcome,
    determine_actual_direction,
    is_prediction_correct,
)
from .outcome_store import (
    load_outcome,
    load_outcomes,
    load_unresolved,
    save_outcome,
)
from .thesis_engine import build_thesis


def get_current_price(symbol: str) -> Optional[float]:
    """Get current price for a symbol from available data sources.

    Priority: market_metrics DC view → fallback.

    Returns None if no price source is available.
    """
    # Try market_metrics DC views
    try:
        path = source_path_for_symbol("market_metrics", symbol)
        if path and path.exists():
            data = json.loads(path.read_text())
            price = data.get("last_price") or (data.get("metrics", {}) or {}).get("price")
            if isinstance(price, (int, float)):
                return float(price)
    except Exception:
        pass

    # Try loading latest thesis (which contains price)
    try:
        thesis = load_latest(symbol)
        if thesis is not None:
            # Extract price from thesis
            flow = thesis.model_dump()
            flow_data = flow.get("flow", {})
            if flow_data.get("open_interest") is not None:
                # Can't get price from flow directly; try other sources
                pass
    except Exception:
        pass

    return None


def track_outcome(thesis_id: str, symbol: str, generated_at: datetime,
                  predicted_direction: str, predicted_confidence: int,
                  predicted_prob_bull: int, predicted_prob_range: int,
                  predicted_prob_bear: int,
                  price_t0: Optional[float] = None) -> Optional[ThesisOutcome]:
    """Create or update an outcome record for a thesis.

    Checks which time windows have elapsed since generation and
    records prices/returns for each.
    """
    now = datetime.now(timezone.utc)
    elapsed_hours = (now - generated_at).total_seconds() / 3600.0

    # Load existing outcome or create new
    outcome = load_outcome(symbol, thesis_id)
    if outcome is None:
        outcome = ThesisOutcome(
            thesis_id=thesis_id,
            symbol=symbol,
            generated_at=generated_at,
            predicted_direction=predicted_direction,
            predicted_confidence=predicted_confidence,
            predicted_prob_bull=predicted_prob_bull,
            predicted_prob_range=predicted_prob_range,
            predicted_prob_bear=predicted_prob_bear,
            price_t0=price_t0,
        )

    # Try to get current price
    current_price = get_current_price(symbol)

    # Check each window
    all_resolved = True
    existing_window_hours = {w.hours for w in outcome.windows if w.resolved_at is not None}

    for window_hours in TRACKING_WINDOWS:
        if window_hours in existing_window_hours:
            continue  # Already resolved

        if elapsed_hours >= window_hours:
            # Window has elapsed — record outcome
            win = OutcomeWindow(hours=window_hours, resolved_at=now)

            if current_price is not None and outcome.price_t0 is not None and outcome.price_t0 > 0:
                win.price = current_price
                win.return_pct = ((current_price - outcome.price_t0) / outcome.price_t0) * 100

            outcome.windows.append(win)
            existing_window_hours.add(window_hours)
        else:
            all_resolved = False

    # Determine actual direction from the longest resolved window
    long_windows = sorted(
        [w for w in outcome.windows if w.return_pct is not None],
        key=lambda w: w.hours, reverse=True,
    )
    if long_windows:
        outcome.actual_direction = determine_actual_direction(long_windows[0].return_pct)
        outcome.correct = is_prediction_correct(outcome.predicted_direction, outcome.actual_direction)

    outcome.resolved = all_resolved
    outcome.tracked_at = now
    if outcome.resolved and not outcome.resolved_at:
        outcome.resolved_at = now

    save_outcome(outcome)
    return outcome


def track_all_symbols() -> List[ThesisOutcome]:
    """Track outcomes for all canonical symbols.

    Builds fresh theses if none exist, then tracks outcomes.
    """
    outcomes: List[ThesisOutcome] = []
    for sym in CANONICAL_SYMBOLS:
        # Build thesis if not exists
        thesis = load_latest(sym)
        if thesis is None:
            try:
                thesis = build_thesis(sym)
            except Exception:
                continue

        # Convert to dict for field access
        td = thesis.model_dump()
        meta = td.get("metadata", {})
        action = td.get("action", {})
        probs = td.get("probabilities", {})

        thesis_id = meta.get("thesis_id", f"thesis_{sym}_unknown")
        generated_at = thesis.metadata.generated_at
        direction = action.get("direction", "neutral")
        confidence = td.get("confidence", 50)

        # Get price from thesis
        price_t0 = None
        try:
            # Extract from flow metrics or technical levels
            price_t0 = _extract_price_from_thesis(td)
        except Exception:
            pass

        outcome = track_outcome(
            thesis_id=thesis_id,
            symbol=sym,
            generated_at=generated_at,
            predicted_direction=direction,
            predicted_confidence=confidence,
            predicted_prob_bull=probs.get("bull", 33),
            predicted_prob_range=probs.get("range", 34),
            predicted_prob_bear=probs.get("bear", 33),
            price_t0=price_t0,
        )
        if outcome is not None:
            outcomes.append(outcome)

    return outcomes


def track_past_theses(symbol: str, limit: int = 50) -> List[ThesisOutcome]:
    """Scan history/ for past theses and create outcome records for them."""
    from .archive import ARCHIVE_ROOT
    hist_dir = ARCHIVE_ROOT / "history" / symbol
    if not hist_dir.exists():
        return []

    files = sorted(hist_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)[:limit]
    outcomes: List[ThesisOutcome] = []

    for f in files:
        try:
            data = json.loads(f.read_text())
            thesis_id = data.get("metadata", {}).get("thesis_id", f.stem)
            generated_at_str = data.get("metadata", {}).get("generated_at", "")
            if generated_at_str:
                generated_at = datetime.fromisoformat(generated_at_str.replace("Z", "+00:00"))
            else:
                generated_at = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)

            action = data.get("action", {})
            probs = data.get("probabilities", {})

            price_t0 = _extract_price_from_thesis(data)

            outcome = track_outcome(
                thesis_id=thesis_id,
                symbol=symbol,
                generated_at=generated_at,
                predicted_direction=action.get("direction", "neutral"),
                predicted_confidence=data.get("confidence", 50),
                predicted_prob_bull=probs.get("bull", 33),
                predicted_prob_range=probs.get("range", 34),
                predicted_prob_bear=probs.get("bear", 33),
                price_t0=price_t0,
            )
            if outcome is not None:
                outcomes.append(outcome)
        except Exception:
            continue

    return outcomes


def _extract_price_from_thesis(data: dict) -> Optional[float]:
    """Extract price from thesis dict (various locations)."""
    # Try technical support levels midpoint
    tech = data.get("technical", {})
    supports = tech.get("key_support", [])
    resistances = tech.get("key_resistance", [])
    if supports and resistances:
        return (supports[0] + resistances[0]) / 2

    # Try flow metrics
    flow = data.get("flow", {})
    if flow.get("open_interest") is not None:
        # OI is not price, skip
        pass

    # Try from the most recent price in the system
    try:
        price = get_current_price(data.get("symbol", ""))
        if price is not None:
            return price
    except Exception:
        pass

    return None
