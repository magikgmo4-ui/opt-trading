from __future__ import annotations

"""Voice Operator — text command router for DeskPro.

Maps natural language commands to read-only API calls.
No side effects. No broker calls. monitor_only always enforced.

Supported intents:
    spcx_score   -- "score spcx" / "spcx score" / "spcx"
    help         -- "help" / "?"
    unknown      -- anything else

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

_HELP_PATTERNS = [
    r"\bhelp\b",
    r"^\?$",
]

# ---------------------------------------------------------------------------
# Response formatters
# ---------------------------------------------------------------------------

_HELP_TEXT = (
    "Voice Operator -- commandes disponibles :\n"
    "  \"score spcx\"   -> Score composite SPCX (grade, setup_state, niveaux)\n"
    "  \"help\" / \"?\"   -> ce message"
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


def _is_spcx(text):
    return any(re.search(p, text, re.IGNORECASE) for p in _SPCX_PATTERNS)


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
