"""
Setup Card Template V1 — Canonical Voice Operator format.

Produces standardized setup cards for active trading setups.
Each card follows the exact canonical field structure:
  asset, asset_type, setup, timeframe, status, grade, score,
  probability, bias, price, vwap, support, resistance,
  entry_trigger, entry_zone, stop_loss, invalidation,
  tp1, tp2, tp3, risk_reward, confirmation, risk_flags, action

Also produces compact spoken + display text.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from .asset_analysis import (_g, _v, _join_spoken, DIR_FR, DIR_SPOKEN,
                               REGIME_FR, SPOKEN_NAMES, DISPLAY_NAMES)

# ── Asset type mapping ─────────────────────────────────────────────────────

ASSET_TYPES = {
    "BTC": "Crypto perp", "ETH": "Crypto perp", "SOL": "Crypto perp", "XRP": "Crypto perp",
    "XAU": "Commodity / CFD",
    "SPCX": "Equity / IPO momentum",
    "NVDA": "Equity / Semiconductor", "AVGO": "Equity / Semiconductor", "MU": "Equity / Semiconductor",
}


# ── Data gathering ─────────────────────────────────────────────────────────

def _gather_all_setups() -> List[Dict[str, Any]]:
    """Gather thesis data for all 9 canonical symbols, return active setups."""
    symbols = ["BTC", "ETH", "SOL", "XRP", "XAU", "SPCX", "NVDA", "AVGO", "MU"]
    setups: List[Dict[str, Any]] = []

    for sym in symbols:
        try:
            from modules.desk_pro.service.market_thesis_reader import get_market_thesis
            thesis = get_market_thesis(sym)
            if thesis is None:
                continue
        except Exception:
            continue

        # ── Enrich with live data ───────────────────────────────────
        try:
            from .live_data_binder import bind_live_data
            live = bind_live_data(sym, thesis)
        except Exception:
            live = {"has_data": True, "price": None, "cdp_triggers": [],
                    "reliability": {}, "leaderboard": {}, "freshness": {"is_stale": False, "stale_sources": []}}

        action = thesis.get("action", {})
        technical = thesis.get("technical", {})
        flow = thesis.get("flow", {})
        probs = thesis.get("probabilities", {})

        direction = action.get("direction", "neutral")
        if direction in ("neutral", "wait"):
            continue

        # Skip if no active setups
        active = technical.get("active_setups", [])
        if not active:
            continue

        # Extract setup details
        setup_name = active[0] if isinstance(active[0], str) else active[0].get("setup_id", "unknown")
        grade = _derive_grade(thesis, direction)
        score = _derive_score(thesis)
        prob = max(probs.get("bull", 0), probs.get("bear", 0))

        # Price — prefer live data
        price = live.get("price") or _derive_price(thesis)

        # VWAP
        vwap = technical.get("vwap")

        # Levels
        supports = technical.get("key_support", [])
        resistances = technical.get("key_resistance", [])

        # Entry / SL / TP
        cdp_triggers = live.get("cdp_triggers", [])
        active_cdp = [t["event"] for t in cdp_triggers if t.get("active")] if cdp_triggers else []
        entry_trigger = _derive_entry_trigger(setup_name, direction, vwap, supports, resistances, active_cdp)
        entry_zone = _derive_entry_zone(supports, resistances, direction, price)
        sl = _derive_sl(supports, resistances, direction)
        tps = _derive_tps(resistances, supports, direction, price)

        # Timeframe
        htf = technical.get("htf_bias", "")
        ltf = technical.get("ltf_bias", "")
        timeframe = f"{'M15' if ltf == 'bearish' else 'H1'} / {'H4' if htf == 'bearish' else 'H1'}"

        # Status
        if grade in ("A+", "A", "A-"):
            status = "Prioritaire"
        elif grade in ("B+", "B", "B-"):
            status = "Watch"
        else:
            status = "Attente confirmation"

        # R/R
        rr = _derive_rr(price, sl, tps)

        # Risk flags — enrich with live data context
        risks = thesis.get("risks", [])
        risk_parts = []
        if risks:
            risk_parts.append(risks[0].get("description", "")[:80])
        # Add reliability context
        rel = live.get("reliability", {})
        if rel.get("sample_size", 0) < 10:
            risk_parts.append("Fiabilité insuffisante (peu d'historique)")
        # Add stale warning
        fresh = live.get("freshness", {})
        if fresh.get("is_stale"):
            risk_parts.append(f"Données anciennes: {', '.join(fresh.get('stale_sources', [])[:2])}")
        risk_flags = " | ".join(risk_parts) if risk_parts else "Aucun"

        # Confirmation
        confirmation = _derive_confirmation(setup_name, direction)

        setups.append({
            "symbol": sym,
            "asset": DISPLAY_NAMES.get(sym, sym),
            "asset_type": ASSET_TYPES.get(sym, "Unknown"),
            "setup": setup_name.replace("_", " ").title(),
            "timeframe": timeframe,
            "status": status,
            "grade": grade,
            "score": score,
            "probability": prob,
            "bias": "Long" if direction == "bullish" else "Short" if direction == "bearish" else direction.title(),
            "price": price,
            "vwap": vwap,
            "support": supports,
            "resistance": resistances,
            "entry_trigger": entry_trigger,
            "entry_zone": entry_zone,
            "stop_loss": sl,
            "invalidation": sl,
            "tp1": tps[0] if len(tps) > 0 else None,
            "tp2": tps[1] if len(tps) > 1 else None,
            "tp3": tps[2] if len(tps) > 2 else None,
            "risk_reward": rr,
            "confirmation": confirmation,
            "risk_flags": risk_flags,
            "action": "Attendre confirmation" if status != "Prioritaire" else "Surveillance uniquement — attente breakout",
        })

    # Sort by grade priority
    grade_order = {"A+": 0, "A": 1, "A-": 2, "B+": 3, "B": 4, "B-": 5, "C": 6}
    setups.sort(key=lambda s: (grade_order.get(s["grade"], 9), -s["score"]))
    return setups


# ── Derivation helpers ─────────────────────────────────────────────────────

def _derive_grade(thesis: dict, direction: str) -> str:
    confidence = thesis.get("confidence", 50)
    probs = thesis.get("probabilities", {})
    max_prob = max(probs.get("bull", 0), probs.get("bear", 0))
    tech = thesis.get("technical", {})
    alignment = tech.get("alignment", "")

    if confidence >= 75 and max_prob >= 65 and alignment in ("aligned_bullish", "aligned_bearish"):
        return "A" if max_prob < 75 else "A+"
    elif confidence >= 65 and max_prob >= 55:
        return "A-"
    elif confidence >= 55 and max_prob >= 45:
        return "B+"
    elif confidence >= 45:
        return "B"
    elif confidence >= 35:
        return "B-"
    return "C"


def _derive_score(thesis: dict) -> int:
    confidence = thesis.get("confidence", 50)
    probs = thesis.get("probabilities", {})
    max_prob = max(probs.get("bull", 0), probs.get("bear", 0))
    return int((confidence + max_prob) / 2.0)


def _derive_price(thesis: dict) -> Optional[float]:
    tech = thesis.get("technical", {})
    supports = tech.get("key_support", [])
    resistances = tech.get("key_resistance", [])
    if supports and resistances:
        return round((supports[0] + resistances[0]) / 2, 2)
    return None


def _derive_entry_trigger(setup: str, direction: str, vwap, supports, resistances,
                         active_cdp: list = None) -> str:
    if active_cdp is None:
        active_cdp = []

    # If we have active CDP triggers, mention them
    cdp_note = ""
    if active_cdp:
        cdp_names = [t.replace("_", " ").title() for t in active_cdp[:2]]
        cdp_note = f" (CDP: {', '.join(cdp_names)})"

    if "vwap" in setup.lower():
        if direction == "bullish":
            base = f"Clôture M15 > {vwap:.0f}" if vwap else "Reclaim VWAP M15"
        else:
            base = f"Clôture M15 < {vwap:.0f}" if vwap else "Loss VWAP M15"
        return base + cdp_note
    if "pullback" in setup.lower():
        return "Reclaim M15 sur pullback" + cdp_note
    if "break" in setup.lower():
        if direction == "bullish" and resistances:
            return f"Clôture H1 > {resistances[0]:.0f}" + cdp_note
        if direction == "bearish" and supports:
            return f"Clôture H1 < {supports[0]:.0f}" + cdp_note
    return ("Attendre signal de confirmation" + cdp_note) if cdp_note else "Attendre signal de confirmation"


def _derive_entry_zone(supports, resistances, direction, price) -> str:
    if direction == "bullish":
        s = supports[0] if supports else (price * 0.98 if price else 0)
        r = resistances[0] if resistances else (price * 1.02 if price else 0)
        return f"{s:.0f} — {r:.0f}"
    else:
        r = resistances[0] if resistances else (price * 1.02 if price else 0)
        s = supports[0] if supports else (price * 0.98 if price else 0)
        return f"{r:.0f} — {s:.0f}"
    return "?"


def _derive_sl(supports, resistances, direction) -> Optional[float]:
    if direction == "bullish" and supports:
        return supports[0] if len(supports) == 1 else supports[1] if len(supports) > 1 else supports[0]
    if direction == "bearish" and resistances:
        return resistances[0] if len(resistances) == 1 else resistances[1] if len(resistances) > 1 else resistances[0]
    return None


def _derive_tps(resistances, supports, direction, price) -> List[float]:
    tps = []
    if direction == "bullish" and resistances:
        for r in resistances[:3]:
            tps.append(r)
    elif direction == "bearish" and supports:
        for s in supports[:3]:
            tps.append(s)
    # Pad with projections
    while len(tps) < 3 and price:
        tps.append(round(price * (1.03 + len(tps) * 0.02), 2))
    return tps[:3]


def _derive_rr(price, sl, tps) -> Optional[float]:
    if price and sl and tps and sl != price:
        risk = abs(price - sl)
        reward = abs(tps[0] - price)
        if risk > 0:
            return round(reward / risk, 1)
    return None


def _derive_confirmation(setup: str, direction: str) -> str:
    parts = []
    if "vwap" in setup.lower():
        parts.append("Volume + maintien VWAP")
    if "break" in setup.lower():
        parts.append("Clôture confirmée + volume")
    if not parts:
        parts.append("Structure + volume + timeframe")
    return " + ".join(parts)


# ── Renderers ──────────────────────────────────────────────────────────────

def render_setup_cards() -> Dict[str, Any]:
    """Render all active setup cards in canonical format."""
    setups = _gather_all_setups()

    if not setups:
        return {
            "spoken_text": "Aucun setup actif détecté pour le moment. Surveillance uniquement.",
            "display_text": "Aucun setup actif.",
            "cards": [],
            "market_summary": {},
        }

    # ── Market summary ─────────────────────────────────────────────────
    best = setups[0]
    best_rr = max(setups, key=lambda s: s.get("risk_reward") or 0)
    waiting = [s for s in setups if s["status"].startswith("Attente")]

    # Get regime
    regime = "unknown"
    try:
        from modules.desk_pro.service.executive_reader import get_executive_regime
        r = get_executive_regime()
        if r:
            regime = r.get("regime", "unknown")
    except Exception:
        pass

    market_summary = {
        "regime": REGIME_FR.get(regime, regime),
        "risk": "Moyen",
        "active_setups": len(setups),
        "best_setup": f"{best['symbol']} {best['setup']}",
        "best_rr": f"{best_rr['symbol']} {best_rr['setup']}",
        "waiting": f"{len(waiting)} setup(s) en attente",
        "pipeline": "OK",
        "mode": "Monitor-only",
    }

    # ── Spoken ─────────────────────────────────────────────────────────
    parts = []
    if regime != "unknown":
        parts.append(f"Marché en {REGIME_FR.get(regime, regime)}")
    parts.append(f"{len(setups)} setups actifs")

    for s in setups[:4]:
        sym = SPOKEN_NAMES.get(s["symbol"], s["symbol"])
        line = f"{sym} est {s['status'].lower()}, grade {s['grade']}, score {s['score']}, probabilité {s['probability']}%"
        if s["entry_zone"]:
            line += f", entrée {s['entry_zone']}"
        if s["stop_loss"]:
            line += f", stop {s['stop_loss']:.0f}"
        if s["tp1"]:
            tps = [f"{t:.0f}" for t in [s["tp1"], s["tp2"], s["tp3"]] if t is not None]
            line += f", objectifs {', '.join(tps)}"
        parts.append(line)

    parts.append("Aucun trade automatique. Validation humaine obligatoire.")
    spoken = ". ".join(parts) + "."
    if len(spoken) > 600:
        spoken = spoken[:597] + "..."

    # ── Display ────────────────────────────────────────────────────────
    display_lines = ["Résumé marché", "─" * 30]
    for k, v in market_summary.items():
        display_lines.append(f"  {k.replace('_', ' ').title():20s} {v}")
    display_lines.append("")

    for s in setups:
        display_lines.append(f"{s['symbol']} | {s['grade']} | {s['score']} | {s['probability']}% | {s['bias'].upper()} | {s['timeframe']}")
        e = f"Entrée {s['entry_zone']}" if s['entry_zone'] else "Entrée ?"
        sl = f"SL {s['stop_loss']:.0f}" if s['stop_loss'] else "SL ?"
        tps = [f"{t:.0f}" for t in [s['tp1'], s['tp2'], s['tp3']] if t is not None]
        tp_str = f"TP {' / '.join(tps)}" if tps else ""
        display_lines.append(f"{e} | {sl} | {tp_str}")
        if s['support'] or s['resistance']:
            sup = f"Support {' / '.join(f'{x:.0f}' for x in s['support'][:2])}" if s['support'] else ""
            res = f"Résistance {' / '.join(f'{x:.0f}' for x in s['resistance'][:2])}" if s['resistance'] else ""
            if sup or res:
                display_lines.append(f"{sup}{' | ' if sup and res else ''}{res}")
        display_lines.append(f"Signal: {s['setup']} | Risque: {s['risk_flags']}")
        display_lines.append("")

    display = "\n".join(display_lines)

    return {
        "spoken_text": spoken,
        "display_text": display,
        "cards": setups,
        "market_summary": market_summary,
    }
