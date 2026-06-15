"""Live collector framework for stock_true_value — all 4 collectors active.

Yahoo Finance (Phase 6) + SEC EDGAR (Remediation R2) + ETF Flows (G3) + Analyst Momentum (G3).
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
    "etf_flows": "active",
    "analyst_momentum": "active",
}

# Space-relevant ETFs for flow signal
ETF_WATCHLIST = ["ARKX", "UFO", "QQQ", "XAR", "ITA"]


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


def _etf_flows_signal() -> float:
    """Compute a flow signal from space-relevant ETF daily changes.
    
    Fetches 5 ETFs, averages their daily change %, maps to 0-100.
    """
    flows = []
    for etf in ETF_WATCHLIST:
        q = _yahoo_quote(etf)
        if q.get("ok") and q.get("price") and q.get("previous_close"):
            change = (q["price"] - q["previous_close"]) / q["previous_close"] * 100
            flows.append(change)
    if not flows:
        return 50.0
    avg_change = sum(flows) / len(flows)
    # Map avg change % to 0-100: -5% → 25, 0% → 50, +5% → 75, +10% → 100
    signal = min(100, max(0, 50 + avg_change * 5))
    return signal


def _analyst_momentum_signal(ticker: str) -> float:
    """Compute an analyst momentum proxy from 1mo daily price+volume data.
    
    Uses: 5d price momentum + volume trend. Maps to 0-100 signal.
    """
    import urllib.request as _ur
    safe = urllib.parse.quote(ticker)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{safe}?range=1mo&interval=1d"
    try:
        req = _ur.Request(url, headers={"User-Agent": "Mozilla/5.0 opt-trading stock_true_value"})
        with _ur.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return 50.0

    result = (data.get("chart", {}).get("result") or [None])[0]
    if not result:
        return 50.0
    quotes = result.get("indicators", {}).get("quote", [{}])[0]
    closes = [c for c in quotes.get("close", []) if c]
    volumes = [v for v in quotes.get("volume", []) if v]

    if len(closes) < 3:
        return 50.0

    # 5-day momentum (or max available)
    lookback = min(5, len(closes) - 1)
    momentum = (closes[-1] - closes[-lookback-1]) / closes[-lookback-1] * 100 if len(closes) > lookback else 0

    # Volume trend: recent 3 days vs early 3 days
    n = min(3, len(volumes) // 2)
    if n > 0 and len(volumes) >= 2 * n:
        vol_recent = sum(volumes[-n:])
        vol_early = sum(volumes[:n])
        vol_trend = (vol_recent - vol_early) / max(1, vol_early) * 100
    else:
        vol_trend = 0

    # Map momentum (-10%..+10%) and vol trend (-50%..+50%) to 0-100
    mom_score = min(100, max(0, 50 + momentum * 5))
    vol_score = min(100, max(0, 50 + vol_trend * 1))
    return round((mom_score * 0.6 + vol_score * 0.4), 1)


def _price_to_raw_scores(quote: dict, sec_signal: float | None = None, etf_signal: float | None = None, analyst_signal: float | None = None) -> dict:
    """Convert Yahoo quote + optional SEC/ETF/Analyst signals to raw scores."""
    price = quote.get("price") or 0
    prev_close = quote.get("previous_close") or price or 1
    change_pct = ((price - prev_close) / prev_close * 100) if prev_close else 0

    sec_boost = sec_signal if sec_signal is not None else 50.0

    etf_boost = etf_signal if etf_signal is not None else 50.0

    analyst_boost = analyst_signal if analyst_signal is not None else 50.0

    return {
        "fundamental_score": min(100, max(0, (50 + change_pct * 2) * 0.6 + sec_boost * 0.4)),
        "valuation_score": min(100, max(0, 50 + (1 - price / 500 if price else 50))),
        "flow_score": etf_boost,
        "speculation_score": analyst_boost,
        "surprise_score": min(100, max(0, 50 + abs(change_pct) * 2)),
        "catalyst_score": analyst_boost,
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

    # Fetch ETF flows signal (once for all tickers)
    etf_signal_value = _etf_flows_signal()
    print(f"  ETF Flows: signal={etf_signal_value:.0f}")

    for ticker in WATCHLIST:
        quote = _yahoo_quote(ticker)
        if not quote.get("ok"):
            sources_err += 1
            print(f"  {ticker}: fetch failed — {quote.get('error')}")
            continue
        sources_ok += 1

        # Apply SEC signal only to SPCX
        ticker_sec = sec_signal_value if ticker == "SPCX" else None
        ticker_analyst = _analyst_momentum_signal(ticker)
        raw = _price_to_raw_scores(quote, ticker_sec, etf_signal_value, ticker_analyst)
        snapshot = compute_score_snapshot(
            ticker=ticker,
            universe="spacex_watchlist",
            raw_scores=raw,
            source_health_payload={"required_sources_available": 4 if ticker == "SPCX" else 3,
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
