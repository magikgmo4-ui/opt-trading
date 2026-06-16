"""
Narrative Memory Engine — PR4.

Detects what changed between market states:
  - Direction shifts per asset
  - Regime transitions
  - Confidence/momentum changes
  - Leadership rotation

Stores snapshots and compares current vs previous.
Read-only. No trade execution.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from .cross_asset_engine import build_leaderboard
from .models import DetectedChange, LeaderBoardEntry
from .regime_engine import detect_regime

MEMORY_ROOT = Path(__file__).resolve().parents[2] / "data" / "market_thesis" / "memory"


def ensure_dirs() -> None:
    MEMORY_ROOT.mkdir(parents=True, exist_ok=True)


def save_snapshot(snapshot: dict) -> Path:
    """Save a market snapshot for future comparison."""
    ensure_dirs()
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = MEMORY_ROOT / f"snapshot_{ts}.json"
    path.write_text(json.dumps(snapshot, indent=2, default=str))
    return path


def load_last_snapshot() -> Optional[dict]:
    """Load the most recent snapshot."""
    ensure_dirs()
    files = sorted(MEMORY_ROOT.glob("snapshot_*.json"), reverse=True)
    if not files:
        return None
    try:
        return json.loads(files[0].read_text())
    except Exception:
        return None


def capture_snapshot() -> dict:
    """Capture current market state as a snapshot."""
    board = build_leaderboard()
    regime = detect_regime()

    return {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "regime": regime.regime,
        "regime_confidence": regime.confidence,
        "risk_score": regime.risk_score,
        "assets": [
            {
                "symbol": e.symbol,
                "direction": e.direction,
                "confidence": e.confidence,
                "reliability": e.reliability,
                "momentum_score": e.momentum_score,
                "rank": e.rank,
                "is_leader": e.is_leader,
            }
            for e in board
        ],
        "bullish_count": sum(1 for e in board if e.direction == "bullish"),
        "bearish_count": sum(1 for e in board if e.direction == "bearish"),
    }


def detect_changes() -> List[DetectedChange]:
    """Detect changes between the last snapshot and current state.

    Compares: regime, direction per asset, leadership, overall confidence.

    Returns a list of DetectedChange objects, sorted by magnitude.
    """
    current = capture_snapshot()
    previous = load_last_snapshot()
    save_snapshot(current)

    if previous is None:
        return [DetectedChange(
            symbol="market",
            field="initialization",
            previous="none",
            current="initialized",
            magnitude="major",
            description="Première capture de l'état de marché. Pas d'historique de comparaison.",
        )]

    changes: List[DetectedChange] = []

    # ── Regime change ─────────────────────────────────────────────────
    prev_regime = previous.get("regime", "unknown")
    curr_regime = current.get("regime", "unknown")
    if prev_regime != curr_regime:
        changes.append(DetectedChange(
            symbol="market",
            field="regime",
            previous=prev_regime,
            current=curr_regime,
            magnitude="major",
            description=f"Le régime de marché est passé de {prev_regime} à {curr_regime}.",
        ))

    # ── Regime confidence shift ───────────────────────────────────────
    prev_conf = previous.get("regime_confidence", 0)
    curr_conf = current.get("regime_confidence", 0)
    if abs(curr_conf - prev_conf) >= 10:
        direction = "augmenté" if curr_conf > prev_conf else "diminué"
        changes.append(DetectedChange(
            symbol="market",
            field="regime_confidence",
            previous=str(prev_conf),
            current=str(curr_conf),
            magnitude="moderate",
            description=f"La confiance dans le régime a {direction} de {prev_conf}% à {curr_conf}%.",
        ))

    # ── Per-asset direction changes ───────────────────────────────────
    prev_assets = {a["symbol"]: a for a in previous.get("assets", [])}
    curr_assets = {a["symbol"]: a for a in current.get("assets", [])}

    for sym in curr_assets:
        prev_a = prev_assets.get(sym)
        curr_a = curr_assets[sym]
        if prev_a is None:
            continue

        # Direction change
        if prev_a["direction"] != curr_a["direction"]:
            magnitude = "major" if prev_a["direction"] in ("bullish", "bearish") and curr_a["direction"] in ("bearish", "bullish") else "moderate"
            changes.append(DetectedChange(
                symbol=sym,
                field="direction",
                previous=prev_a["direction"],
                current=curr_a["direction"],
                magnitude=magnitude,
                description=f"{sym} passe de {prev_a['direction']} à {curr_a['direction']}.",
            ))

        # Confidence change
        if abs(curr_a["confidence"] - prev_a["confidence"]) >= 15:
            dir_word = "augmenté" if curr_a["confidence"] > prev_a["confidence"] else "diminué"
            changes.append(DetectedChange(
                symbol=sym,
                field="confidence",
                previous=str(prev_a["confidence"]),
                current=str(curr_a["confidence"]),
                magnitude="minor",
                description=f"Confiance {sym} {dir_word} de {prev_a['confidence']}% à {curr_a['confidence']}%.",
            ))

        # Leadership change
        if prev_a.get("is_leader") != curr_a.get("is_leader"):
            if curr_a["is_leader"]:
                changes.append(DetectedChange(
                    symbol=sym,
                    field="leadership",
                    previous="follower",
                    current="leader",
                    magnitude="moderate",
                    description=f"{sym} est devenu un leader de marché.",
                ))
            else:
                changes.append(DetectedChange(
                    symbol=sym,
                    field="leadership",
                    previous="leader",
                    current="follower",
                    magnitude="moderate",
                    description=f"{sym} n'est plus un leader de marché.",
                ))

    # ── Sort by magnitude ─────────────────────────────────────────────
    order = {"major": 0, "moderate": 1, "minor": 2}
    changes.sort(key=lambda c: order.get(c.magnitude, 3))

    return changes


def summarize_changes(changes: List[DetectedChange]) -> str:
    """Generate a French summary of detected changes."""
    if not changes:
        return "Aucun changement significatif détecté depuis la dernière analyse."

    major = [c for c in changes if c.magnitude == "major"]
    moderate = [c for c in changes if c.magnitude == "moderate"]

    parts = []
    if major:
        parts.append(f"{len(major)} changement(s) majeur(s): " + "; ".join(c.description for c in major[:3]))
    if moderate:
        parts.append(f"{len(moderate)} changement(s) modéré(s): " + "; ".join(c.description for c in moderate[:3]))

    return ". ".join(parts) if parts else f"{len(changes)} changement(s) mineur(s) détecté(s)."


def detect_and_save() -> tuple[List[DetectedChange], str]:
    """Detect changes, save snapshot, and return summary."""
    changes = detect_changes()
    summary = summarize_changes(changes)
    return changes, summary
