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

    (["vue marche", "market view", "snapshot marche", "marches", "tous les marches",
      "rapport marche", "rapport marche", "rapport des marches", "market report",
      "rapport marché", "marché", "vue marché"],
     "market_view", "/read/composite", {"type": "market_view"}),

    (["nouveautes", "quoi de neuf", "derniers changements", "updates"],
     "whats_new", "/read/composite", {"type": "whats_new"}),

    (["spcx complet", "spcx full", "spcx detail", "tout spcx",
      "resume spcx", "resume spcx", "spcx resume", "spcx summary",
      "resume SPCX", "SPCX resume",
      "resumer spcx", "spcx resumer"],
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

    # ── Priority commands ──
    (["priorites", "priorite", "top priorites", "quoi regarder", "que regarder"],
     "priorities", "/read/composite", {"type": "priorities"}),

    (["attention", "avertissements", "alertes attention", "quoi surveiller", "points attention"],
     "attention", "/read/composite", {"type": "attention"}),

    (["changements", "nouveautes", "quoi de neuf", "derniers changements", "updates"],
     "whats_new", "/read/composite", {"type": "whats_new"}),

    (["top movers", "movers", "bouge", "mouvements"],
     "top_movers", "/read/composite", {"type": "top_movers"}),

    (["resume executif", "exec summary", "resume", "bref"],
     "exec_summary", "/read/composite", {"type": "exec_summary"}),
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
