"""
Voice Operator — Executive Text Formatter (PR8).

Detailed French display text from executive data.
No JSON. No code. Clean sections.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def _s(d: dict, *keys: str, default: Any = "?") -> Any:
    for k in keys:
        if isinstance(d, dict) and k in d:
            return d[k]
    return default


def format_briefing_text(data: Optional[Dict[str, Any]]) -> str:
    if data is None:
        return "Briefing marché\n──────────────\nStatut: Non disponible.\nLes données sont absentes ou trop anciennes."

    regime = _s(data, "market_regime", default="?")
    conf = _s(data, "regime_confidence", default=0)
    global_conf = _s(data, "overall_confidence", default=0)
    leaders = _s(data, "leaders", default=[])
    laggards = _s(data, "laggards", default=[])
    summary = _s(data, "summary", default="")
    changed = _s(data, "what_changed", default="")
    watch = _s(data, "what_to_watch", default="")
    risks = _s(data, "top_risks", default=[])
    opps = _s(data, "top_opportunities", default=[])

    regime_fr = {"risk_on": "Risk-On", "risk_off": "Risk-Off", "expansion": "Expansion",
                 "compression": "Compression", "distribution": "Distribution",
                 "accumulation": "Accumulation", "panic": "Panique", "recovery": "Reprise"}.get(regime, regime)

    lines = []
    lines.append("Briefing marché")
    lines.append("─" * 30)
    lines.append(f"Régime: {regime_fr}  |  Confiance: {conf}%  |  Globale: {global_conf}%")
    lines.append("")

    if summary:
        lines.append("Résumé")
        lines.append("─" * 15)
        lines.append(summary)
        lines.append("")

    if leaders:
        lines.append(f"Leaders: {', '.join(leaders)}")
    if laggards:
        lines.append(f"Actifs faibles: {', '.join(laggards)}")
    lines.append("")

    if risks:
        lines.append("Risques")
        lines.append("─" * 10)
        for r in risks:
            lines.append(f"  • {r}")
        lines.append("")

    if opps:
        lines.append("Opportunités")
        lines.append("─" * 10)
        for o in opps:
            lines.append(f"  • {o}")
        lines.append("")

    if changed:
        lines.append("Ce qui a changé")
        lines.append("─" * 10)
        lines.append(changed)
        lines.append("")

    if watch:
        lines.append("À surveiller")
        lines.append("─" * 10)
        lines.append(watch)
        lines.append("")

    lines.append("Mode: Surveillance uniquement. Aucun ordre automatique.")

    result = "\n".join(lines)
    # Final cleanup: replace any remaining underscores in the text
    for raw, clean in [("risk_on", "Risk-On"), ("risk_off", "Risk-Off"),
                        ("monitor_only", "surveillance uniquement"),
                        ("bearish", "baissier"), ("bullish", "haussier")]:
        result = result.replace(raw, clean)
    return result
