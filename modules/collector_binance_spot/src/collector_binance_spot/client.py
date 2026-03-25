from __future__ import annotations

import json

from collectors_core import ValidationError
from collectors_core.http import JsonHttpClient

from .config import BinanceSpotRuntimeConfig


class BinanceSpotClient:
    def __init__(self, config: BinanceSpotRuntimeConfig) -> None:
        headers = {
            "Accept": "application/json",
            "User-Agent": config.api_user_agent,
        }
        self._http = JsonHttpClient(
            base_url=config.api_base_url,
            default_headers=headers,
            timeout_seconds=config.api_timeout_seconds,
        )
        self._config = config

    def ping(self) -> dict[str, object]:
        response = self._http.get_json("/api/v3/ping")
        if not isinstance(response.data, dict):
            raise ValidationError("Binance Spot /api/v3/ping did not return a JSON object")
        return response.data

    def fetch_exchange_info(self) -> dict[str, object]:
        response = self._http.get_json(
            "/api/v3/exchangeInfo",
            params={"symbols": _encode_symbols_param(self._config.collection_symbols)},
        )
        if not isinstance(response.data, dict):
            raise ValidationError("Binance Spot /api/v3/exchangeInfo did not return a JSON object")
        return response.data

    def fetch_ticker_24hr(self) -> list[dict[str, object]]:
        response = self._http.get_json(
            "/api/v3/ticker/24hr",
            params={
                "symbols": _encode_symbols_param(self._config.collection_symbols),
                "type": self._config.collection_ticker_type,
            },
        )
        if isinstance(response.data, dict):
            return [response.data]
        if not isinstance(response.data, list):
            raise ValidationError("Binance Spot /api/v3/ticker/24hr did not return a JSON array")
        return response.data


def _encode_symbols_param(symbols: tuple[str, ...]) -> str:
    return json.dumps(list(symbols), separators=(",", ":"))
