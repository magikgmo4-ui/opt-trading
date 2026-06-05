"""
market_metrics_writer — synthetic market_metrics.v1 from vision analysis + coinglass OCR.

Derives approximate prices from vision analysis support/resistance levels.
Uses coinglass OCR stub data for OI/Funding metrics.
Writes valid market_metrics.v1 JSON files understood by the existing readers.
"""

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from modules.derivatives_collector.app.market_metrics_v1 import (
    MarketMetricsV1,
    MetricsPayload,
    ProviderCoverage,
    Refs,
)

from .vision_analysis_reader import extract_signals_from_vision, list_available_symbols

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_MARKET_METRICS_BY_SYMBOL = _PROJECT_ROOT / "data" / "data_center" / "views" / "market_metrics" / "by_symbol"
_MARKET_METRICS_LATEST = _PROJECT_ROOT / "data" / "data_center" / "views" / "market_metrics" / "latest.json"
_COINGLASS_LATEST = _PROJECT_ROOT / "data" / "deskpro" / "inputs" / "vision_context" / "coinglass" / "latest.json"

_SYMBOL_TO_MARKET = {
    "BTCUSDT.P": "BTCUSDT",
    "ETHUSDT.P": "ETHUSDT",
    "SOLUSDT.P": "SOLUSDT",
    "DOGEUSDT.P": "DOGEUSDT",
    "XRPUSDT.P": "XRPUSDT",
    "OANDA:XAUUSD": "XAUUSD",
    "TVC:DXY": "DXY",
    "SPY": "SPY",
    "NYMEX:CL1!": "WTI",
}


def _read_coinglass_oi() -> Optional[float]:
    if not _COINGLASS_LATEST.exists():
        return None
    try:
        data = json.loads(_COINGLASS_LATEST.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    detections = data.get("detections", [])
    if not isinstance(detections, list):
        return None
    for d in detections:
        if isinstance(d, dict) and d.get("detected_metric_type") == "open_interest":
            return d.get("extracted_value")
    return None


def _price_from_vision(symbol: str) -> Optional[float]:
    """Derive approximate price from vision analysis support/resistance midpoint."""
    signals = extract_signals_from_vision(symbol)
    if not signals.get("available"):
        return None
    supports = signals.get("supports", [])
    resistances = signals.get("resistances", [])
    if supports and resistances:
        sup_val = supports[0].get("value")
        res_val = resistances[0].get("value")
        if sup_val is not None and res_val is not None:
            return round((sup_val + res_val) / 2.0, 2)
    if supports:
        return supports[0].get("value")
    if resistances:
        return resistances[0].get("value")
    return None


def write_synthetic_market_metrics(symbol: str = "BTCUSDT") -> Optional[MarketMetricsV1]:
    """Write synthetic market_metrics.v1 for a symbol using vision analysis prices."""
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    # Find the vision symbol
    tv_symbol = None
    for tv, mkt in _SYMBOL_TO_MARKET.items():
        if mkt == symbol:
            tv_symbol = tv
            break
    if tv_symbol is None:
        tv_symbol = "BTCUSDT.P"

    price = _price_from_vision(tv_symbol)
    oi = _read_coinglass_oi()

    warnings = [
        "synthetic data: prices derived from vision analysis support/resistance levels",
        "data_quality=STUB: not from live exchange API",
    ]

    if price is None:
        warnings.append("no vision analysis available for price derivation")

    mm = MarketMetricsV1(
        contract_version="v1",
        input_class="market_metrics.v1",
        module_id="analysis_bundles.synthetic",
        symbol=symbol,
        metrics_ts=now_iso,
        freshness_state="fresh",
        provider_id="synthetic_from_vision",
        provider_coverage=ProviderCoverage(
            status="partial",
            collectable_metrics=["open_interest", "funding_rate"],
            missing_metrics=["volume_futures", "long_short_ratio", "liquidations_long", "liquidations_short"],
        ),
        metrics=MetricsPayload(
            open_interest=oi,
            funding_rate=0.0123,  # placeholder — from coinglass stub
        ),
        refs=Refs(
            primary_output=str(_MARKET_METRICS_BY_SYMBOL / f"{symbol}.json"),
            meta_output=str(_MARKET_METRICS_BY_SYMBOL / "meta.json"),
            latest=str(_MARKET_METRICS_LATEST),
            status="synthetic_from_vision",
        ),
        warnings=warnings,
    )

    # Write by-symbol
    _MARKET_METRICS_BY_SYMBOL.mkdir(parents=True, exist_ok=True)
    sym_path = _MARKET_METRICS_BY_SYMBOL / f"{symbol}.json"
    sym_path.write_text(json.dumps(asdict(mm), indent=2, default=str), encoding="utf-8")

    # Write latest (for readers that only read latest.json)
    _MARKET_METRICS_LATEST.parent.mkdir(parents=True, exist_ok=True)
    _MARKET_METRICS_LATEST.write_text(json.dumps(asdict(mm), indent=2, default=str), encoding="utf-8")

    return mm


def write_all() -> list[str]:
    """Write market_metrics: try live Binance first, fallback to synthetic from vision."""
    written = []

    # Write synthetic for all symbols first
    for tv_symbol, mkt_symbol in _SYMBOL_TO_MARKET.items():
        if _price_from_vision(tv_symbol) is not None:
            write_synthetic_market_metrics(mkt_symbol)
            written.append(mkt_symbol)

    # Then overwrite with live Binance data (wins — BTC last = latest.json = live)
    try:
        from .market_metrics_live_writer import write_all_live
        live = write_all_live()
        for sym in live:
            if sym not in written:
                written.append(sym)
    except Exception:
        pass

    return written
