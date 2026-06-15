"""
Voice Operator Intent Router
GO_DESKPRO_VOICE_OPERATOR_01 — Lot C

Keyword-based intent router. Maps user phrases to /read/* endpoints.
No LLM, no NLP — pure pattern matching for reliability and zero cost.

Extensible: add more patterns to INTENT_MAP to support new voice commands.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RoutedIntent:
    intent: str                           # e.g. "system_status", "spcx_summary"
    endpoint: str                         # e.g. "/read/system"
    params: dict = field(default_factory=dict)  # e.g. {"symbol": "BTC"}
    raw_phrase: str = ""                  # original user phrase
    confidence: float = 1.0              # 1.0 = exact match, <1.0 = fuzzy


# Intent mapping: (keywords) → (intent_id, endpoint, param_template)
# Order matters — first match wins. Place specific patterns before general ones.
INTENT_PATTERNS: list[tuple[list[str], str, str, dict]] = [
    # ── System ──
    (["etat systeme", "status systeme", "systeme", "etat du systeme", "health", "sante"],
     "system_status", "/read/system", {}),

    # ── Trader commands — MUST come before generic single-word patterns ──
    (["briefing matin", "briefing", "morning brief", "point matin"],
     "morning_brief", "/read/composite", {"type": "morning_brief"}),

    (["vue marche", "market view", "snapshot marche", "marches", "tous les marches"],
     "market_view", "/read/composite", {"type": "market_view"}),

    (["nouveautes", "quoi de neuf", "derniers changements", "updates"],
     "whats_new", "/read/composite", {"type": "whats_new"}),

    (["spcx complet", "spcx full", "spcx detail", "tout spcx"],
     "spcx_full", "/read/composite", {"type": "spcx_full"}),

    (["spcx risque", "spcx risk", "spcx danger", "risque spcx"],
     "spcx_risk", "/read/composite", {"type": "spcx_risk"}),

    (["gold complet", "gold full", "gold detail", "tout gold", "or complet"],
     "gold_full", "/read/composite", {"type": "gold_full"}),

    (["gold danger", "gold risk", "gold risque", "danger gold", "danger or"],
     "gold_danger", "/read/composite", {"type": "gold_danger"}),

    (["top setups", "meilleurs setups", "top scores", "best setups"],
     "top_setups", "/read/composite", {"type": "top_setups"}),

    (["watchlist ia", "ia watchlist", "ai watchlist", "watchlist ai"],
     "watchlist_ia", "/read/composite", {"type": "watchlist_ia"}),

    (["watchlist spatial", "spatial watchlist", "space watchlist", "watchlist space", "spatiale"],
     "watchlist_spatial", "/read/composite", {"type": "watchlist_spatial"}),

    (["setups a+", "a+", "grade a+", "setups a plus", "meilleurs setups a+"],
     "a_plus_setups", "/read/composite", {"type": "a_plus_setups"}),

    (["risques", "risque", "danger", "alertes risque", "risk"],
     "risks", "/read/composite", {"type": "risks"}),

    (["urgences", "urgent", "critique"],
     "urgencies", "/read/composite", {"type": "urgencies"}),

    (["changements"],
     "whats_new", "/read/composite", {"type": "whats_new"}),

    # ── SPCX — generic (AFTER specific compound patterns) ──
    (["resume spcx", "spcx resume", "spcx summary", "spcx", "spacex", "space x"],
     "spcx_summary", "/read/spacex", {}),

    # ── Alerts ──
    (["alertes telegram", "alertes", "alerts", "alerte", "dernieres alertes", "notifications"],
     "alerts", "/read/alerts", {"limit": 10}),

    (["alertes critiques", "critiques", "alertes urgentes"],
     "alerts_critical", "/read/alerts", {"limit": 50}),

    # ── Setups ──
    (["setups actifs", "tous les setups", "quels setups", "setups en cours", "liste setups"],
     "setups_all", "/read/setups", {}),

    (["setups a+", "setups a plus", "meilleurs setups", "top setups", "grade a+"],
     "setups_all", "/read/setups", {}),  # /read/setups includes A+ count

    # ── Setup detail (symbol-specific) — MUST come before generic spcx/btc patterns ──
    (["setup btc", "btc setup", "bitcoin setup"],
     "setup_detail", "/read/setup", {"symbol": "BTC"}),

    (["setup gold", "gold setup", "xau setup", "xauusd setup"],
     "setup_detail", "/read/setup", {"symbol": "XAUUSD"}),

    (["setup eth", "eth setup", "ethereum setup"],
     "setup_detail", "/read/setup", {"symbol": "ETH"}),

    (["setup spcx", "spcx setup"],
     "setup_detail", "/read/setup", {"symbol": "SPCX"}),

    # ── Score detail (symbol-specific) — MUST come before generic patterns ──
    (["score btc", "btc score", "score bitcoin", "probabilite btc"],
     "score_detail", "/read/score", {"symbol": "BTC"}),

    (["score gold", "gold score", "score xau", "probabilite gold"],
     "score_detail", "/read/score", {"symbol": "XAUUSD"}),

    (["score eth", "eth score", "score ethereum"],
     "score_detail", "/read/score", {"symbol": "ETH"}),

    (["score spcx", "spcx score"],
     "score_detail", "/read/score", {"symbol": "SPCX"}),

    # ── Generic analysis — MUST come before generic spcx/btc ──
    (["analyse btc", "btc analyse", "analyse bitcoin"],
     "score_detail", "/read/score", {"symbol": "BTC"}),

    (["analyse gold", "gold analyse", "analyse or", "analyse xau"],
     "score_detail", "/read/score", {"symbol": "XAUUSD"}),

    (["analyse eth", "eth analyse", "analyse ethereum"],
     "score_detail", "/read/score", {"symbol": "ETH"}),

    (["analyse spcx", "spcx analyse"],
     "score_detail", "/read/score", {"symbol": "SPCX"}),

    # ── SPCX — generic (after specific setup/score/analyse patterns) ──
    (["resume spcx", "spcx resume", "spcx summary", "spcx", "spacex", "space x"],
     "spcx_summary", "/read/spacex", {}),

    # ── Market / Report ──
    (["rapport marche", "marche", "market", "etat du marche", "overview"],
     "market", "/read/market", {}),

    (["rapport quotidien", "rapport journalier", "daily report", "rapport du jour", "daily", "aujourd'hui"],
     "report", "/read/report", {}),

    (["rapport", "report"],
      "report", "/read/report", {}),
]


def route(phrase: str) -> RoutedIntent:
    """Route a user phrase to the best matching intent.

    Args:
        phrase: User's natural language query (e.g. "Etat systeme")

    Returns:
        RoutedIntent with endpoint + params, or a fallback intent if no match.
    """
    normalized = phrase.lower().strip().rstrip("?!.,;:")

    # Exact keyword matching
    for keywords, intent_id, endpoint, params in INTENT_PATTERNS:
        for kw in keywords:
            if kw in normalized:
                # Extract dynamic symbol if present
                resolved_params = dict(params)
                resolved_params = _extract_symbol(normalized, resolved_params)
                return RoutedIntent(
                    intent=intent_id,
                    endpoint=endpoint,
                    params=resolved_params,
                    raw_phrase=phrase,
                    confidence=1.0,
                )

    # No match — default to system status
    return RoutedIntent(
        intent="unknown",
        endpoint="/read/system",
        params={},
        raw_phrase=phrase,
        confidence=0.0,
    )


def _extract_symbol(phrase: str, params: dict) -> dict:
    """Extract a trading symbol from the phrase if not already in params."""
    if params.get("symbol"):
        return params

    # Word-boundary aware matching to avoid "or" matching "rapport"
    import re
    symbols_map = {
        "btc": "BTC", "bitcoin": "BTC",
        "eth": "ETH", "ethereum": "ETH",
        "gold": "XAUUSD", "xau": "XAUUSD",
        "spcx": "SPCX", "spacex": "SPCX",
        "sol": "SOL", "solana": "SOL",
        "nvda": "NVDA",
        "rklb": "RKLB",
        "dxy": "DXY",
        "spy": "SPY",
        "vix": "VIX",
    }
    # "or" is too ambiguous — only match explicit "xauusd" or "gold"
    for key, sym in symbols_map.items():
        if key == "or":
            continue
        if re.search(r'\b' + re.escape(key) + r'\b', phrase):
            params["symbol"] = sym
            break
    return params


def list_intents() -> list[dict]:
    """Return all registered intents for help/display."""
    seen = set()
    result = []
    for keywords, intent_id, endpoint, params in INTENT_PATTERNS:
        if intent_id not in seen:
            seen.add(intent_id)
            result.append({
                "intent": intent_id,
                "endpoint": endpoint,
                "example": keywords[0] if keywords else "?",
            })
    return result
