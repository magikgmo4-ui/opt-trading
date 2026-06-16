"""
Voice Operator — Market Thesis Voice Formatter (short audio).

Produces human-readable spoken text. No JSON, no underscores, no field names.
French language. 2-4 sentences. < 250 chars ideal.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


def _safe(d: dict, *keys: str, default: Any = "?") -> Any:
    for k in keys:
        if isinstance(d, dict) and k in d:
            return d[k]
    return default


def format_spoken(symbol: str, thesis: Optional[Dict[str, Any]]) -> str:
    """Format a thesis into a short, natural French voice line.

    Returns a spoken_text string suitable for TTS.
    """
    if thesis is None:
        return _missing_spoken(symbol)

    action = thesis.get("action", {})
    ctx = thesis.get("context", {})
    technical = thesis.get("technical", {})
    probs = thesis.get("probabilities", {})
    risks = thesis.get("risks", [])
    freshness = thesis.get("freshness", {})
    confidence = thesis.get("confidence", 50)

    # ── Stale warning ──────────────────────────────────────────────────
    fresh_state = _safe(freshness, "overall", default="fresh")
    if fresh_state in ("stale", "expired"):
        return _stale_spoken(symbol, thesis)

    # ── Build spoken text ──────────────────────────────────────────────
    direction = action.get("direction", "neutral")
    dir_spoken = {"bullish": "haussier", "bearish": "baissier", "neutral": "neutre", "wait": "en attente"}.get(direction, direction)

    display_sym = {"XAU": "l'or", "SPCX": "SpaceX"}.get(symbol, symbol)

    # Sentence 1: Bias + confidence
    parts = [f"{display_sym} reste en biais {dir_spoken}"]

    if confidence >= 70:
        parts[-1] += f", avec une confiance élevée de {confidence}%"
    elif confidence >= 45:
        parts[-1] += f", avec une confiance modérée de {confidence}%"
    else:
        parts[-1] += f", avec une confiance faible de {confidence}%"

    # Sentence 2: Context or technical
    ctx_narrative = _safe(ctx, "narrative", default="")
    if ctx_narrative and len(ctx_narrative) > 10:
        # Extract first meaningful sentence
        first_sent = ctx_narrative.split(".")[0].strip()
        if len(first_sent) > 20:
            parts.append(first_sent + ".")
        else:
            parts.append("Le contexte macro est incertain.")

    # Sentence 3: Risk
    high_risks = [r for r in risks if r.get("severity") == "high"]
    if high_risks:
        risk_desc = high_risks[0].get("description", "")
        # Shorten
        if len(risk_desc) > 120:
            risk_desc = risk_desc[:117] + "..."
        parts.append(f"Le risque principal: {risk_desc}")
    else:
        mod_risks = [r for r in risks if r.get("severity") == "moderate"]
        if mod_risks:
            risk_desc = mod_risks[0].get("description", "")
            if len(risk_desc) > 100:
                risk_desc = risk_desc[:97] + "..."
            parts.append(f"Risque modéré: {risk_desc}")

    # Sentence 4: Action — always monitor-only
    parts.append("Action recommandée: surveillance uniquement, attendre confirmation avant toute décision.")

    spoken = ". ".join(parts)

    # Ensure < 350 chars for TTS
    if len(spoken) > 350:
        spoken = spoken[:347] + "..."

    return spoken


def _missing_spoken(symbol: str) -> str:
    display = {"XAU": "l'or", "SPCX": "SpaceX"}.get(symbol, symbol)
    return f"Je n'ai pas encore de thèse exploitable pour {display}. Les données sont absentes ou trop anciennes."


def _stale_spoken(symbol: str, thesis: Dict[str, Any]) -> str:
    display = {"XAU": "l'or", "SPCX": "SpaceX"}.get(symbol, symbol)
    freshness = thesis.get("freshness", {})
    age = freshness.get("max_age_minutes", 0)
    age_str = f"{int(age)} minutes" if age < 120 else f"{int(age / 60)} heures"
    return f"Attention, la thèse pour {display} date de plus de {age_str}. Je peux la lire, mais elle doit être validée avant usage."


def format_summary_spoken(summaries: list[Dict[str, Any]]) -> str:
    """Format a summary of all symbols for voice."""
    if not summaries:
        return "Aucune thèse disponible pour le moment."

    bullish = [s for s in summaries if s.get("direction") == "bullish"]
    bearish = [s for s in summaries if s.get("direction") == "bearish"]

    parts = [f"{len(summaries)} actifs suivis."]

    if bullish:
        names = [{"XAU": "l'or", "SPCX": "SpaceX"}.get(s["symbol"], s["symbol"]) for s in bullish[:3]]
        parts.append(f"Tendance haussière sur {', '.join(names)}")

    if bearish:
        names = [{"XAU": "l'or", "SPCX": "SpaceX"}.get(s["symbol"], s["symbol"]) for s in bearish[:3]]
        parts.append(f"Tendance baissière sur {', '.join(names)}")

    parts.append("Surveillance uniquement sur tous les actifs.")

    spoken = ". ".join(parts)
    if len(spoken) > 350:
        spoken = spoken[:347] + "..."
    return spoken
