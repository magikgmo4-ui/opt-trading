"""Presentation Templates Engine.

Transforms structured market data into cognitively-optimized
human-readable output. Declarative: templates are data, not code.

Three output modes:
  - spoken: short natural French (2-6 phrases, < 400 chars)
  - display: full structured text with sections
  - cards: key-value pairs for UI cards
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# ── Translation maps ───────────────────────────────────────────────────────

DIR_FR = {"bullish": "Haussier", "bearish": "Baissier", "neutral": "Neutre", "wait": "En attente"}
DIR_SPOKEN = {"bullish": "haussier", "bearish": "baissier", "neutral": "neutre", "wait": "en attente"}
REGIME_FR = {"risk_on": "Risk-On", "risk_off": "Risk-Off", "expansion": "Expansion",
             "compression": "Compression", "distribution": "Distribution",
             "accumulation": "Accumulation", "panic": "Panique", "recovery": "Reprise"}
FRESH_FR = {"fresh": "Fraîches", "warm": "Acceptables", "stale": "Anciennes",
            "expired": "Expirées", "missing": "Absentes"}
SEVERITY_FR = {"high": "ÉLEVÉ", "moderate": "MODÉRÉ", "low": "Faible"}
GRADE_FR = {"excellent": "Excellent", "good": "Bon", "fair": "Acceptable",
            "poor": "Faible", "insufficient": "Insuffisant"}
ALIGN_FR = {"aligned_bullish": "Aligné haussier", "aligned_bearish": "Aligné baissier",
            "divergent": "Divergent", "neutral": "Neutre"}
PHASE_FR = {"markup": "Hausse", "markdown": "Baisse", "accumulation": "Accumulation",
            "distribution": "Distribution"}

DISPLAY_NAMES = {"XAU": "Or (Gold)", "SPCX": "SpaceX (SPCX)"}
SPOKEN_NAMES = {"XAU": "l'or", "SPCX": "SpaceX"}

# ── Data access ────────────────────────────────────────────────────────────

def _g(section: str, data: dict) -> dict:
    """Get a section from data, empty dict if missing."""
    if data is None:
        return {}
    d = data.get(section)
    return d if isinstance(d, dict) else {}


def _v(d: dict, *keys: str, default: Any = "?") -> Any:
    """Safely navigate nested dict keys."""
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d


# ── Section renderers ──────────────────────────────────────────────────────

def _executive_summary(data: dict, symbol: str) -> Tuple[str, str]:
    """Generate spoken + display executive summary."""
    thesis = data.get("thesis") or {}
    exec_data = data.get("executive") or {}
    reliability = data.get("reliability") or {}

    name_spoken = SPOKEN_NAMES.get(symbol, symbol)
    name_display = DISPLAY_NAMES.get(symbol, symbol)

    direction = _v(thesis, "action", "direction", default="neutral")
    confidence = _v(thesis, "confidence", default=50)
    rel_score = _v(reliability, "score", default=0)
    rel_grade = _v(reliability, "grade", default="?")
    regime = _v(exec_data, "market_regime", default="")
    leaders = _v(exec_data, "leaders", default=[])
    laggards = _v(exec_data, "laggards", default=[])

    dir_display = DIR_FR.get(direction, direction)
    dir_spoken = DIR_SPOKEN.get(direction, direction)
    regime_display = REGIME_FR.get(regime, regime)

    # Position
    canon = symbol.upper()
    if canon in leaders:
        position = "Leader"
    elif canon in laggards:
        position = "En retard"
    else:
        position = "Neutre"

    # --- Display ---
    lines = []
    lines.append(f"Analyse {name_display}")
    lines.append("─" * 50)
    lines.append("")
    lines.append("Résumé exécutif")
    lines.append("─" * 20)

    # Contextual summary paragraph
    ctx_narrative = _v(thesis, "context", "narrative", default="")
    tech_narrative = _v(thesis, "technical", "narrative", default="")
    if ctx_narrative and len(ctx_narrative) > 15:
        lines.append(ctx_narrative.split(".")[0].strip() + ".")
    elif tech_narrative and len(tech_narrative) > 15:
        lines.append(tech_narrative.split(".")[0].strip() + ".")
    else:
        lines.append(f"{name_display} en biais {dir_display.lower()} avec {confidence}% de confiance.")

    lines.append("")
    lines.append("Situation actuelle")
    lines.append("─" * 20)
    lines.append(f"  Biais              {dir_display}")
    lines.append(f"  Confiance          {confidence}%")
    if rel_score > 0:
        lines.append(f"  Fiabilité          {rel_score}% ({GRADE_FR.get(rel_grade, rel_grade)})")
    if regime:
        lines.append(f"  Régime marché      {regime_display}")
    if position:
        lines.append(f"  Position marché    {position}")

    # Setup info
    setups = _v(thesis, "technical", "active_setups", default=[])
    if setups:
        lines.append(f"  Setup dominant     {setups[0] if isinstance(setups[0], str) else setups[0].get('setup_id', '')}")

    display = "\n".join(lines)

    # --- Spoken ---
    parts = []
    if confidence >= 70:
        parts.append(f"{name_spoken} reste en biais {dir_spoken} avec une confiance élevée de {confidence}%")
    elif confidence >= 45:
        parts.append(f"{name_spoken} reste en biais {dir_spoken} avec une confiance modérée de {confidence}%")
    else:
        parts.append(f"{name_spoken} est en biais {dir_spoken} avec une confiance faible de {confidence}%")

    if canon in leaders:
        parts.append(f"il fait partie des leaders du marché")
    elif canon in laggards:
        parts.append(f"il est en position de faiblesse")

    if regime_display:
        parts.append(f"dans un régime {regime_display}")

    spoken = _join_spoken(parts)
    return spoken, display


def _supporting_evidence(data: dict) -> Tuple[str, str]:
    """What supports the current scenario."""
    thesis = data.get("thesis") or {}
    technical = _g("technical", thesis)
    flow = _g("flow", thesis)
    news = _g("news", thesis)

    evidence: List[str] = []

    # Technical evidence
    htf = _v(technical, "htf_bias", default="")
    ltf = _v(technical, "ltf_bias", default="")
    alignment = _v(technical, "alignment", default="")
    if htf == "bullish":
        evidence.append("Tendance de fond haussière")
    if ltf in ("bullish",):
        evidence.append("Structure court terme favorable")
    if alignment in ("aligned_bullish",):
        evidence.append("Timeframes alignées à la hausse")

    # VWAP
    vwap = _v(technical, "vwap", default=None)
    if vwap is not None:
        evidence.append("VWAP identifié et surveillé")

    # Flow evidence
    funding = _v(flow, "funding_rate", default=None)
    if funding is not None and funding < 0.01:
        evidence.append("Funding non excessif")
    elif funding is not None and funding > 0.05:
        evidence.append("Funding élevé — signal contrariant possible")

    oi = _v(flow, "open_interest", default=None)
    if oi is not None:
        evidence.append("Open Interest disponible")

    # News
    sentiment = _v(news, "sentiment", default="unknown")
    if sentiment == "positive":
        evidence.append("Sentiment news positif")
    elif sentiment == "negative":
        evidence.append("Sentiment news négatif — prudence")

    if not evidence:
        evidence.append("Données insuffisantes pour évaluation")

    display_lines = ["Ce qui soutient le scénario", "─" * 25]
    for e in evidence:
        display_lines.append(f"  • {e}")
    display = "\n".join(display_lines)

    spoken = f"Éléments favorables: {', '.join(evidence[:3])}."
    if len(spoken) > 200:
        spoken = spoken[:197] + "..."

    return spoken, display


def _opposing_evidence(data: dict) -> Tuple[str, str]:
    """What threatens the current scenario."""
    thesis = data.get("thesis") or {}
    technical = _g("technical", thesis)
    flow = _g("flow", thesis)
    risks = _v(thesis, "risks", default=[])
    executive = data.get("executive") or {}

    threats: List[str] = []

    # Technical threats
    alignment = _v(technical, "alignment", default="")
    if alignment == "divergent":
        threats.append("Divergence entre timeframes")
    htf = _v(technical, "htf_bias", default="")
    ltf = _v(technical, "ltf_bias", default="")
    if htf == "bearish" and ltf == "bearish":
        threats.append("Tendance baissière confirmée")

    # Flow threats
    ls_ratio = _v(flow, "long_short_ratio", default=None)
    if ls_ratio is not None and ls_ratio > 2.0:
        threats.append("Ratio Long/Short excessif — risque de squeeze")
    funding = _v(flow, "funding_rate", default=None)
    if funding is not None and abs(funding) > 0.05:
        threats.append("Funding rate extrême")

    # Risk items
    for r in risks[:3]:
        desc = r.get("description", "")
        if desc and len(desc) > 5:
            threats.append(desc[:100])

    # Lagggard risk
    canon = data.get("symbol", "").upper() if isinstance(data, dict) else ""
    laggards = executive.get("laggards", [])
    if canon in laggards:
        threats.append("Position de faiblesse dans le marché")

    if not threats:
        threats.append("Aucune menace majeure identifiée")

    display_lines = ["Ce qui menace le scénario", "─" * 25]
    for t in threats:
        display_lines.append(f"  • {t}")
    display = "\n".join(display_lines)

    spoken = f"Points de vigilance: {', '.join(threats[:2])}."
    if len(spoken) > 200:
        spoken = spoken[:197] + "..."
    return spoken, display


def _scenarios_section(data: dict) -> Tuple[str, str]:
    """Probability scenarios."""
    thesis = data.get("thesis") or {}
    probs = _g("probabilities", thesis)
    bull = probs.get("bull", 33)
    range_v = probs.get("range", 34)
    bear = probs.get("bear", 33)

    if bull > bear and bull > range_v:
        primary = "Continuation haussière"
    elif bear > bull and bear > range_v:
        primary = "Reversal baissier"
    else:
        primary = "Range / consolidation"

    display_lines = ["Scénarios", "─" * 25]
    display_lines.append(f"  Continuation haussière   {bull}%")
    display_lines.append(f"  Range / consolidation    {range_v}%")
    display_lines.append(f"  Reversal baissier        {bear}%")
    display_lines.append(f"  Scénario principal: {primary}")
    display = "\n".join(display_lines)

    spoken = f"Scénario principal: {primary} ({max(bull, bear, range_v)}%). "
    spoken += "Surveillance uniquement."
    return spoken, display


def _setups_section(data: dict) -> Tuple[str, str]:
    """Active setups detail."""
    thesis = data.get("thesis") or {}
    technical = _g("technical", thesis)
    setups = _v(technical, "active_setups", default=[])
    supports = _v(technical, "key_support", default=[])
    resistances = _v(technical, "key_resistance", default=[])

    display_lines = ["Setups actifs", "─" * 25]
    if setups:
        for s in setups[:3]:
            display_lines.append(f"  • {s}")
    else:
        display_lines.append("  Aucun setup actif identifié")

    if supports:
        display_lines.append(f"  Supports: {', '.join(str(int(s)) for s in supports[:3])}")
    if resistances:
        display_lines.append(f"  Résistances: {', '.join(str(int(r)) for r in resistances[:3])}")

    display = "\n".join(display_lines)
    spoken = f"Setups actifs: {len(setups)}. Niveaux clés à surveiller." if setups else "Aucun setup actif."
    return spoken, display


def _watchlist_section(data: dict) -> Tuple[str, str]:
    """What to watch."""
    thesis = data.get("thesis") or {}
    executive = data.get("executive") or {}

    watch = []

    # Always monitor these
    watch.append("Évolution du biais directionnel")
    watch.append("Niveaux de support et résistance")
    watch.append("Volume et flux de capitaux")

    # Executive context
    regime = executive.get("market_regime", "")
    if regime in ("risk_on", "expansion"):
        watch.append("Signes de distribution ou ralentissement")
    elif regime in ("risk_off", "panic"):
        watch.append("Signes de stabilisation ou reprise")

    display_lines = ["À surveiller", "─" * 25]
    for w in watch:
        display_lines.append(f"  • {w}")
    display = "\n".join(display_lines)

    spoken = f"Points à surveiller: {', '.join(watch[:3])}."
    return spoken, display


def _action_section(data: dict) -> Tuple[str, str]:
    """Always monitor-only action."""
    thesis = data.get("thesis") or {}
    action = _g("action", thesis)
    narrative = _v(action, "narrative", default="")
    levels = _v(action, "key_levels", default=[])

    effective_narrative = narrative if narrative and len(narrative) > 10 else "Le scénario principal reste valide mais nécessite confirmation avant toute décision."

    display_lines = ["Action", "─" * 25]
    display_lines.append(f"  {effective_narrative}")
    display_lines.append("")
    display_lines.append("  Mode: Surveillance uniquement.")
    display_lines.append("  Aucun ordre automatique n'est émis.")
    if levels:
        display_lines.append("")
        display_lines.append("  Niveaux à surveiller:")
        for lv in levels[:6]:
            display_lines.append(f"  • {lv}")
    display = "\n".join(display_lines)

    spoken = f"Action recommandée: surveillance uniquement. {effective_narrative[:120]}"
    return spoken, display


# ── Join helpers ───────────────────────────────────────────────────────────

def _join_spoken(parts: List[str]) -> str:
    """Join spoken parts into flowing French sentences."""
    cleaned = [p.strip().rstrip(".") for p in parts if p.strip()]
    text = ". ".join(cleaned) + "."
    if len(text) > 400:
        text = text[:397] + "..."
    return text


# ── Template renderer ──────────────────────────────────────────────────────

def render_asset_analysis(symbol: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Render the full Asset Analysis V2 template for a symbol.

    Args:
        symbol: Canonical symbol (BTC, XAU, SPCX, etc.)
        data: Optional pre-gathered data. If None, gathers from engines.

    Returns:
        Dict with spoken_text, display_text, cards.
    """
    if data is None:
        from modules.voice_operator.formatters.asset_state_formatter import _gather_asset_state
        data = _gather_asset_state(symbol)

    if data is None or data.get("thesis") is None:
        name = SPOKEN_NAMES.get(symbol, symbol)
        return {
            "spoken_text": f"Je n'ai pas encore d'analyse exploitable pour {name}. Les données sont absentes ou trop anciennes.",
            "display_text": f"Analyse {DISPLAY_NAMES.get(symbol, symbol)}\nStatut: Non disponible.",
            "cards": [{"label": "Statut", "value": "Indisponible"}],
        }

    # Stale check
    thesis = data.get("thesis") or {}
    freshness = thesis.get("freshness") or {}
    fresh_state = _v(freshness, "overall", default="fresh")
    if fresh_state in ("stale", "expired"):
        name = SPOKEN_NAMES.get(symbol, symbol)
        age = _v(freshness, "max_age_minutes", default=0)
        age_str = f"{int(age)} minutes" if age < 120 else f"{int(age/60)} heures"
        return {
            "spoken_text": f"Attention, la thèse pour {name} date de plus de {age_str}. Je peux la lire, mais elle doit être validée avant usage.",
            "display_text": f"Analyse {DISPLAY_NAMES.get(symbol, symbol)}\nStatut: Données anciennes ({age_str}). À valider avant usage.",
            "cards": [{"label": "Statut", "value": f"Ancien ({age_str})"}],
        }

    # Gather all sections
    sections: List[Tuple[str, str, str]] = []  # (name, spoken, display)
    all_display_parts: List[str] = []
    spoken_parts: List[str] = []

    # 1. Executive Summary
    s_sp, s_disp = _executive_summary(data, symbol)
    spoken_parts.append(s_sp)
    all_display_parts.append(s_disp)
    all_display_parts.append("")

    # 2. Supporting evidence
    s_sp, s_disp = _supporting_evidence(data)
    all_display_parts.append(s_disp)
    all_display_parts.append("")

    # 3. Opposing evidence
    s_sp, s_disp = _opposing_evidence(data)
    all_display_parts.append(s_disp)
    all_display_parts.append("")

    # 4. Setups
    s_sp, s_disp = _setups_section(data)
    all_display_parts.append(s_disp)
    all_display_parts.append("")

    # 5. Scenarios
    s_sp, s_disp = _scenarios_section(data)
    all_display_parts.append(s_disp)
    all_display_parts.append("")

    # 6. Watchlist
    s_sp, s_disp = _watchlist_section(data)
    all_display_parts.append(s_disp)
    all_display_parts.append("")

    # 7. Action (spoken simple, display full)
    s_sp, s_disp = _action_section(data)
    spoken_parts.append("Action recommandée: surveillance uniquement")
    all_display_parts.append(s_disp)

    # Assemble
    spoken = _join_spoken(spoken_parts)
    display = "\n".join(all_display_parts)

    # Clean underscores
    for raw, clean in [("risk_on", "Risk-On"), ("risk_off", "Risk-Off"),
                        ("monitor_only", "surveillance uniquement"),
                        ("bearish", "baissier"), ("bullish", "haussier")]:
        display = display.replace(raw, clean)

    # Cards
    thesis = data.get("thesis") or {}
    reliability = data.get("reliability") or {}
    executive = data.get("executive") or {}
    cards = [
        {"label": "Biais", "value": DIR_FR.get(_v(thesis, "action", "direction", default="?"), "?")},
        {"label": "Confiance", "value": f"{_v(thesis, 'confidence', default='?')}%"},
        {"label": "Fiabilité", "value": f"{_v(reliability, 'score', default='?')}/100" if reliability else "?"},
        {"label": "Régime", "value": REGIME_FR.get(_v(executive, "market_regime", default="?"), "?")},
        {"label": "Action", "value": "Surveillance uniquement"},
        {"label": "Fraîcheur", "value": FRESH_FR.get(_v(thesis, "freshness", "overall", default="?"), "?")},
    ]

    return {
        "spoken_text": spoken,
        "display_text": display,
        "cards": cards,
    }
