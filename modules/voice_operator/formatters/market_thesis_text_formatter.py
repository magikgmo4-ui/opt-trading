"""
Voice Operator — Market Thesis Text Formatter (detailed display).

Produces a clean, structured French text output.
No JSON. No code. No raw field names.
Sections: Summary, Context, Technical, Flow, News, Risks, Probabilities, Action, Sources, Freshness.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def _safe(d: dict, *keys: str, default: Any = "?") -> Any:
    for k in keys:
        if isinstance(d, dict) and k in d:
            return d[k]
    return default


def format_display(symbol: str, thesis: Optional[Dict[str, Any]]) -> str:
    """Format a thesis into detailed French display text."""
    display_sym = {"XAU": "Or (XAU)", "SPCX": "SpaceX (SPCX)"}.get(symbol, symbol)

    if thesis is None:
        return f"""Analyse {display_sym}
─────────────────────────────
Statut: Thèse non disponible.
Les données sont absentes ou trop anciennes.
Action: Relancer le build si autorisé.
"""

    action = thesis.get("action", {})
    ctx = thesis.get("context", {})
    technical = thesis.get("technical", {})
    flow = thesis.get("flow", {})
    news = thesis.get("news", {})
    probs = thesis.get("probabilities", {})
    risks = thesis.get("risks", [])
    sources = thesis.get("sources", [])
    freshness = thesis.get("freshness", {})
    meta = thesis.get("metadata", {})
    confidence = thesis.get("confidence", 50)

    direction = action.get("direction", "neutral")
    dir_fr = {"bullish": "Haussier", "bearish": "Baissier", "neutral": "Neutre", "wait": "En attente"}.get(direction, direction)

    # Translation maps
    _regime = {"risk_on": "Risk-on", "risk_off": "Risk-off", "neutral": "Neutre", "unknown": "?"}
    _dxy = {"bullish": "Haussier", "bearish": "Baissier", "neutral": "Stable", "unknown": "?"}
    _vix = {"low": "Bas", "normal": "Normal", "elevated": "Élevé", "high": "Très élevé", "unknown": "?"}
    _phase = {"accumulation": "Accumulation", "markup": "Hausse", "distribution": "Distribution", "markdown": "Baisse", "unknown": "?"}
    _bias = {"bullish": "Haussier", "bearish": "Baissier", "neutral": "Neutre"}
    _align = {"aligned_bullish": "Aligné haussier", "aligned_bearish": "Aligné baissier", "divergent": "Divergent", "neutral": "Neutre"}

    # ── Header ─────────────────────────────────────────────────────────
    lines = []
    lines.append(f"Analyse {display_sym}")
    lines.append("─" * 40)
    lines.append(f"Biais: {dir_fr}  |  Confiance: {confidence}%  |  Mode: Surveillance uniquement")
    lines.append(f"Généré le: {_safe(meta, 'generated_at', default='?')}")
    lines.append("")

    # ── One-liner ─────────────────────────────────────────────────────
    one_liner = action.get("voice_one_liner", "")
    if one_liner:
        lines.append(one_liner)
        lines.append("")

    # ── Context ───────────────────────────────────────────────────────
    lines.append("Contexte")
    lines.append("─" * 20)
    ctx_narr = _safe(ctx, "narrative", default="Données insuffisantes.")
    lines.append(ctx_narr)
    regime = _regime.get(_safe(ctx, "macro_regime", default="?"), "?")
    dxy = _dxy.get(_safe(ctx, "dxy_trend", default="?"), "?")
    vix = _vix.get(_safe(ctx, "vix_state", default="?"), "?")
    phase = _phase.get(_safe(ctx, "market_phase", default="?"), "?")
    lines.append(f"  Régime: {regime}  ·  DXY: {dxy}  ·  VIX: {vix}  ·  Phase: {phase}")
    lines.append("")

    # ── Technical ─────────────────────────────────────────────────────
    lines.append("Analyse technique")
    lines.append("─" * 20)
    tech_narr = _safe(technical, "narrative", default="Données insuffisantes.")
    lines.append(tech_narr)
    htf = _bias.get(_safe(technical, "htf_bias", default="?"), "?")
    ltf = _bias.get(_safe(technical, "ltf_bias", default="?"), "?")
    align = _align.get(_safe(technical, "alignment", default="?"), "?")
    lines.append(f"  HTF: {htf}  ·  LTF: {ltf}  ·  Alignement: {align}")
    lines.append("")

    # ── Flow ──────────────────────────────────────────────────────────
    lines.append("Flux et positionnement")
    lines.append("─" * 20)
    flow_narr = _safe(flow, "narrative", default="Données insuffisantes.")
    lines.append(flow_narr)
    lines.append("")

    # ── News ──────────────────────────────────────────────────────────
    lines.append("Actualité et sentiment")
    lines.append("─" * 20)
    news_narr = _safe(news, "narrative", default="Données insuffisantes.")
    lines.append(news_narr)
    lines.append("")

    # ── Risks ─────────────────────────────────────────────────────────
    lines.append("Risques identifiés")
    lines.append("─" * 20)
    if risks:
        for r in risks:
            sev = r.get("severity", "?")
            sev_fr = {"high": "ÉLEVÉ", "moderate": "MODÉRÉ", "low": "Faible"}.get(sev, sev)
            desc = r.get("description", "")
            lines.append(f"  [{sev_fr}] {desc}")
    else:
        lines.append("  Aucun risque significatif identifié.")
    lines.append("")

    # ── Probabilities ─────────────────────────────────────────────────
    lines.append("Probabilités directionnelles")
    lines.append("─" * 20)
    bull = probs.get("bull", 33)
    range_v = probs.get("range", 34)
    bear = probs.get("bear", 33)
    if bull > bear and bull > range_v:
        prob_bias = "haussier"
    elif bear > bull and bear > range_v:
        prob_bias = "baissier"
    else:
        prob_bias = "neutre"
    lines.append(f"  Biais {prob_bias} — Haussier {bull}%  ·  Range {range_v}%  ·  Baissier {bear}%")
    lines.append("")

    # ── Action ────────────────────────────────────────────────────────
    lines.append("Recommandation")
    lines.append("─" * 20)
    act_narr = _safe(action, "narrative", default="Surveillance uniquement.")
    lines.append(act_narr)
    levels = action.get("key_levels", [])
    if levels:
        lines.append("  Niveaux à surveiller:")
        for lv in levels[:6]:
            lines.append(f"  • {lv}")
    lines.append("")

    # ── Sources ───────────────────────────────────────────────────────
    lines.append("Sources de données")
    lines.append("─" * 20)
    if sources:
        for s in sources[:8]:
            name = s.get("name", "?")
            status = s.get("status", "?")
            status_fr = {"used": "✓", "stale": "≈", "missing": "✗"}.get(status, status)
            age = s.get("age_minutes")
            age_str = f" ({age:.0f}min)" if age is not None else ""
            lines.append(f"  {status_fr} {name}{age_str}")
    else:
        lines.append("  Aucune source disponible.")
    lines.append("")

    # ── Freshness ─────────────────────────────────────────────────────
    fresh_overall = _safe(freshness, "overall", default="?")
    max_age = _safe(freshness, "max_age_minutes", default=0)
    src_count = _safe(freshness, "source_count", default=0)
    fresh_count = _safe(freshness, "fresh_count", default=0)
    fresh_fr = {"fresh": "Fraîches", "stale": "Anciennes", "partial": "Partielles", "expired": "Expirées"}.get(fresh_overall, fresh_overall)
    lines.append(f"Fraîcheur: {fresh_fr}  ·  {fresh_count}/{src_count} sources à jour  ·  Âge max {max_age:.0f}min")

    return "\n".join(lines)


def format_summary_display(summaries: list[Dict[str, Any]]) -> str:
    """Format a summary of all symbols for display."""
    if not summaries:
        return "Aucune thèse disponible."

    lines = ["Résumé des thèses de marché", "─" * 30, ""]
    for s in summaries:
        sym = s["symbol"]
        direction = s.get("direction", "?")
        dir_fr = {"bullish": "▲", "bearish": "▼", "neutral": "■", "wait": "⏳"}.get(direction, "?")
        conf = s.get("confidence", 0)
        one_liner = s.get("one_liner", "")
        freshness = s.get("freshness", "?")

        # Truncate one_liner
        if len(one_liner) > 100:
            one_liner = one_liner[:97] + "..."

        lines.append(f"  {dir_fr} {sym:6s}  confiance {conf}%  {freshness}")
        if one_liner:
            lines.append(f"     {one_liner}")
        lines.append("")

    return "\n".join(lines)
