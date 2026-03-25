from __future__ import annotations

from typing import Any

from collectors_core import ValidationError, parse_z

from .config import CoinGeckoRuntimeConfig


def normalize_market_snapshot(
    *,
    config: CoinGeckoRuntimeConfig,
    run_id: str,
    generated_at: str,
    raw_items: list[dict[str, Any]],
) -> dict[str, Any]:
    items_by_provider_id: dict[str, dict[str, Any]] = {}
    for item in raw_items:
        if not isinstance(item, dict):
            raise ValidationError("CoinGecko market payload item must be a JSON object")
        provider_asset_id = _require_string(item, "id")
        items_by_provider_id[provider_asset_id] = item

    missing_ids = [coin_id for coin_id in config.collection_coin_ids if coin_id not in items_by_provider_id]
    if missing_ids:
        joined = ", ".join(missing_ids)
        raise ValidationError(f"CoinGecko did not return all requested coin ids: {joined}")

    records = []
    for provider_asset_id in config.collection_coin_ids:
        item = items_by_provider_id[provider_asset_id]
        last_updated = _require_string(item, "last_updated")
        parse_z(last_updated)

        records.append(
            {
                "asset_symbol": _require_string(item, "symbol").upper(),
                "asset_name": _require_string(item, "name"),
                "image_url": _optional_string(item, "image"),
                "price": _require_number_or_null(item, "current_price"),
                "market_cap": _require_number_or_null(item, "market_cap"),
                "market_cap_rank": _require_int_or_null(item, "market_cap_rank"),
                "total_volume": _require_number_or_null(item, "total_volume"),
                "high_24h": _require_number_or_null(item, "high_24h"),
                "low_24h": _require_number_or_null(item, "low_24h"),
                "price_change_percentage_24h": _require_number_or_null(item, "price_change_percentage_24h"),
                "circulating_supply": _require_number_or_null(item, "circulating_supply"),
                "total_supply": _require_number_or_null(item, "total_supply"),
                "max_supply": _require_number_or_null(item, "max_supply"),
                "last_updated": last_updated,
                "source": {"provider_asset_id": provider_asset_id},
            }
        )

    return {
        "contract_version": config.contract_version,
        "schema_version": config.schema_version,
        "module_id": config.module_id,
        "provider_id": config.provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "entity_type": "market_snapshot",
        "quote_currency": config.collection_vs_currency,
        "records": records,
    }


def _require_string(item: dict[str, Any], key: str) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"Missing required string field in CoinGecko payload: {key}")
    return value.strip()


def _optional_string(item: dict[str, Any], key: str) -> str | None:
    value = item.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


def _require_number_or_null(item: dict[str, Any], key: str) -> int | float | None:
    value = item.get(key)
    if value is None or isinstance(value, (int, float)):
        return value
    raise ValidationError(f"Field must be numeric or null in CoinGecko payload: {key}")


def _require_int_or_null(item: dict[str, Any], key: str) -> int | None:
    value = item.get(key)
    if value is None or isinstance(value, int):
        return value
    raise ValidationError(f"Field must be an integer or null in CoinGecko payload: {key}")
