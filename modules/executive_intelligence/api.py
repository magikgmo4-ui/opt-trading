"""
Executive Intelligence API — PR6.

Read-only FastAPI router exposing executive intelligence:
  - /read/executive           — full briefing
  - /read/executive/briefing  — summary + voice
  - /read/executive/regime    — current regime
  - /read/executive/leaders   — leaderboard
  - /read/executive/risks     — top risks

Cache TTL 60s. No DeskPro. No Voice. No broker.
"""

from __future__ import annotations

import time
from typing import Dict, Optional

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Executive Intelligence API",
    description="Read-only market intelligence for opt-trading",
    version="1.0.0",
)

# ── Cache ──────────────────────────────────────────────────────────────────

_cache: Dict[str, tuple[dict, float]] = {}
CACHE_TTL = 60


def _cache_get(key: str) -> Optional[dict]:
    entry = _cache.get(key)
    if entry is None:
        return None
    data, ts = entry
    if time.time() - ts > CACHE_TTL:
        del _cache[key]
        return None
    return data


def _cache_set(key: str, data: dict) -> None:
    _cache[key] = (data, time.time())


def _get_or_build(cache_key: str, builder, force: bool = False) -> tuple[dict, str]:
    if not force:
        cached = _cache_get(cache_key)
        if cached:
            return cached, "cache"
    try:
        data = builder()
        _cache_set(cache_key, data)
        return data, "build"
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, "error"


# ── Builders ───────────────────────────────────────────────────────────────

def _build_full() -> dict:
    from .briefing_engine import build_briefing
    brief = build_briefing()
    return {
        "ok": True,
        "briefing_id": brief.briefing_id,
        "generated_at": brief.generated_at.isoformat(),
        "market_regime": brief.market_regime,
        "regime_confidence": brief.regime_confidence,
        "overall_confidence": brief.overall_confidence,
        "leaders": brief.leaders,
        "laggards": brief.laggards,
        "summary": brief.summary,
        "what_changed": brief.what_changed,
        "what_to_watch": brief.what_to_watch,
        "top_risks": brief.top_risks,
        "top_opportunities": brief.top_opportunities,
        "voice_one_liner": brief.voice_one_liner,
        "voice_briefing": brief.voice_briefing,
    }


def _build_briefing() -> dict:
    from .briefing_engine import build_briefing
    brief = build_briefing()
    return {
        "ok": True,
        "briefing_id": brief.briefing_id,
        "generated_at": brief.generated_at.isoformat(),
        "summary": brief.summary,
        "voice_one_liner": brief.voice_one_liner,
        "voice_briefing": brief.voice_briefing,
        "top_risks": brief.top_risks,
        "top_opportunities": brief.top_opportunities,
        "what_changed": brief.what_changed,
        "what_to_watch": brief.what_to_watch,
    }


def _build_regime() -> dict:
    from .regime_engine import detect_regime
    regime = detect_regime()
    return {
        "ok": True,
        "regime": regime.regime,
        "confidence": regime.confidence,
        "risk_score": regime.risk_score,
        "narrative": regime.narrative,
        "drivers": {
            "dxy_trend": regime.evidence.dxy_trend,
            "vix_level": regime.evidence.vix_level,
            "spy_trend": regime.evidence.spy_trend,
            "btc_dominance": regime.evidence.btc_dominance,
            "fear_greed": regime.evidence.fear_greed,
            "volatility_regime": regime.evidence.volatility_regime,
        },
        "next_likely_regime": regime.next_likely_regime,
        "transition_probability": regime.transition_probability,
        "asset_count_bullish": regime.evidence.asset_count_bullish,
        "asset_count_bearish": regime.evidence.asset_count_bearish,
    }


def _build_leaders() -> dict:
    from .cross_asset_engine import build_leaderboard, compute_influences
    board = build_leaderboard()
    influences = compute_influences()
    return {
        "ok": True,
        "leaders": [
            {"symbol": e.symbol, "rank": e.rank, "direction": e.direction,
             "confidence": e.confidence, "reliability": e.reliability,
             "momentum_score": e.momentum_score}
            for e in board if e.is_leader
        ],
        "laggards": [
            {"symbol": e.symbol, "rank": e.rank, "direction": e.direction,
             "confidence": e.confidence, "reliability": e.reliability,
             "momentum_score": e.momentum_score}
            for e in board if e.is_laggard
        ],
        "full_board": [
            {"symbol": e.symbol, "rank": e.rank, "direction": e.direction,
             "confidence": e.confidence, "reliability": e.reliability,
             "momentum_score": e.momentum_score}
            for e in board
        ],
        "cross_asset_notes": [
            f"{i.source}→{i.target}: {i.direction} (influence {i.influence_score})"
            for i in influences[:6]
        ],
    }


def _build_risks() -> dict:
    from .briefing_engine import build_briefing
    from .regime_engine import detect_regime
    from .cross_asset_engine import build_leaderboard
    brief = build_briefing()
    regime = detect_regime()
    board = build_leaderboard()

    stale = sum(1 for e in board if e.confidence < 35)
    return {
        "ok": True,
        "top_risks": brief.top_risks,
        "regime_risk": regime.risk_score,
        "regime_risk_label": "high" if regime.risk_score >= 70 else "moderate" if regime.risk_score >= 40 else "low",
        "stale_assets_count": stale,
        "concentration_note": f"{sum(1 for e in board if e.direction == 'bullish' and e.confidence >= 75)} actifs en crowding haussier",
        "divergence_note": "Divergence détectée entre leaders" if len({e.direction for e in board if e.is_leader}) > 1 else "Leaders alignés",
    }


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.get("/read/executive")
def read_executive(build: bool = Query(False)):
    data, source = _get_or_build("executive_full", _build_full, force=build)
    data["source"] = source
    data["ttl_seconds"] = CACHE_TTL
    return data


@app.get("/read/executive/briefing")
def read_briefing(build: bool = Query(False)):
    data, source = _get_or_build("executive_briefing", _build_briefing, force=build)
    data["source"] = source
    data["ttl_seconds"] = CACHE_TTL
    return data


@app.get("/read/executive/regime")
def read_regime(build: bool = Query(False)):
    data, source = _get_or_build("executive_regime", _build_regime, force=build)
    data["source"] = source
    data["ttl_seconds"] = CACHE_TTL
    return data


@app.get("/read/executive/leaders")
def read_leaders(build: bool = Query(False)):
    data, source = _get_or_build("executive_leaders", _build_leaders, force=build)
    data["source"] = source
    data["ttl_seconds"] = CACHE_TTL
    return data


@app.get("/read/executive/risks")
def read_risks(build: bool = Query(False)):
    data, source = _get_or_build("executive_risks", _build_risks, force=build)
    data["source"] = source
    data["ttl_seconds"] = CACHE_TTL
    return data


@app.get("/health")
def health():
    return {"ok": True, "module": "executive_intelligence", "version": "1.0.0"}
