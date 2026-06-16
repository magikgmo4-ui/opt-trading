"""
Cross-Asset Engine — PR2.

Analyzes relationships between assets using market thesis data.
Detects leaders, laggards, and computes influence/correlation scores.

Read-only. Reads from market_thesis archive. No broker.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .models import AssetInfluence, LeaderBoardEntry


# ── Dependency Graph ───────────────────────────────────────────────────────

# Predefined cross-asset relationships (parent → children)
DEPENDENCY_MAP: Dict[str, List[str]] = {
    "BTC": ["ETH", "SOL", "XRP"],
    "DXY": ["XAU"],
    "SPY": ["NVDA", "AVGO", "MU"],
    "NVDA": ["AVGO", "MU"],
}

# Sector classification
SECTORS: Dict[str, str] = {
    "BTC": "crypto", "ETH": "crypto", "SOL": "crypto", "XRP": "crypto",
    "XAU": "commodity",
    "SPCX": "space",
    "NVDA": "semiconductor", "AVGO": "semiconductor", "MU": "semiconductor",
}

# Inverse relationships (parent up → child down)
INVERSE_PAIRS: set[Tuple[str, str]] = {("DXY", "XAU")}

# Symbol display names
DISPLAY_NAMES: Dict[str, str] = {"XAU": "Gold", "SPCX": "SpaceX"}


# ── Thesis reader ──────────────────────────────────────────────────────────

def _load_thesis(symbol: str) -> Optional[dict]:
    """Load latest thesis for a symbol from archive."""
    try:
        from modules.market_thesis.archive import load_latest
        thesis = load_latest(symbol)
        if thesis is None:
            from modules.market_thesis.thesis_engine import build_thesis
            from modules.market_thesis.archive import save_all
            thesis = build_thesis(symbol)
            save_all(thesis)
        return thesis.model_dump(by_alias=True, mode="json")
    except Exception:
        return None


def _load_reliability(symbol: str) -> dict:
    """Load reliability stats for a symbol."""
    try:
        from modules.market_thesis.reliability_engine import evaluate_reliability
        rel = evaluate_reliability(symbol)
        return {
            "reliability": rel.reliability_score,
            "sample_size": rel.sample_size,
        }
    except Exception:
        return {"reliability": 0, "sample_size": 0}


# ── Engine ─────────────────────────────────────────────────────────────────

def compute_influences(symbols: Optional[List[str]] = None) -> List[AssetInfluence]:
    """Compute cross-asset influence relationships.

    For each parent→child pair in DEPENDENCY_MAP, checks if the
    thesis directions are aligned (or inversely aligned for inverse pairs).
    """
    if symbols is None:
        symbols = list(DEPENDENCY_MAP.keys())

    influences: List[AssetInfluence] = []

    for parent, children in DEPENDENCY_MAP.items():
        parent_thesis = _load_thesis(parent)
        if parent_thesis is None:
            continue

        parent_dir = parent_thesis.get("action", {}).get("direction", "neutral")
        parent_conf = parent_thesis.get("confidence", 50)

        for child in children:
            child_thesis = _load_thesis(child)
            if child_thesis is None:
                continue

            child_dir = child_thesis.get("action", {}).get("direction", "neutral")
            is_inverse = (parent, child) in INVERSE_PAIRS

            # Determine expected alignment
            if is_inverse:
                aligned = (
                    (parent_dir == "bullish" and child_dir == "bearish") or
                    (parent_dir == "bearish" and child_dir == "bullish")
                )
                direction = "opposite"
            else:
                aligned = parent_dir == child_dir
                direction = "same"

            # Compute influence score
            if aligned:
                influence = min(100, int(parent_conf * 0.8 + 20))
            else:
                influence = max(5, int(50 - abs(parent_conf - 50) * 0.3))

            # Compute approximate correlation
            if aligned:
                correlation = 0.5 + (parent_conf / 200.0)  # 0.5 to 1.0 range
            else:
                correlation = 0.0 + ((100 - parent_conf) / 200.0)  # 0.0 to 0.5

            if is_inverse:
                correlation = -correlation

            evidence = f"{parent} → {child}: {'alignés' if aligned else 'divergents'} (confiance parent: {parent_conf}%)"
            if is_inverse:
                evidence += " [relation inverse]"

            influences.append(AssetInfluence(
                source=parent,
                target=child,
                correlation=round(correlation, 2),
                influence_score=influence,
                direction=direction,
                evidence=evidence,
            ))

    return influences


def build_leaderboard(symbols: Optional[List[str]] = None) -> List[LeaderBoardEntry]:
    """Build a ranked leaderboard of all tracked assets.

    Ranking based on: confidence × reliability × momentum.
    """
    all_symbols = ["BTC", "ETH", "SOL", "XRP", "XAU", "SPCX", "NVDA", "AVGO", "MU"]
    if symbols:
        all_symbols = [s for s in all_symbols if s in symbols]

    entries: List[LeaderBoardEntry] = []

    for sym in all_symbols:
        thesis = _load_thesis(sym)
        if thesis is None:
            entries.append(LeaderBoardEntry(symbol=sym, rank=0))
            continue

        direction = thesis.get("action", {}).get("direction", "neutral")
        confidence = thesis.get("confidence", 50)
        probs = thesis.get("probabilities", {})
        prob_bull = probs.get("bull", 33)
        prob_bear = probs.get("bear", 33)

        rel = _load_reliability(sym)
        reliability = rel.get("reliability", 0)

        # Momentum = |prob_bull - prob_bear| weighted by confidence
        momentum = int(abs(prob_bull - prob_bear) * confidence / 100.0)
        momentum = max(0, min(100, momentum))

        # Change 24h from thesis data
        change_24h = None
        flow = thesis.get("flow", {})
        oi_change = flow.get("oi_change_24h_pct")
        if oi_change is not None:
            change_24h = float(oi_change)

        entries.append(LeaderBoardEntry(
            symbol=sym,
            rank=0,  # Will be set after sorting
            direction=direction,
            confidence=confidence,
            reliability=reliability,
            momentum_score=momentum,
            change_24h=change_24h,
        ))

    # Sort by composite score
    def composite_score(e: LeaderBoardEntry) -> int:
        return e.confidence + e.reliability + e.momentum_score

    entries.sort(key=composite_score, reverse=True)

    # Assign ranks
    for i, e in enumerate(entries):
        e.rank = i + 1

    # Mark leaders (top 3) and laggards (bottom 3)
    if len(entries) >= 3:
        for e in entries[:3]:
            e.is_leader = True
        for e in entries[-3:]:
            if e.momentum_score < 30 or e.confidence < 40:
                e.is_laggard = True

    return entries


def detect_leaders() -> List[LeaderBoardEntry]:
    """Return only the market leaders."""
    board = build_leaderboard()
    return [e for e in board if e.is_leader]


def detect_laggards() -> List[LeaderBoardEntry]:
    """Return only the market laggards."""
    board = build_leaderboard()
    return [e for e in board if e.is_laggard]


def compute_all() -> dict:
    """Compute full cross-asset analysis: influences + leaderboard."""
    influences = compute_influences()
    leaders = build_leaderboard()
    return {
        "influences": influences,
        "leaders": leaders,
        "leader_count": sum(1 for l in leaders if l.is_leader),
        "laggard_count": sum(1 for l in leaders if l.is_laggard),
        "total_assets": len(leaders),
    }
