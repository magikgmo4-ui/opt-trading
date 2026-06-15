"""Live collector framework for stock_true_value — Yahoo Finance + SEC EDGAR.

Activation: Yahoo Finance (Phase 6) + SEC EDGAR (Remediation R2).
Other sources (ETF, Analyst) are stubs to be activated later.
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
    "sec_edgar": "active",
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


def _sec_edgar_filings(cik: str = "1181412", timeout: int = 10) -> dict[str, Any]:
    """Fetch SEC EDGAR filings for given CIK. Default: SPCX (CIK 1181412)."""
    url = f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 opt-trading stock_true_value"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"cik": cik, "ok": False, "error": str(e)}
    filings = data.get("filings", {}).get("recent", {})
    forms = filings.get("form", [])[:20]
    dates = filings.get("filingDate", [])[:20]
    return {
        "cik": cik,
        "ok": True,
        "name": data.get("name", ""),
        "recent_forms": forms,
        "recent_dates": dates,
        "filing_count": len(forms),
    }


def _sec_signal(filings: dict) -> float:
    """Convert SEC filing activity to a signal score (0-100).
    
    Higher score = more recent and diverse filings.
    """
    if not filings.get("ok"):
        return 50.0
    forms = filings.get("recent_forms", [])
    if not forms:
        return 50.0
    # Score: more filings + more diverse forms = higher score
    unique_forms = len(set(forms))
    filing_count = len(forms)
    # 0-15 filings → 50-70, 15+ diverse → 70-100
    signal = min(100, 50 + unique_forms * 3 + filing_count * 0.5)
    return signal


def _price_to_raw_scores(quote: dict, sec_signal: float | None = None) -> dict:
    """Convert Yahoo quote + optional SEC signal to raw scores.
    
    SEC signal enriches fundamental_score when available.
    """
    price = quote.get("price") or 0
    prev_close = quote.get("previous_close") or price or 1
    change_pct = ((price - prev_close) / prev_close * 100) if prev_close else 0

    sec_boost = sec_signal if sec_signal is not None else 50.0

    return {
        "fundamental_score": min(100, max(0, (50 + change_pct * 2) * 0.6 + sec_boost * 0.4)),
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

    # Fetch SEC data once (SPCX only — CIK 1181412)
    sec_filings = _sec_edgar_filings()
    sec_signal_value = _sec_signal(sec_filings) if sec_filings.get("ok") else None
    print(f"  SEC EDGAR: {sec_filings.get('filing_count', 0)} filings, signal={sec_signal_value:.0f}" if sec_signal_value else "  SEC EDGAR: fetch failed")

    for ticker in WATCHLIST:
        quote = _yahoo_quote(ticker)
        if not quote.get("ok"):
            sources_err += 1
            print(f"  {ticker}: fetch failed — {quote.get('error')}")
            continue
        sources_ok += 1

        # Apply SEC signal only to SPCX
        ticker_sec = sec_signal_value if ticker == "SPCX" else None
        raw = _price_to_raw_scores(quote, ticker_sec)
        snapshot = compute_score_snapshot(
            ticker=ticker,
            universe="spacex_watchlist",
            raw_scores=raw,
            source_health_payload={"required_sources_available": 2 if ticker == "SPCX" else 1,
                                   "optional_sources_available": 0,
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
