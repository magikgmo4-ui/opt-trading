from __future__ import annotations

from collectors_core import ValidationError
from collectors_core.http import JsonHttpClient

from .config import CoinGeckoRuntimeConfig


class CoinGeckoClient:
    def __init__(self, config: CoinGeckoRuntimeConfig) -> None:
        headers = {
            "Accept": "application/json",
            "User-Agent": config.api_user_agent,
            config.auth_header_name: config.api_key or "",
        }
        self._http = JsonHttpClient(
            base_url=config.api_base_url,
            default_headers=headers,
            timeout_seconds=config.api_timeout_seconds,
        )
        self._config = config

    def ping(self) -> dict[str, object]:
        response = self._http.get_json("/ping")
        if not isinstance(response.data, dict):
            raise ValidationError("CoinGecko /ping did not return a JSON object")
        if "gecko_says" not in response.data:
            raise ValidationError("CoinGecko /ping response missing gecko_says")
        return response.data

    def fetch_markets(self) -> list[dict[str, object]]:
        params = {
            "vs_currency": self._config.collection_vs_currency,
            "ids": ",".join(self._config.collection_coin_ids),
            "sparkline": str(self._config.collection_sparkline).lower(),
            "locale": self._config.collection_locale,
            "precision": self._config.collection_precision,
        }
        if self._config.collection_price_change_percentage:
            params["price_change_percentage"] = ",".join(self._config.collection_price_change_percentage)

        response = self._http.get_json("/coins/markets", params=params)
        if not isinstance(response.data, list):
            raise ValidationError("CoinGecko /coins/markets did not return a JSON array")
        return response.data
