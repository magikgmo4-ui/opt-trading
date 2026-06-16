"""
Voice Operator — Multi-TF Setup Reader

Reads multitf_setup_score.v1 views and provides voice-friendly summaries.
No execution, no broker, no order — monitor-only.

GO_VOICE_OPERATOR_MULTITF_SETUP_CONSUMER_01
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_SCORE_DIR = _VIEWS_DIR / "multitf_setup_score.v1" / "by_symbol"


def _load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def read_symbol_score(symbol: str) -> dict | None:
    """Read multitf_setup_score.v1 for one symbol."""
    return _load_json(_SCORE_DIR / f"{symbol}.json")


def read_all_scores() -> list[dict]:
    """Read all available multitf_setup_score.v1 views."""
    scores = []
    if not _SCORE_DIR.exists():
        return scores
    for f in sorted(_SCORE_DIR.glob("*.json")):
        d = _load_json(f)
        if isinstance(d, dict):
            scores.append(d)
    return scores


def summarize_best_setups(top_n: int = 3) -> list[dict]:
    """Return top setups by score across all symbols."""
    all_scores = read_all_scores()
    all_setups = []
    for s in all_scores:
        sym = s.get("symbol", "?")
        bias = s.get("bias", {})
        for st in s.get("setups", []):
            all_setups.append({
                "symbol": sym,
                "setup_id": st.get("setup_id", ""),
                "setup_type": st.get("setup_type", ""),
                "grade": st.get("grade", "C"),
                "score": st.get("score", 0),
                "probability_pct": st.get("probability_pct", 0),
                "confidence_pct": st.get("confidence_pct", 0),
                "direction": st.get("direction", "monitor_only"),
                "htf": bias.get("htf", "neutral"),
                "ltf": bias.get("ltf", "neutral"),
                "alignment": bias.get("alignment", "neutral"),
                "reason": st.get("reason", []),
                "missing": st.get("missing", []),
                "source_quality": s.get("source_quality", {}),
                "next_action": s.get("next_action", []),
            })
    return sorted(all_setups, key=lambda x: x["score"], reverse=True)[:top_n]


def summarize_missing() -> list[str]:
    """Aggregate missing fields across all symbols."""
    all_missing = set()
    for s in read_all_scores():
        for m in s.get("missing", []):
            all_missing.add(m)
    return sorted(all_missing)


def build_setup_summary_for_voice(symbol: str) -> dict:
    """Build a voice-operator-ready summary for a single symbol.

    Returns a dict with spoken-friendly fields.
    """
    score = read_symbol_score(symbol)
    if not score:
        return {
            "ok": False,
            "symbol": symbol,
            "one_line": f"Score {symbol} indisponible.",
            "spoken_text": f"Score {symbol} indisponible. Aucune donnee multitf_setup_score.",
            "cards": [{"label": "Statut", "value": "Aucune vue multitf"}],
            "missing": ["multitf_setup_score"],
            "next_action": ["Produire multitf_setup_score.v1"],
        }

    bias = score.get("bias", {})
    setups = score.get("setups", [])
    sq = score.get("source_quality", {})
    next_actions = score.get("next_action", [])

    # Build cards
    cards = [
        {"label": "Biais HTF", "value": bias.get("htf", "?")},
        {"label": "Biais LTF", "value": bias.get("ltf", "?")},
        {"label": "Alignement", "value": bias.get("alignment", "?")},
    ]
    if setups:
        best = setups[0]
        cards.extend([
            {"label": "Setup", "value": best.get("setup_type", "?")},
            {"label": "Grade", "value": best.get("grade", "?")},
            {"label": "Score", "value": f"{best.get('score', 0)}/100"},
            {"label": "Proba", "value": f"{best.get('probability_pct', 0)}%"},
            {"label": "Confiance", "value": f"{best.get('confidence_pct', 0)}%"},
        ])
        if best.get("invalidation"):
            cards.append({"label": "Invalidation", "value": str(best["invalidation"])})

    # Build spoken text
    parts = [f"{symbol}"]
    if bias.get("htf"):
        parts.append(f"biais H4 {bias['htf']}")
    if bias.get("ltf"):
        parts.append(f"M15 {bias['ltf']}")
    if bias.get("alignment"):
        parts.append(f"alignement {bias['alignment']}")

    if setups:
        best = setups[0]
        parts.append(f"setup {best.get('setup_type', '?')}")
        parts.append(f"grade {best.get('grade', '?')}")
        parts.append(f"score {best.get('score', 0)}/100")
        if best.get("reason"):
            parts.append(f"raison: {'; '.join(best['reason'][:2])}")
    else:
        parts.append("aucun setup detecte")

    spoken = ". ".join(parts) + "."
    one_line = f"{symbol} {bias.get('htf', '?')}/{bias.get('ltf', '?')} · {'grade '+best['grade'] if setups else 'pas de setup'}"

    # Missing fields
    missing = list(score.get("missing", []))
    if not setups:
        missing.append("setups")
    if sq.get("completeness_pct", 100) < 60:
        missing.append("faible completude")

    return {
        "ok": True,
        "symbol": symbol,
        "one_line": one_line,
        "spoken_text": spoken,
        "cards": cards,
        "missing": missing,
        "next_action": next_actions,
        "freshness": sq.get("input_freshness", "unknown"),
    }
