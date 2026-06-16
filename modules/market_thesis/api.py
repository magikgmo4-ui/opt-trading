"""
Market Thesis API — PR6.

Read-only FastAPI router exposing market theses.
No trade execution, no DeskPro, no Voice — pure data.

Endpoints:
  GET /read/thesis           — list all symbols or get one
  GET /read/thesis?symbol=BTC — latest thesis for symbol
  GET /read/thesis?symbol=BTC&build=true — force rebuild
  GET /health                — health check
"""

from __future__ import annotations

import time
from typing import Dict, Optional

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from .archive import load_latest, save_all
from .config import CANONICAL_SYMBOLS
from .models import MarketThesis
from .thesis_engine import build_thesis

app = FastAPI(
    title="Market Thesis API",
    description="Read-only thesis exposure for opt-trading",
    version="1.0.0",
)

# ── Simple in-memory cache ────────────────────────────────────────────────

_cache: Dict[str, tuple[MarketThesis, float]] = {}
CACHE_TTL = 60  # seconds


def _cache_get(symbol: str) -> Optional[MarketThesis]:
    entry = _cache.get(symbol)
    if entry is None:
        return None
    thesis, cached_at = entry
    if time.time() - cached_at > CACHE_TTL:
        del _cache[symbol]
        return None
    return thesis


def _cache_set(symbol: str, thesis: MarketThesis) -> None:
    _cache[symbol] = (thesis, time.time())


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.get("/read/thesis")
def read_thesis(
    symbol: Optional[str] = Query(None, description="Canonical symbol (BTC, ETH, SOL, ...)"),
    build: bool = Query(False, description="Force rebuild instead of reading latest"),
):
    """Get market thesis for one or all symbols.

    Without ?symbol= : returns summary of all 9 symbols.
    With ?symbol=BTC : returns full thesis for BTC.
    With ?build=true : regenerates the thesis instead of reading from disk.
    """
    if symbol:
        return _get_one(symbol, force_build=build)
    return _get_all()


def _get_one(symbol: str, force_build: bool = False) -> JSONResponse:
    sym = symbol.upper()

    # Normalize aliases
    from .config import normalize_symbol
    sym = normalize_symbol(sym)

    thesis: Optional[MarketThesis] = None
    source = "unknown"

    if not force_build:
        # Try cache
        thesis = _cache_get(sym)
        if thesis is not None:
            source = "cache"

    if thesis is None and not force_build:
        # Try disk
        thesis = load_latest(sym)
        if thesis is not None:
            source = "disk"
            _cache_set(sym, thesis)

    if thesis is None or force_build:
        # Build on demand
        try:
            thesis = build_thesis(sym)
            source = "build"
            _cache_set(sym, thesis)
            save_all(thesis)
        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content={"ok": False, "symbol": sym, "error": str(exc)},
            )

    return JSONResponse(content={
        "ok": True,
        "symbol": sym,
        "source": source,
        "ttl_seconds": CACHE_TTL,
        "thesis": thesis.model_dump(by_alias=True, mode="json"),
    })


def _get_all() -> JSONResponse:
    items = []
    for sym in CANONICAL_SYMBOLS:
        thesis = _cache_get(sym) or load_latest(sym)
        if thesis is not None:
            items.append({
                "symbol": sym,
                "direction": thesis.action.direction,
                "confidence": thesis.confidence,
                "prob_bull": thesis.probabilities.bull,
                "prob_bear": thesis.probabilities.bear,
                "one_liner": thesis.action.voice_one_liner,
                "freshness": thesis.freshness.overall,
                "thesis_id": thesis.metadata.thesis_id,
            })
        else:
            items.append({
                "symbol": sym,
                "direction": "unknown",
                "confidence": 0,
                "prob_bull": 33,
                "prob_bear": 33,
                "one_liner": f"{sym} : thèse non disponible.",
                "freshness": "missing",
                "thesis_id": None,
            })

    return JSONResponse(content={
        "ok": True,
        "count": len(items),
        "symbols": items,
    })


@app.get("/health")
def health():
    return {"ok": True, "module": "market_thesis", "version": "1.0.0"}


# ── Reliability / Calibration Endpoints (PR10) ──────────────────────────

@app.get("/read/thesis/reliability")
def read_reliability(symbol: str = Query(None)):
    """Get reliability/calibration stats. ?symbol=BTC for single, or all."""
    from .calibration_engine import calibrate, calibrate_all
    from .reliability_engine import evaluate_reliability, evaluate_all_reliability

    if symbol:
        sym = symbol.upper()
        cal = calibrate(sym)
        rel = evaluate_reliability(sym)
        return {
            "ok": True,
            "symbol": sym,
            "sample_size": rel.sample_size,
            "accuracy_pct": cal.accuracy_pct,
            "correct_count": cal.correct_count,
            "incorrect_count": cal.incorrect_count,
            "confidence_error": cal.confidence_error,
            "probability_error": cal.probability_error,
            "reliability_score": rel.reliability_score,
            "reliability_grade": rel.grade,
            "bullish_win_rate": cal.bullish_win_rate,
            "bearish_win_rate": cal.bearish_win_rate,
            "mean_return_pct": cal.mean_return_pct,
        }

    # All symbols
    all_cal = calibrate_all()
    all_rel = evaluate_all_reliability()
    items = []
    for cal, rel in zip(all_cal.by_symbol, all_rel):
        items.append({
            "symbol": cal.symbol,
            "sample_size": cal.sample_size,
            "accuracy_pct": cal.accuracy_pct,
            "confidence_error": cal.confidence_error,
            "reliability_score": rel.reliability_score,
            "reliability_grade": rel.grade,
        })

    return {
        "ok": True,
        "total_outcomes": all_cal.total_outcomes,
        "total_correct": all_cal.total_correct,
        "overall_accuracy_pct": all_cal.overall_accuracy_pct,
        "symbols": items,
    }
