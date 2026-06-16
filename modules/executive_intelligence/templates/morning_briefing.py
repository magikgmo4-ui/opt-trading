"""
Morning Briefing Template — PR10.

Generates an automatic daily market briefing combining:
  - Market regime detection
  - Cross-asset leaderboard
  - Active trading setups
  - Top risks and opportunities
  - What changed since yesterday
  - Voice-friendly compact output

No trade execution. Monitor-only.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from .asset_analysis import (_v, _join_spoken, REGIME_FR, SPOKEN_NAMES, DISPLAY_NAMES)


def _gather_morning_data() -> Dict[str, Any]:
    """Gather all data needed for the morning briefing."""
    data: Dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "regime": None,
        "leaders": [],
        "laggards": [],
        "setups": [],
        "changes": [],
        "top_risks": [],
        "top_opportunities": [],
        "reliability": {},
    }

    # Regime + leaders/laggards
    try:
        from modules.desk_pro.service.executive_reader import (
            get_executive,
            get_executive_regime,
            get_executive_leaders,
            get_executive_risks,
        )
        exec_data = get_executive()
        if exec_data:
            data["regime"] = exec_data.get("market_regime", "unknown")
            data["leaders"] = exec_data.get("leaders", [])
            data["laggards"] = exec_data.get("laggards", [])
            data["top_risks"] = exec_data.get("top_risks", [])
            data["top_opportunities"] = exec_data.get("top_opportunities", [])

        regime_data = get_executive_regime()
        if regime_data:
            data["regime_confidence"] = regime_data.get("confidence", 50)
            data["risk_score"] = regime_data.get("risk_score", 50)
    except Exception:
        pass

    # Setups
    try:
        from .setup_card import render_setup_cards
        setup_result = render_setup_cards()
        data["setups"] = setup_result.get("cards", [])
        data["market_summary"] = setup_result.get("market_summary", {})
    except Exception:
        pass

    # Changes
    try:
        from modules.executive_intelligence.narrative_memory import detect_changes, summarize_changes
        changes = detect_changes()
        # Filter out initialization
        real_changes = [c for c in changes if c.field != "initialization"]
        data["changes"] = [
            {"field": c.field, "symbol": c.symbol, "description": c.description, "magnitude": c.magnitude}
            for c in real_changes
        ]
        data["change_summary"] = summarize_changes(changes)
    except Exception:
        data["changes"] = []
        data["change_summary"] = "Aucun changement détecté."

    # Leaderboard for reliability overview
    try:
        from modules.executive_intelligence.cross_asset_engine import build_leaderboard
        board = build_leaderboard()
        bullish = sum(1 for e in board if e.direction == "bullish")
        bearish = sum(1 for e in board if e.direction == "bearish")
        data["bullish_count"] = bullish
        data["bearish_count"] = bearish
        data["total_assets"] = len(board)
        avg_conf = sum(e.confidence for e in board) / len(board) if board else 50
        data["avg_confidence"] = int(avg_conf)
    except Exception:
        data["bullish_count"] = 0
        data["bearish_count"] = 0

    return data


def render_morning_briefing() -> Dict[str, Any]:
    """Generate the morning briefing.

    Returns spoken_text (compact), display_text (full), cards[].
    """
    data = _gather_morning_data()
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%d %B %Y")

    # ── Spoken ─────────────────────────────────────────────────────────
    parts = []

    # Market overview
    regime = data.get("regime", "unknown")
    regime_fr = REGIME_FR.get(regime, regime)
    bullish = data.get("bullish_count", 0)
    total = data.get("total_assets", 9)

    parts.append(f"Briefing du {date_str}")
    parts.append(f"Marché en régime {regime_fr}")

    if bullish >= 6:
        parts.append(f"tendance haussière dominante avec {bullish} actifs sur {total}")
    elif bullish >= 4:
        parts.append(f"marché partagé avec {bullish} actifs haussiers sur {total}")
    else:
        parts.append(f"marché prudent avec seulement {bullish} actifs haussiers sur {total}")

    # Leaders
    leaders = data.get("leaders", [])
    if leaders:
        leader_names = [SPOKEN_NAMES.get(l, l) for l in leaders[:3]]
        parts.append(f"Leaders: {', '.join(leader_names)}")

    # Setups
    setups = data.get("setups", [])
    if setups:
        best = setups[0]
        sym = best.get("symbol", "?")
        sym_spoken = SPOKEN_NAMES.get(sym, sym)
        parts.append(
            f"Setup prioritaire: {sym_spoken} {best.get('setup', '')}, "
            f"grade {best.get('grade', '?')}, probabilité {best.get('probability', '?')}%"
        )

    # Risks
    risks = data.get("top_risks", [])
    if risks:
        parts.append(f"Risque principal: {risks[0][:100]}")

    # Changes
    changes = data.get("changes", [])
    major_changes = [c for c in changes if c.get("magnitude") == "major"]
    if major_changes:
        parts.append(f"Changement majeur: {major_changes[0].get('description', '')[:100]}")

    parts.append("Surveillance uniquement. Aucun ordre automatique.")

    spoken = _join_spoken(parts)
    if len(spoken) > 600:
        spoken = spoken[:597] + "..."

    # ── Display ────────────────────────────────────────────────────────
    display_lines = []
    display_lines.append(f"Briefing — {date_str}")
    display_lines.append("═" * 50)
    display_lines.append("")

    # Market state
    display_lines.append("État du marché")
    display_lines.append("─" * 30)
    display_lines.append(f"  Régime:          {regime_fr}")
    display_lines.append(f"  Confiance:       {data.get('regime_confidence', '?')}%")
    display_lines.append(f"  Risque:          {data.get('risk_score', '?')}/100")
    display_lines.append(f"  Actifs haussiers: {bullish}/{total}")
    display_lines.append(f"  Actifs baissiers: {data.get('bearish_count', '?')}/{total}")
    display_lines.append(f"  Confiance moyenne: {data.get('avg_confidence', '?')}%")
    display_lines.append("")

    # Leaders / Laggards
    if leaders:
        display_lines.append(f"Leaders: {', '.join(leaders)}")
    laggards = data.get("laggards", [])
    if laggards:
        display_lines.append(f"En retard: {', '.join(laggards)}")
    display_lines.append("")

    # Active setups
    display_lines.append("Setups actifs")
    display_lines.append("─" * 30)
    if setups:
        for s in setups[:5]:
            sym = s.get("symbol", "?")
            grade = s.get("grade", "?")
            prob = s.get("probability", "?")
            bias = s.get("bias", "?")
            entry = s.get("entry_zone", "?")
            sl = s.get("stop_loss", "?")
            sl_str = f"{sl:.0f}" if isinstance(sl, (int, float)) else str(sl)
            display_lines.append(f"  {sym:6s} | {grade:3s} | {prob}% | {bias:5s} | Entrée {entry} | SL {sl_str}")
    else:
        display_lines.append("  Aucun setup actif.")
    display_lines.append("")

    # Top risks
    display_lines.append("Risques principaux")
    display_lines.append("─" * 30)
    for r in risks[:4]:
        display_lines.append(f"  • {r}")
    if not risks:
        display_lines.append("  Aucun risque majeur identifié.")
    display_lines.append("")

    # Opportunities
    opps = data.get("top_opportunities", [])
    if opps:
        display_lines.append("Opportunités")
        display_lines.append("─" * 30)
        for o in opps[:4]:
            display_lines.append(f"  • {o}")
        display_lines.append("")

    # Changes
    display_lines.append("Ce qui a changé")
    display_lines.append("─" * 30)
    if changes:
        for c in changes[:5]:
            display_lines.append(f"  • {c.get('description', '')}")
    else:
        display_lines.append("  Aucun changement significatif.")
    display_lines.append("")

    display_lines.append("Mode: Surveillance uniquement. Aucun ordre automatique.")
    display = "\n".join(display_lines)

    # ── Cards ──────────────────────────────────────────────────────────
    cards = [
        {"label": "Régime", "value": regime_fr},
        {"label": "Confiance", "value": f"{data.get('regime_confidence', '?')}%"},
        {"label": "Risque", "value": f"{data.get('risk_score', '?')}/100"},
        {"label": "Setups actifs", "value": str(len(setups))},
        {"label": "Haussiers", "value": f"{bullish}/{total}"},
        {"label": "Mode", "value": "Surveillance uniquement"},
    ]

    return {
        "spoken_text": spoken,
        "display_text": display,
        "cards": cards,
        "generated_at": data["generated_at"],
    }
