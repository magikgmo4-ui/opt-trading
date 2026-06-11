"""
external_data_producers.py — collect missing data from free APIs → data_center.

Providers:
    AlphaVantage (free key) — forex rates, stock prices
    FRED (free key) — US macro data (interest rates, GDP)
    Finnhub (free key) — news, sentiment, company data
    TwelveData (free key) — OHLCV historical

Writes to data_center views:
    fx_context.v1, macro_event.v1, news_event.v1, equity_context.v1

Usage:
    python -m modules.data_center.external_data_producers
    python -m modules.data_center.external_data_producers --provider alphavantage
"""

from __future__ import annotations

import json
import os
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"


def _atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp") as fh:
        json.dump(payload, fh, indent=2, default=str)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def _fetch_json(url: str) -> Optional[dict]:
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  fetch error: {e}")
        return None


def _get_key(env_var: str) -> str:
    # Ensure env is loaded
    try:
        from modules.env.env import load_env
        load_env()
    except Exception:
        pass
    return os.getenv(env_var, "").strip()


# ═══════════════════════════════════════════════════════════════════
# AlphaVantage — forex rates + stock prices
# ═══════════════════════════════════════════════════════════════════

_FOREX_PAIRS = [
    ("EUR", "USD"), ("GBP", "USD"), ("USD", "JPY"), ("USD", "CAD"),
    ("AUD", "USD"), ("NZD", "USD"), ("USD", "CHF"),
    ("EUR", "JPY"), ("GBP", "JPY"), ("EUR", "GBP"),
]

def produce_fx_context() -> dict:
    """Fetch forex rates from AlphaVantage → fx_context.v1."""
    key = _get_key("ALPHAVANTAGE_API_KEY")
    if not key:
        return {"error": "ALPHAVANTAGE_API_KEY not set"}
    now = datetime.now(timezone.utc).isoformat()
    results = {}

    for base, quote in _FOREX_PAIRS:
        pair = f"{base}/{quote}"
        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={base}&to_currency={quote}&apikey={key}"
        data = _fetch_json(url)
        if not data:
            continue
        rate_data = data.get("Realtime Currency Exchange Rate", {})
        if not rate_data:
            continue
        price = float(rate_data.get("5. Exchange Rate", 0))
        if not price:
            continue

        sym_safe = pair.replace("/", "_")
        snap_dir = _VIEWS_DIR / "fx_context" / "by_symbol" / sym_safe
        snap_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write(snap_dir / "latest.json", {
            "input_class": "fx_context.v1",
            "provider_id": "alphavantage",
            "symbol": pair,
            "produced_at": now,
            "rate": price,
            "bid": float(rate_data.get("8. Bid Price", 0)),
            "ask": float(rate_data.get("9. Ask Price", 0)),
            "refresh_ts": rate_data.get("6. Last Refreshed", ""),
        })
        results[pair] = price

    # Global
    _atomic_write(_VIEWS_DIR / "fx_context" / "latest.json", {
        "input_class": "fx_context.v1",
        "provider_id": "alphavantage",
        "produced_at": now,
        "total_pairs": len(results),
        "pairs": [{"symbol": k, "rate": v} for k, v in sorted(results.items())],
    })

    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write("alphavantage", "fx_context.v1",
        str(_VIEWS_DIR / "fx_context" / "latest.json"), "ok", {"pairs": len(results)})
    return {"produced_at": now, "pairs": len(results)}


# ═══════════════════════════════════════════════════════════════════
# FRED — US macro (Fed funds rate, GDP, CPI, unemployment)
# ═══════════════════════════════════════════════════════════════════

_FRED_SERIES = {
    "FEDFUNDS": {"label": "Fed Funds Rate", "unit": "%"},
    "GDP": {"label": "GDP", "unit": "B USD"},
    "CPIAUCSL": {"label": "CPI All Items", "unit": "index"},
    "UNRATE": {"label": "Unemployment Rate", "unit": "%"},
    "DGS10": {"label": "10Y Treasury Yield", "unit": "%"},
    "T10Y2Y": {"label": "10Y-2Y Spread", "unit": "%"},
    "VIXCLS": {"label": "VIX Close", "unit": "index"},
}


def produce_macro_context() -> dict:
    """Fetch US macro indicators from FRED → macro_event.v1."""
    key = _get_key("FRED_API_KEY")
    if not key:
        return {"error": "FRED_API_KEY not set"}
    now = datetime.now(timezone.utc).isoformat()
    results = {}

    for series_id, info in _FRED_SERIES.items():
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={key}&file_type=json&sort_order=desc&limit=1"
        data = _fetch_json(url)
        if not data:
            continue
        obs = data.get("observations", [])
        if not obs:
            continue
        value = obs[0].get("value", "")
        try:
            value_float = float(value)
        except (ValueError, TypeError):
            continue

        results[series_id] = {"label": info["label"], "value": value_float, "unit": info["unit"], "date": obs[0].get("date", "")}

    _atomic_write(_VIEWS_DIR / "macro_event" / "latest.json", {
        "input_class": "macro_event.v1",
        "provider_id": "fred",
        "produced_at": now,
        "indicators": results,
    })

    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write("fred", "macro_event.v1",
        str(_VIEWS_DIR / "macro_event" / "latest.json"), "ok", {"indicators": len(results)})
    return {"produced_at": now, "indicators": len(results)}


# ═══════════════════════════════════════════════════════════════════
# Finnhub — news + company data
# ═══════════════════════════════════════════════════════════════════

def produce_news_context() -> dict:
    """Fetch general market news from Finnhub → news_event.v1."""
    key = _get_key("FINNHUB_API_KEY")
    if not key:
        return {"error": "FINNHUB_API_KEY not set"}
    now = datetime.now(timezone.utc).isoformat()
    url = f"https://finnhub.io/api/v1/news?category=general&token={key}"
    data = _fetch_json(url)
    if not data or not isinstance(data, list):
        return {"error": "no news data"}

    articles = []
    for item in data[:20]:
        articles.append({
            "headline": item.get("headline", ""),
            "summary": (item.get("summary", "") or "")[:200],
            "source": item.get("source", ""),
            "published_at": datetime.fromtimestamp(item.get("datetime", 0), tz=timezone.utc).isoformat() if item.get("datetime") else "",
            "category": item.get("category", ""),
        })

    _atomic_write(_VIEWS_DIR / "news_event" / "latest.json", {
        "input_class": "news_event.v1",
        "provider_id": "finnhub",
        "produced_at": now,
        "total_articles": len(articles),
        "articles": articles,
    })

    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write("finnhub", "news_event.v1",
        str(_VIEWS_DIR / "news_event" / "latest.json"), "ok", {"articles": len(articles)})
    return {"produced_at": now, "articles": len(articles)}


# ═══════════════════════════════════════════════════════════════════
# TwelveData — OHLCV historical (backtest)
# ═══════════════════════════════════════════════════════════════════

def produce_ohlcv_history(symbols: Optional[list[str]] = None) -> dict:
    """Fetch OHLCV historical from TwelveData for backtesting."""
    key = _get_key("TWELVEDATA_API_KEY")
    if not key:
        return {"error": "TWELVEDATA_API_KEY not set"}
    syms = symbols or ["XAU/USD", "BTC/USD", "ETH/USD", "EUR/USD"]
    now = datetime.now(timezone.utc).isoformat()
    results = {}

    for sym in syms:
        url = f"https://api.twelvedata.com/time_series?symbol={sym.replace('/','')}&interval=1day&outputsize=90&apikey={key}"
        data = _fetch_json(url)
        if not data or data.get("status") == "error":
            continue
        values = data.get("values", [])
        klines = []
        for v in reversed(values):
            klines.append({
                "datetime": v.get("datetime", ""),
                "open": float(v.get("open", 0)),
                "high": float(v.get("high", 0)),
                "low": float(v.get("low", 0)),
                "close": float(v.get("close", 0)),
            })

        sym_safe = sym.replace("/", "_")
        hist_dir = _PROJECT_ROOT / "data" / "market_data" / "klines" / sym_safe
        hist_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write(hist_dir / "latest.json", {
            "input_class": "market_klines.v1",
            "provider_id": "twelvedata",
            "symbol": sym,
            "interval": "1d",
            "produced_at": now,
            "klines": klines,
        })
        results[sym] = len(klines)

    return {"produced_at": now, "pairs": results}


# ═══════════════════════════════════════════════════════════════════
# EIA — Commodities inventory (P15)
# ═══════════════════════════════════════════════════════════════════

def produce_commodity_context() -> dict:
    """Fetch US energy data from EIA → commodity_inventory.v1."""
    key = _get_key("EIA_API_KEY")
    if not key:
        return {"error": "EIA_API_KEY not set"}
    now = datetime.now(timezone.utc).isoformat()
    # EIA series: PET.RWTC.D (WTI Crude), PET.RBRTE.D (Brent), NG.RNGWHHD.D (Natural Gas)
    series = {"WTI": "PET.RWTC.D", "BRENT": "PET.RBRTE.D", "NATGAS": "NG.RNGWHHD.D"}
    results = {}
    for label, series_id in series.items():
        url = f"https://api.eia.gov/v2/seriesid/{series_id}?api_key={key}&length=1"
        data = _fetch_json(url)
        if not data:
            continue
        resp = data.get("response", {})
        rows = resp.get("data", [])
        if rows and isinstance(rows[0], list) and len(rows[0]) >= 2:
            results[label] = {"price": rows[0][1], "unit": resp.get("unit", "?"), "date": rows[0][0]}

    _atomic_write(_VIEWS_DIR / "commodity_inventory" / "latest.json", {
        "input_class": "commodity_inventory.v1", "provider_id": "eia",
        "produced_at": now, "commodities": results,
    })
    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write("eia", "commodity_inventory.v1",
        str(_VIEWS_DIR / "commodity_inventory" / "latest.json"), "ok", {"commodities": len(results)})
    return {"produced_at": now, "commodities": len(results)}


# ═══════════════════════════════════════════════════════════════════
# Rates context — FRED rates → rates_context.v1 (P6)
# ═══════════════════════════════════════════════════════════════════

def produce_rates_context() -> dict:
    """Consolidate FRED rates into rates_context.v1."""
    key = _get_key("FRED_API_KEY")
    if not key:
        return {"error": "FRED_API_KEY not set"}
    now = datetime.now(timezone.utc).isoformat()
    rates_series = {"FEDFUNDS": "Fed Funds", "DGS10": "10Y Yield", "DGS2": "2Y Yield", "T10Y2Y": "10Y-2Y Spread"}
    results = {}
    for sid, label in rates_series.items():
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={sid}&api_key={key}&file_type=json&sort_order=desc&limit=1"
        data = _fetch_json(url)
        if not data:
            continue
        obs = data.get("observations", [])
        if obs:
            try:
                results[label] = {"value": float(obs[0]["value"]), "date": obs[0]["date"]}
            except (ValueError, TypeError):
                pass

    _atomic_write(_VIEWS_DIR / "rates_context" / "latest.json", {
        "input_class": "rates_context.v1", "provider_id": "fred",
        "produced_at": now, "rates": results,
    })
    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write("fred", "rates_context.v1",
        str(_VIEWS_DIR / "rates_context" / "latest.json"), "ok", {"rates": len(results)})
    return {"produced_at": now, "rates": len(results)}


# ═══════════════════════════════════════════════════════════════════
# Crypto derivatives state — consolidate OI/funding/liq (P14)
# ═══════════════════════════════════════════════════════════════════

def produce_crypto_derivatives_state() -> dict:
    """Aggregate crypto derivatives data from existing sources → crypto_derivatives_state.v1."""
    now = datetime.now(timezone.utc).isoformat()
    # Read from existing views
    sources = {}
    # Coinglass OCR
    cg_path = _VIEWS_DIR / "vision_context" / "coinglass" / "latest.json"
    if cg_path.exists():
        try:
            cg = json.loads(cg_path.read_text(encoding="utf-8"))
            for d in cg.get("detections", []):
                sources[d.get("detected_metric_type", "")] = {"value": d.get("extracted_value"), "source": "coinglass_ocr"}
        except Exception:
            pass
    # Market metrics (OI from derivatives collector if available)
    mm_path = _VIEWS_DIR / "market_metrics" / "latest.json"
    if mm_path.exists():
        try:
            mm = json.loads(mm_path.read_text(encoding="utf-8"))
        except Exception:
            mm = {}

    _atomic_write(_VIEWS_DIR / "crypto_derivatives_state" / "latest.json", {
        "input_class": "crypto_derivatives_state.v1",
        "provider_id": "data_center_aggregator",
        "produced_at": now,
        "metrics": sources,
    })
    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write("data_center_aggregator", "crypto_derivatives_state.v1",
        str(_VIEWS_DIR / "crypto_derivatives_state" / "latest.json"), "ok")
    return {"produced_at": now, "metrics": len(sources)}


# ═══════════════════════════════════════════════════════════════════
# Flow positioning — aggregate whale + liquidations + OI (P10)
# ═══════════════════════════════════════════════════════════════════

def produce_flow_positioning() -> dict:
    """Aggregate whale flows + liquidations → flow_positioning.v1."""
    now = datetime.now(timezone.utc).isoformat()
    flows = []
    # Read from telegram_context (whale transfers)
    ctx_path = _VIEWS_DIR / "telegram_context" / "latest.json"
    if ctx_path.exists():
        try:
            ctx = json.loads(ctx_path.read_text(encoding="utf-8"))
            flows.append({"source": "telegram_context", "count": ctx.get("context_signals", 0)})
        except Exception:
            pass

    _atomic_write(_VIEWS_DIR / "flow_positioning" / "latest.json", {
        "input_class": "flow_positioning.v1",
        "provider_id": "data_center_aggregator",
        "produced_at": now,
        "sources": flows,
    })
    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write("data_center_aggregator", "flow_positioning.v1",
        str(_VIEWS_DIR / "flow_positioning" / "latest.json"), "ok")
    return {"produced_at": now, "flows": len(flows)}


# ═══════════════════════════════════════════════════════════════════
# Yahoo Finance — fundamentals snapshot (P8)
# ═══════════════════════════════════════════════════════════════════

_FUNDAMENTAL_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BTC-USD", "ETH-USD", "GC=F"]


def produce_fundamental_snapshot() -> dict:
    now = datetime.now(timezone.utc).isoformat()
    results = {}
    for ticker in _FUNDAMENTAL_TICKERS[:5]:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1mo"
            data = _fetch_json(url)
            if not data:
                continue
            result = data.get("chart", {}).get("result", [])
            if not result:
                continue
            meta = result[0].get("meta", {})
            results[ticker] = {
                "price": meta.get("regularMarketPrice"),
                "previous_close": meta.get("previousClose"),
                "currency": meta.get("currency"),
            }
        except Exception:
            continue

    _atomic_write(_VIEWS_DIR / "fundamental_snapshot" / "latest.json", {
        "input_class": "fundamental_snapshot.v1",
        "provider_id": "yahoo_finance", "produced_at": now, "tickers": results,
    })
    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write("yahoo_finance", "fundamental_snapshot.v1",
        str(_VIEWS_DIR / "fundamental_snapshot" / "latest.json"), "ok", {"tickers": len(results)})
    return {"tickers": len(results)}


# ═══════════════════════════════════════════════════════════════════
# Deribit — crypto options surface (P5)
# ═══════════════════════════════════════════════════════════════════

def produce_options_surface() -> dict:
    now = datetime.now(timezone.utc).isoformat()
    results = {}
    for coin in ["BTC", "ETH"]:
        url = f"https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency={coin}&kind=option"
        data = _fetch_json(url)
        if not data:
            continue
        entries = data.get("result", [])
        results[coin] = {"total_options": len(entries), "sample": [e.get("instrument_name", "") for e in entries[:3]]}

    _atomic_write(_VIEWS_DIR / "options_surface" / "latest.json", {
        "input_class": "options_surface.v1", "provider_id": "deribit_public", "produced_at": now, "surfaces": results,
    })
    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write("deribit_public", "options_surface.v1",
        str(_VIEWS_DIR / "options_surface" / "latest.json"), "ok", {"coins": len(results)})
    return {"coins": len(results)}


# ═══════════════════════════════════════════════════════════════════
# Compliance state — risk config → compliance_state.v1 (P18)
# ═══════════════════════════════════════════════════════════════════

def produce_compliance_state() -> dict:
    now = datetime.now(timezone.utc).isoformat()
    risk = {}
    risk_path = _PROJECT_ROOT / "state" / "risk_config.json"
    if risk_path.exists():
        try:
            risk = json.loads(risk_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    _atomic_write(_VIEWS_DIR / "compliance_state" / "latest.json", {
        "input_class": "compliance_state.v1", "provider_id": "risk_engine",
        "produced_at": now, "risk_config": risk,
        "checks": {"risk_configured": bool(risk), "accounts_defined": len(risk.get("accounts", {}))},
    })
    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write("risk_engine", "compliance_state.v1",
        str(_VIEWS_DIR / "compliance_state" / "latest.json"), "ok")
    return {"accounts": len(risk.get("accounts", {}))}


# ═══════════════════════════════════════════════════════════════════

def produce_all() -> dict:
    from modules.env.env import load_env
    load_env()
    results = {}
    for name, fn in [
        ("fx_context", produce_fx_context),
        ("macro_event", produce_macro_context),
        ("news_event", produce_news_context),
        ("commodity_inventory", produce_commodity_context),
        ("rates_context", produce_rates_context),
        ("crypto_derivatives_state", produce_crypto_derivatives_state),
        ("flow_positioning", produce_flow_positioning),
        ("fundamental_snapshot", produce_fundamental_snapshot),
        ("options_surface", produce_options_surface),
        ("compliance_state", produce_compliance_state),
    ]:
        try:
            r = fn()
            results[name] = r
        except Exception as e:
            results[name] = {"error": str(e)}
    return results


if __name__ == "__main__":
    import sys
    from modules.env.env import load_env
    load_env()
    args = sys.argv[1:]
    provider = None
    i = 0
    while i < len(args):
        if args[i] == "--provider" and i + 1 < len(args):
            provider = args[i + 1]; i += 2
        else:
            i += 1

    if provider == "alphavantage":
        r = produce_fx_context()
        print(f"FX context: {r.get('pairs', 0)} pairs")
    elif provider == "fred":
        r = produce_macro_context()
        print(f"Macro: {r.get('indicators', 0)} indicators")
        r2 = produce_rates_context()
        print(f"Rates: {r2.get('rates', 0)} rates")
    elif provider == "finnhub":
        r = produce_news_context()
        print(f"News: {r.get('articles', 0)} articles")
    elif provider == "twelvedata":
        r = produce_ohlcv_history()
        print(f"OHLCV: {r.get('pairs', {})}")
    elif provider == "eia":
        r = produce_commodity_context()
        print(f"Commodities: {r.get('commodities', 0)}")
    elif provider == "crypto":
        r = produce_crypto_derivatives_state()
        print(f"Crypto derivatives: {r.get('metrics', 0)} metrics")
    elif provider == "flows":
        r = produce_flow_positioning()
        print(f"Flows: {r.get('flows', 0)} sources")
    elif provider == "yahoo":
        r = produce_fundamental_snapshot()
        print(f"Fundamentals: {r.get('tickers', 0)} tickers")
    elif provider == "deribit":
        r = produce_options_surface()
        print(f"Options: {r.get('coins', 0)} coins")
    elif provider == "compliance":
        r = produce_compliance_state()
        print(f"Compliance: {r.get('accounts', 0)} accounts")
    else:
        r = produce_all()
        for name, info in r.items():
            status = info.get("error", "OK")
            print(f"  {name}: {status}")
