"""Live collector framework for stock_true_value — Yahoo Finance adapter (Phase 6).

Activation: 1 collector at a time. Current: Yahoo Finance only.
Other sources (SEC, TV, ETF, Analyst) are stubs to be activated later.
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "stock_true_value" / "latest"

WATCHLIST = ["SPCX", "NVDA", "AVGO", "AMD", "MRVL", "MU", "PLTR", "RKLB", "ASTS", "LUNR"]

COLLECTOR_STATUS = {
    "yahoo_finance": "active",
    "sec_edgar": "stub",
    "etf_flows": "stub",
    "analyst_revisions": "stub",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _yahoo_quote(symbol: str, timeout: int = 10) -> dict[str, Any]:
    safe = urllib.parse.quote(symbol)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{safe}?range=1d&interval=1d"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 opt-trading stock_true_value"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"symbol": symbol, "ok": False, "error": str(e)}

    result = (data.get("chart", {}).get("result") or [None])[0]
    if not result:
        return {"symbol": symbol, "ok": False, "error": "no chart result"}
    meta = result.get("meta", {})
    return {
        "symbol": symbol,
        "ok": True,
        "price": meta.get("regularMarketPrice"),
        "previous_close": meta.get("chartPreviousClose"),
        "currency": meta.get("currency"),
        "exchange": meta.get("exchangeName"),
    }


def _price_to_raw_scores(quote: dict) -> dict:
    """Convert Yahoo quote to raw scores expected by scoring_engine.
    
    This is a minimal mapping — live data provides only price-related signals.
    Full multi-source scoring requires SEC, ETF, Analyst collectors (stubs).
    """
    price = quote.get("price") or 0
    prev_close = quote.get("previous_close") or price or 1
    change_pct = ((price - prev_close) / prev_close * 100) if prev_close else 0

    return {
        "fundamental_score": min(100, max(0, 50 + change_pct * 2)),
        "valuation_score": min(100, max(0, 50 + (1 - price / 500 if price else 50))),
        "flow_score": 50.0,
        "speculation_score": 50.0,
        "surprise_score": min(100, max(0, 50 + abs(change_pct) * 2)),
        "catalyst_score": 50.0,
        "ecosystem_score": 50.0,
    }


def _build_source_health(collected: int, errors: int) -> dict:
    return {
        "required_sources_available": collected,
        "optional_sources_available": 0,
        "missing_sources": [],
        "stale_sources": [],
        "data_conflicts": [],
    }


def collect_and_score(dry_run: bool = False) -> dict:
    """Fetch live Yahoo data for watchlist, score each ticker, write outputs."""
    from modules.stock_true_value.scoring_engine import (
        compute_score_snapshot,
        MODEL_VERSION,
    )

    results: list[dict] = []
    sources_ok = 0
    sources_err = 0

    for ticker in WATCHLIST:
        quote = _yahoo_quote(ticker)
        if not quote.get("ok"):
            sources_err += 1
            print(f"  {ticker}: fetch failed — {quote.get('error')}")
            continue
        sources_ok += 1

        raw = _price_to_raw_scores(quote)
        snapshot = compute_score_snapshot(
            ticker=ticker,
            universe="spacex_watchlist",
            raw_scores=raw,
            source_health_payload={"required_sources_available": 1, "optional_sources_available": 0,
                                   "missing_sources": [], "stale_sources": [], "data_conflicts": []},
        )
        results.append(snapshot.to_dict())

    output = {
        "asof": _utc_now(),
        "model_version": MODEL_VERSION,
        "items": results,
        "summary": {
            "count": len(results),
            "low_confidence_count": sum(1 for r in results if r["confidence_score"] < 60),
            "grades": _count_grades(results),
            "collector_status": COLLECTOR_STATUS,
            "sources_ok": sources_ok,
            "sources_err": sources_err,
        },
    }

    if not dry_run:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        scores_path = OUTPUT_DIR / "scores.json"
        scores_path.write_text(json.dumps(output, indent=2))
        _write_summary_md(output, scores_path)

    return output


def _count_grades(results: list[dict]) -> dict:
    grades = {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "RESEARCH_REQUIRED": 0}
    for r in results:
        g = r.get("final_grade", "?")
        if g in grades:
            grades[g] += 1
        else:
            grades["RESEARCH_REQUIRED"] += 1
    return grades


def _write_summary_md(output: dict, scores_path: Path):
    lines = [
        "# Stock / SpaceX True Value — Live Summary",
        "",
        f"- asof: `{output['asof']}`",
        f"- model_version: `{output['model_version']}`",
        f"- items: `{output['summary']['count']}`",
        "",
        "| Ticker | Grade | True Value | Hype | Risk | Confidence | Action |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for it in output["items"]:
        lines.append(
            f"| {it['ticker']} | {it['final_grade']} | {it['true_value_score']:.1f} | "
            f"{it['hype_score']:.1f} | {it['risk_score']:.1f} | "
            f"{it['confidence_score']:.1f} | {it['action_bias']} |"
        )
    summary_path = OUTPUT_DIR / "summary.md"
    summary_path.write_text("\n".join(lines))


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    result = collect_and_score(dry_run=dry)
    print(f"\nItems: {result['summary']['count']} | "
          f"Sources: {result['summary']['sources_ok']} ok / {result['summary']['sources_err']} err | "
          f"Grades: {result['summary']['grades']}")
    if dry:
        print("DRY RUN — no files written.")
