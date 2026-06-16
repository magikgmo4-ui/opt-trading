"""
Voice Operator — Executive Voice Formatter (PR8).

Short natural French spoken text from executive data.
No JSON. No underscores. No field names.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def _s(d: dict, *keys: str, default: Any = "?") -> Any:
    for k in keys:
        if isinstance(d, dict) and k in d:
            return d[k]
    return default


def format_briefing_spoken(data: Optional[Dict[str, Any]]) -> str:
    if data is None:
        return "Je n'ai pas encore de briefing marché exploitable. Les données sont absentes ou trop anciennes."

    regime = _s(data, "market_regime", default="inconnu")
    leaders = _s(data, "leaders", default=[])
    risks = _s(data, "top_risks", default=[])
    opps = _s(data, "top_opportunities", default=[])

    regime_fr = {"risk_on": "Risk-On", "risk_off": "Risk-Off", "expansion": "Expansion",
                 "compression": "Compression", "distribution": "Distribution",
                 "accumulation": "Accumulation", "panic": "Panique", "recovery": "Reprise"}.get(regime, regime)

    parts = [f"Le marché est actuellement en régime {regime_fr}"]

    conf = _s(data, "regime_confidence", default=50)
    if conf >= 70:
        parts[0] += f", avec une confiance élevée de {conf}%"
    elif conf >= 45:
        parts[0] += f", avec une confiance modérée de {conf}%"

    if leaders:
        leader_names = leaders[:3]
        parts.append(f"Les actifs leaders sont {', '.join(leader_names)}")

    laggards = _s(data, "laggards", default=[])
    if laggards:
        parts.append(f"Les actifs les plus faibles sont {', '.join(laggards[:2])}")

    if risks:
        parts.append(f"Le principal risque: {risks[0][:120]}")

    if opps:
        parts.append(f"Opportunité principale: {opps[0][:100]}")

    parts.append("Action recommandée: surveillance uniquement.")

    spoken = ". ".join(parts)
    if len(spoken) > 400:
        spoken = spoken[:397] + "..."
    return spoken


def format_regime_spoken(data: Optional[Dict[str, Any]]) -> str:
    if data is None:
        return "Je n'ai pas d'information sur le régime de marché actuel."

    regime = _s(data, "regime", default="inconnu")
    conf = _s(data, "confidence", default=50)
    risk = _s(data, "risk_score", default=50)
    narrative = _s(data, "narrative", default="")

    regime_fr = {"risk_on": "Risk-On", "risk_off": "Risk-Off", "expansion": "Expansion",
                 "compression": "Compression", "distribution": "Distribution",
                 "accumulation": "Accumulation", "panic": "Panique", "recovery": "Reprise"}.get(regime, regime)

    risk_label = "élevé" if risk >= 70 else "modéré" if risk >= 40 else "faible"
    spoken = f"Régime {regime_fr} détecté avec {conf}% de confiance. Niveau de risque {risk_label} ({risk}/100)."

    if narrative and len(narrative) > 10:
        first = narrative.split(".")[0].strip()
        if len(first) > 15:
            spoken += f" {first}."

    spoken += " Surveillance uniquement."
    return spoken


def format_risks_spoken(data: Optional[Dict[str, Any]]) -> str:
    if data is None:
        return "Je n'ai pas d'information sur les risques actuels."

    risks = _s(data, "top_risks", default=[])
    if not risks:
        return "Aucun risque majeur identifié pour le moment."

    parts = [f"{len(risks)} risque(s) identifié(s)"]
    for r in risks[:3]:
        parts.append(r[:120])

    spoken = ". ".join(parts) + ". Surveillance uniquement."
    if len(spoken) > 350:
        spoken = spoken[:347] + "..."
    return spoken


def format_leaders_spoken(data: Optional[Dict[str, Any]]) -> str:
    if data is None:
        return "Je n'ai pas d'information sur les leaders de marché."

    leaders = _s(data, "leaders", default=[])
    laggards = _s(data, "laggards", default=[])

    parts = []
    if leaders:
        parts.append(f"Leaders: {', '.join(l.get('symbol', l) if isinstance(l, dict) else l for l in leaders[:3])}")
    if laggards:
        parts.append(f"Actifs faibles: {', '.join(l.get('symbol', l) if isinstance(l, dict) else l for l in laggards[:3])}")

    if not parts:
        return "Pas de données sur les leaders pour le moment."

    return ". ".join(parts) + ". Surveillance uniquement."
