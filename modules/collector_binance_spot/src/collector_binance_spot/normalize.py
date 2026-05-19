from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from collectors_core import ValidationError

from .config import BinanceSpotRuntimeConfig


def normalize_pair_market_snapshot(
    *,
    config: BinanceSpotRuntimeConfig,
    run_id: str,
    generated_at: str,
    exchange_info: dict[str, Any],
    ticker_items: list[dict[str, Any]],
) -> dict[str, Any]:
    symbol_entries = exchange_info.get("symbols")
    if not isinstance(symbol_entries, list):
        raise ValidationError("Binance Spot exchangeInfo response missing symbols list")

    metadata_by_symbol: dict[str, dict[str, Any]] = {}
    for item in symbol_entries:
        if not isinstance(item, dict):
            raise ValidationError("Binance Spot exchangeInfo symbol entry must be a JSON object")
        symbol = _require_string(item, "symbol")
        metadata_by_symbol[symbol] = item

    ticker_by_symbol: dict[str, dict[str, Any]] = {}
    for item in ticker_items:
        if not isinstance(item, dict):
            raise ValidationError("Binance Spot ticker item must be a JSON object")
        symbol = _require_string(item, "symbol")
        ticker_by_symbol[symbol] = item

    missing_metadata = [symbol for symbol in config.collection_symbols if symbol not in metadata_by_symbol]
    if missing_metadata:
        raise ValidationError(f"Binance Spot exchangeInfo missing requested symbols: {', '.join(missing_metadata)}")

    missing_tickers = [symbol for symbol in config.collection_symbols if symbol not in ticker_by_symbol]
    if missing_tickers:
        raise ValidationError(f"Binance Spot ticker/24hr missing requested symbols: {', '.join(missing_tickers)}")

    records = []
    for symbol in config.collection_symbols:
        meta = metadata_by_symbol[symbol]
        ticker = ticker_by_symbol[symbol]

        records.append(
            {
                "pair_symbol": symbol,
                "base_asset": _require_string(meta, "baseAsset"),
                "quote_asset": _require_string(meta, "quoteAsset"),
                "trading_status": _require_string(meta, "status"),
                "is_spot_trading_allowed": _require_bool(meta, "isSpotTradingAllowed"),
                "last_price": _require_decimal_string(ticker, "lastPrice"),
                "open_price_24h": _require_decimal_string(ticker, "openPrice"),
                "high_price_24h": _require_decimal_string(ticker, "highPrice"),
                "low_price_24h": _require_decimal_string(ticker, "lowPrice"),
                "price_change_percent_24h": _require_decimal_string(ticker, "priceChangePercent"),
                "volume_base_24h": _require_decimal_string(ticker, "volume"),
                "volume_quote_24h": _require_decimal_string(ticker, "quoteVolume"),
                "trade_count_24h": _require_int_like(ticker, "count"),
                "window_open_at": _ms_to_z(_require_int_like(ticker, "openTime")),
                "window_close_at": _ms_to_z(_require_int_like(ticker, "closeTime")),
                "weighted_avg_price_24h": _optional_decimal_string(ticker, "weightedAvgPrice"),
                "source": {"provider_symbol": symbol},
            }
        )

    return {
        "contract_version": config.contract_version,
        "schema_version": config.schema_version,
        "module_id": config.module_id,
        "provider_id": config.provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "entity_type": "pair_market_snapshot",
        "records": records,
    }


def _ms_to_z(value: int) -> str:
    return datetime.fromtimestamp(value / 1000, tz=UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _require_string(item: dict[str, Any], key: str) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"Missing required string field in Binance payload: {key}")
    return value.strip()


def _require_bool(item: dict[str, Any], key: str) -> bool:
    value = item.get(key)
    if not isinstance(value, bool):
        raise ValidationError(f"Field must be boolean in Binance payload: {key}")
    return value


def _require_decimal_string(item: dict[str, Any], key: str) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"Field must be a decimal string in Binance payload: {key}")
    return value.strip()


def _optional_decimal_string(item: dict[str, Any], key: str) -> str | None:
    value = item.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"Optional decimal field must be a string when present in Binance payload: {key}")
    return value.strip()


def _require_int_like(item: dict[str, Any], key: str) -> int:
    value = item.get(key)
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    raise ValidationError(f"Field must be an integer in Binance payload: {key}")
