from __future__ import annotations

"""Voice Operator — text command router for DeskPro.

Maps natural language commands to read-only API calls.
No side effects. No broker calls. monitor_only always enforced.

Supported intents:
    spcx_score              -- "score spcx" / "spcx score" / "spcx"
    spcx_opening_analysis   -- "analyse ouverture spcx" / "résumé première demi-heure"
    spcx_gap                -- "gap spcx"
    spcx_momentum           -- "momentum spcx"
    spcx_risk               -- "risque spcx"
    help                    -- "help" / "?"
    unknown                 -- anything else

Usage:
    from modules.desk_pro.service.voice_operator import dispatch_command
    result = dispatch_command("score spcx")
    print(result["response"])
"""

import re
from typing import Any

from modules.desk_pro.service.spcx_score_reader import read_spcx_score

# ---------------------------------------------------------------------------
# Intent patterns
# ---------------------------------------------------------------------------

_SPCX_PATTERNS = [
    r"\bscore\s+spcx\b",
    r"\bspcx\s+score\b",
    r"\bscore\s+spacex\b",
    r"\bspacex\s+score\b",
    r"\bspcx\b",
]

_OPENING_ANALYSIS_PATTERNS = [
    r"\banalyse\s+ouverture\s+spcx\b",
    r"\brésumé\s+premi[èe]re\s+demi[\s-]?heure\b",
    r"\bpremi[èe]re\s+demi[\s-]?heure\b",
    r"\bouverture\s+spcx\b",
]

_GAP_PATTERNS = [
    r"\bgap\s+spcx\b",
    r"\bgap\b",
]

_MOMENTUM_PATTERNS = [
    r"\bmomentum\s+spcx\b",
    r"\bmomentum\b",
]

_RISK_PATTERNS = [
    r"\brisque\s+spcx\b",
    r"\brisque\b",
]

_HELP_PATTERNS = [
    r"\bhelp\b",
    r"^\?$",
]

# ---------------------------------------------------------------------------
# Response formatters
# ---------------------------------------------------------------------------

_HELP_TEXT = (
    "Voice Operator -- commandes disponibles :\n"
    "  \"score spcx\"              -> Score composite SPCX (grade, setup_state, niveaux)\n"
    "  \"analyse ouverture spcx\"  -> Analyse complète ouverture SPCX\n"
    "  \"gap spcx\"                -> Gap d'ouverture SPCX\n"
    "  \"momentum spcx\"           -> Momentum SPCX\n"
    "  \"risque spcx\"             -> Risque SPCX\n"
    "  \"help\" / \"?\"             -> ce message"
)


def _fmt_spcx(result):
    score = result.get("score", 0)
    grade = result.get("grade", "?")
    state = result.get("setup_state", "?")
    bias = result.get("bias", "?")
    events = ", ".join(result.get("events", [])) or "none"
    risk = ", ".join(result.get("risk_notes", [])) or "none"
    levels = result.get("levels") or {}
    price = levels.get("price")
    vwap = levels.get("vwap")
    orb_high = levels.get("orb_high")

    price_str = f"{price:.2f}" if price is not None else "--"
    vwap_str = f"{vwap:.2f}" if vwap is not None else "--"
    orb_str = f"{orb_high:.2f}" if orb_high is not None else "--"

    return (
        f"SPCX  {score}/100 -- Grade {grade} -- {state.upper()}\n"
        f"Bias: {bias}  |  Prix: {price_str}  |  VWAP: {vwap_str}  |  ORB High: {orb_str}\n"
        f"Signaux: {events}\n"
        f"Risque: {risk}\n"
        f"[monitor_only]"
    )


# ---------------------------------------------------------------------------
# Intent matchers
# ---------------------------------------------------------------------------


def _fmt_opening_analysis(result):
    om = result.get("opening_metrics") or {}
    oc = result.get("opening_components") or {}
    score = result.get("score", 0)
    grade = result.get("grade", "?")
    state = result.get("setup_state", "?")

    gap = f"{om.get('opening_gap_pct', 0):+.2f}%" if om.get('opening_gap_pct') is not None else "--"
    drive = om.get("opening_drive", "--")
    dv = f"{om.get('distance_vwap_pct', 0):+.2f}%" if om.get('distance_vwap_pct') is not None else "--"
    dpm = f"{om.get('distance_premarket_high_pct', 0):+.2f}%" if om.get('distance_premarket_high_pct') is not None else "--"
    rvol = f"{om.get('relative_volume_15m', 0):.1f}x" if om.get('relative_volume_15m') is not None else "--"
    rs = om.get("risk_score", 0)
    cs = om.get("continuation_score", 0)
    es = om.get("exhaustion_score", 0)
    boost = oc.get("dynamic_boost", 0)
    det = ", ".join(oc.get("details", [])) or "none"

    return (
        f"SPCX Ouverture  {score}/100 -- Grade {grade} -- {state.upper()}\n"
        f"Gap: {gap}  |  Drive: {drive}  |  RVOL: {rvol}\n"
        f"Dist VWAP: {dv}  |  Dist Premarket: {dpm}\n"
        f"Risque: {rs}/100  |  Continuation: {cs}/100  |  Épuisement: {es}/100\n"
        f"Détails: {det}\n"
        f"Dynamic boost: {boost:+d}\n"
        f"[monitor_only]"
    )


def _fmt_gap(result):
    om = result.get("opening_metrics") or {}
    events = result.get("events", [])
    gap = f"{om.get('opening_gap_pct', 0):+.2f}%" if om.get('opening_gap_pct') is not None else "--"
    drive = om.get("opening_drive", "--")
    dorb = f"{om.get('distance_orb_pct', 0):+.2f}%" if om.get('distance_orb_pct') is not None else "--"
    dv = f"{om.get('distance_vwap_pct', 0):+.2f}%" if om.get('distance_vwap_pct') is not None else "--"
    has_gap_events = [e for e in events if "GAP" in e]
    gap_events = ", ".join(has_gap_events) if has_gap_events else "none"

    return (
        f"SPCX Gap: {gap}  |  Drive: {drive}\n"
        f"Dist VWAP: {dv}  |  Dist ORB: {dorb}\n"
        f"Événements gap: {gap_events}\n"
        f"[monitor_only]"
    )


def _fmt_momentum(result):
    om = result.get("opening_metrics") or {}
    events = result.get("events", [])
    cs = om.get("continuation_score", 0)
    es = om.get("exhaustion_score", 0)
    rvol = f"{om.get('relative_volume_15m', 0):.1f}x" if om.get('relative_volume_15m') is not None else "--"
    dv = f"{om.get('distance_vwap_pct', 0):+.2f}%" if om.get('distance_vwap_pct') is not None else "--"
    evt = ", ".join(events) if events else "none"

    return (
        f"SPCX Momentum -- Continuation: {cs}/100  |  Épuisement: {es}/100\n"
        f"RVOL: {rvol}  |  Dist VWAP: {dv}\n"
        f"Signaux: {evt}\n"
        f"[monitor_only]"
    )


def _fmt_risk(result):
    om = result.get("opening_metrics") or {}
    risk = om.get("risk_score", 0)
    es = om.get("exhaustion_score", 0)
    dv = f"{om.get('distance_vwap_pct', 0):+.2f}%" if om.get('distance_vwap_pct') is not None else "--"
    gap = f"{om.get('opening_gap_pct', 0):+.2f}%" if om.get('opening_gap_pct') is not None else "--"
    notes = ", ".join(result.get("risk_notes", [])) or "none"

    return (
        f"SPCX Risque: {risk}/100  |  Épuisement: {es}/100\n"
        f"Extension: {dv}  |  Gap: {gap}\n"
        f"Notes: {notes}\n"
        f"[monitor_only]"
    )


def _is_spcx(text):
    return any(re.search(p, text, re.IGNORECASE) for p in _SPCX_PATTERNS)


def _is_opening_analysis(text):
    return any(re.search(p, text, re.IGNORECASE) for p in _OPENING_ANALYSIS_PATTERNS)


def _is_gap(text):
    return any(re.search(p, text, re.IGNORECASE) for p in _GAP_PATTERNS)


def _is_momentum(text):
    return any(re.search(p, text, re.IGNORECASE) for p in _MOMENTUM_PATTERNS)


def _is_risk(text):
    return any(re.search(p, text, re.IGNORECASE) for p in _RISK_PATTERNS)


def _is_help(text):
    return any(re.search(p, text.strip(), re.IGNORECASE) for p in _HELP_PATTERNS)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def dispatch_command(text):
    if not text or not text.strip():
        return {
            "matched": False,
            "intent": "empty",
            "response": _HELP_TEXT,
            "data": {},
        }

    text = text.strip()

    if _is_help(text):
        return {
            "matched": True,
            "intent": "help",
            "response": _HELP_TEXT,
            "data": {},
        }

    if _is_opening_analysis(text):
        data = read_spcx_score()
        return {
            "matched": True,
            "intent": "spcx_opening_analysis",
            "response": _fmt_opening_analysis(data),
            "data": data,
        }

    if _is_gap(text):
        data = read_spcx_score()
        return {
            "matched": True,
            "intent": "spcx_gap",
            "response": _fmt_gap(data),
            "data": data,
        }

    if _is_momentum(text):
        data = read_spcx_score()
        return {
            "matched": True,
            "intent": "spcx_momentum",
            "response": _fmt_momentum(data),
            "data": data,
        }

    if _is_risk(text):
        data = read_spcx_score()
        return {
            "matched": True,
            "intent": "spcx_risk",
            "response": _fmt_risk(data),
            "data": data,
        }

    if _is_spcx(text):
        data = read_spcx_score()
        return {
            "matched": True,
            "intent": "spcx_score",
            "response": _fmt_spcx(data),
            "data": data,
        }

    return {
        "matched": False,
        "intent": "unknown",
        "response": f"Commande non reconnue : '{text}'. Essayez 'help'.",
        "data": {},
    }
