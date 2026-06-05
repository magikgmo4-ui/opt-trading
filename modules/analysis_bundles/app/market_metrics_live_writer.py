"""
market_metrics_live_writer — real market_metrics.v1 from Binance spot collector.

Replaces synthetic market_metrics with live data from collector_binance_spot.
Runs the collector oneshot, reads its output, converts to market_metrics.v1.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from modules.derivatives_collector.app.market_metrics_v1 import (
    MarketMetricsV1,
    MetricsPayload,
    ProviderCoverage,
    Refs,
)

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_COLLECTOR_DIR = _PROJECT_ROOT / "modules" / "collector_binance_spot"
_COLLECTOR_OUTPUTS = _COLLECTOR_DIR / "outputs" / "normalized"
_MARKET_METRICS_LATEST = _PROJECT_ROOT / "data" / "data_center" / "views" / "market_metrics" / "latest.json"
_MARKET_METRICS_BY_SYMBOL = _PROJECT_ROOT / "data" / "data_center" / "views" / "market_metrics" / "by_symbol"

_PYTHONPATH = f"src:{_PROJECT_ROOT}/packages/collectors_core/src"


def _run_collector() -> Optional[Path]:
    """Run collector_binance_spot oneshot, return path to normalized output or None."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "collector_binance_spot.cli", "run"],
            cwd=str(_COLLECTOR_DIR),
            capture_output=True,
            text=True,
            timeout=30,
            env={**__import__("os").environ, "PYTHONPATH": _PYTHONPATH},
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        normalized = data.get("normalized_output", "")
        if normalized:
            return _COLLECTOR_DIR / normalized
    except Exception:
        pass
    return None


def _read_collected_prices(normalized_path: Optional[Path] = None) -> dict[str, float]:
    """Read collected prices from Binance output. Returns {symbol: price} or empty."""
    if normalized_path is None:
        # Find latest normalized file
        files = sorted(_COLLECTOR_OUTPUTS.glob("pair_market_snapshot_*.json"))
        if not files:
            return {}
        normalized_path = files[-1]

    if not normalized_path or not normalized_path.exists():
        return {}

    try:
        data = json.loads(normalized_path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    records = data.get("records", [])
    if not isinstance(records, list):
        return {}

    prices = {}
    for r in records:
        if not isinstance(r, dict):
            continue
        symbol = r.get("pair_symbol", "")
        price = r.get("last_price", "")
        if symbol and price:
            try:
                prices[symbol] = float(price)
            except (ValueError, TypeError):
                pass

    return prices


def write_live_market_metrics(symbol: str = "BTCUSDT") -> Optional[MarketMetricsV1]:
    """Run collector and write real market_metrics.v1 for a symbol."""
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    normalized_path = _run_collector()
    prices = _read_collected_prices(normalized_path)
    price = prices.get(symbol)

    if price is None:
        return None

    mm = MarketMetricsV1(
        contract_version="v1",
        input_class="market_metrics.v1",
        module_id="analysis_bundles.live",
        symbol=symbol,
        metrics_ts=now_iso,
        freshness_state="fresh",
        provider_id="binance_spot",
        provider_coverage=ProviderCoverage(
            status="partial",
            collectable_metrics=["open_interest"],
            missing_metrics=["funding_rate", "volume_futures", "long_short_ratio", "liquidations_long", "liquidations_short"],
        ),
        metrics=MetricsPayload(
            open_interest=None,
            funding_rate=None,
            volume_futures=None,
        ),
        refs=Refs(
            primary_output=str(_MARKET_METRICS_BY_SYMBOL / f"{symbol}.json"),
            meta_output=str(_MARKET_METRICS_BY_SYMBOL / "meta.json"),
            latest=str(_MARKET_METRICS_LATEST),
            status="live_from_binance",
        ),
        warnings=[],
    )

    # Write price in extra field (market_metrics_v1 doesn't have a direct price field in metrics)
    # Add a custom extra field for the live price
    mm_dict = mm.__dict__.copy()
    mm_dict["last_price"] = price
    mm_dict["provider_coverage"] = mm.provider_coverage.__dict__
    mm_dict["metrics"] = mm.metrics.__dict__
    mm_dict["refs"] = mm.refs.__dict__

    _MARKET_METRICS_BY_SYMBOL.mkdir(parents=True, exist_ok=True)
    sym_path = _MARKET_METRICS_BY_SYMBOL / f"{symbol}.json"
    sym_path.write_text(json.dumps(mm_dict, indent=2, default=str), encoding="utf-8")

    _MARKET_METRICS_LATEST.parent.mkdir(parents=True, exist_ok=True)
    _MARKET_METRICS_LATEST.write_text(json.dumps(mm_dict, indent=2, default=str), encoding="utf-8")

    return mm


def write_all_live() -> list[str]:
    """Run collector once, write real market_metrics for all collected symbols. BTC last to win latest.json."""
    normalized_path = _run_collector()
    prices = _read_collected_prices(normalized_path)

    if not prices:
        return []

    # Write non-BTC first
    for symbol in prices:
        if symbol != "BTCUSDT":
            write_live_market_metrics(symbol)

    # BTC last → wins latest.json
    if "BTCUSDT" in prices:
        write_live_market_metrics("BTCUSDT")

    return list(prices.keys())
