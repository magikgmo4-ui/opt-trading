"""scorer.py — Score setup /10 per SMC_ORB_VWAP_SCALP_A_PLUS rules."""
from __future__ import annotations

from .detectors import Setup

_ACTIVE_SESSIONS = {"london", "ny", "overlap"}


def score_setup(setup: Setup, min_rr: float = 1.8) -> int:
    """Return integer score 0-10."""
    score = 0

    # HTF bias clear (proxied: structure state set)
    if setup.structure_state:
        score += 2

    # Liquidity zone or ORB zone clear
    if setup.liquidity_state or setup.orb_state:
        score += 2

    # CHOCH/BOS confirmed
    if "choch" in setup.structure_state or "bos" in setup.structure_state:
        score += 2

    # Clean retest (proxied: setup_type contains RETEST or SWEEP)
    if "RETEST" in setup.setup_type or "SWEEP" in setup.setup_type or "COMBINED" in setup.setup_type:
        score += 1

    # RR >= min_rr (estimated from ATR; SL = 1 ATR, TP = min_rr ATR)
    if setup.atr > 0:
        score += 1  # RR will be enforced in simulator; credit here

    # Active session
    if setup.session in _ACTIVE_SESSIONS:
        score += 1

    # Spread/slippage acceptable (always true in backtest — spreads from config)
    score += 1

    return min(score, 10)
