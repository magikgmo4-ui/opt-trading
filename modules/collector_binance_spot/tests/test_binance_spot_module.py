from __future__ import annotations

import importlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "packages" / "collectors_core" / "src"))
sys.path.insert(0, str(REPO_ROOT / "modules" / "collector_binance_spot" / "src"))

load_runtime_config = importlib.import_module("collector_binance_spot.config").load_runtime_config
encode_symbols_param = importlib.import_module("collector_binance_spot.client")._encode_symbols_param
run_collection = importlib.import_module("collector_binance_spot.run").run_collection
run_sanity = importlib.import_module("collector_binance_spot.run").run_sanity
ConfigurationError = importlib.import_module("collectors_core").ConfigurationError
HttpRequestError = importlib.import_module("collectors_core").HttpRequestError


class FakeBinanceSpotClient:
    def ping(self) -> dict[str, object]:
        return {}

    def fetch_exchange_info(self) -> dict[str, object]:
        return {
            "timezone": "UTC",
            "serverTime": 1710000000000,
            "symbols": [
                {
                    "symbol": "BTCUSDT",
                    "status": "TRADING",
                    "baseAsset": "BTC",
                    "quoteAsset": "USDT",
                    "isSpotTradingAllowed": True,
                },
                {
                    "symbol": "ETHUSDT",
                    "status": "TRADING",
                    "baseAsset": "ETH",
                    "quoteAsset": "USDT",
                    "isSpotTradingAllowed": True,
                },
            ],
        }

    def fetch_ticker_24hr(self) -> list[dict[str, object]]:
        return [
            {
                "symbol": "BTCUSDT",
                "priceChangePercent": "1.25",
                "weightedAvgPrice": "51000.00",
                "lastPrice": "51200.00",
                "openPrice": "50500.00",
                "highPrice": "51500.00",
                "lowPrice": "50000.00",
                "volume": "1234.56000000",
                "quoteVolume": "63000000.00000000",
                "openTime": 1710000000000,
                "closeTime": 1710086400000,
                "count": 111111,
            },
            {
                "symbol": "ETHUSDT",
                "priceChangePercent": "-0.75",
                "weightedAvgPrice": "3000.00",
                "lastPrice": "2990.00",
                "openPrice": "3010.00",
                "highPrice": "3050.00",
                "lowPrice": "2950.00",
                "volume": "9876.54000000",
                "quoteVolume": "29600000.00000000",
                "openTime": 1710000000000,
                "closeTime": 1710086400000,
                "count": 222222,
            },
        ]


class FailingBinanceSpotClient:
    def __init__(self, exc: Exception) -> None:
        self._exc = exc

    def ping(self) -> dict[str, object]:
        raise self._exc

    def fetch_exchange_info(self) -> dict[str, object]:
        raise self._exc

    def fetch_ticker_24hr(self) -> list[dict[str, object]]:
        raise self._exc


class CollectorBinanceSpotTests(unittest.TestCase):
    def test_symbols_param_encoding_matches_binance_compact_array_format(self) -> None:
        self.assertEqual(encode_symbols_param(("BTCUSDT", "ETHUSDT")), '["BTCUSDT","ETHUSDT"]')

    def test_env_override_changes_symbol_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)
            with patch.dict("os.environ", {"COLLECTOR_BINANCE_SPOT__COLLECTION__SYMBOLS": "BTCUSDT,ETHUSDT"}, clear=False):
                config = load_runtime_config(module_dir)
            self.assertEqual(config.collection_symbols, ("BTCUSDT", "ETHUSDT"))

    def test_run_sanity_returns_ok_without_secret(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)
            result = run_sanity(module_dir, client=FakeBinanceSpotClient())
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["ping"], {})
            self.assertFalse((module_dir / "outputs" / "status.json").exists())

    def test_run_collection_writes_pair_market_snapshot_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)
            result = run_collection(module_dir, client=FakeBinanceSpotClient())

            status_payload = self._read_json(module_dir / "outputs" / "status.json")
            latest_payload = self._read_json(module_dir / "outputs" / "latest.json")
            manifest_payload = self._read_json(module_dir / "outputs" / "manifest.json")
            normalized_payload = self._read_json(module_dir / result["normalized_output"])
            events_payload = self._read_jsonl(module_dir / "outputs" / "events.jsonl")
            errors_payload = self._read_jsonl(module_dir / "outputs" / "errors.jsonl")
            raw_dir_contents = self._list_non_gitkeep(module_dir / "outputs" / "raw")

            self.assertEqual(result["status"], "healthy")
            self.assertEqual(status_payload["state"], "healthy")
            self.assertEqual(status_payload["run_id"], result["run_id"])
            self.assertEqual(normalized_payload["entity_type"], "pair_market_snapshot")
            self.assertEqual([record["pair_symbol"] for record in normalized_payload["records"]], ["BTCUSDT", "ETHUSDT"])
            self.assertEqual(latest_payload["summary"]["pair_symbols"], ["BTCUSDT", "ETHUSDT"])
            self.assertEqual(manifest_payload["normalized_contract"]["entity_type"], "pair_market_snapshot")
            self.assertEqual(manifest_payload["artifacts"]["errors"], "outputs/errors.jsonl")
            self.assertEqual(latest_payload["data_ref"], result["normalized_output"])
            self.assertEqual([event["event_type"] for event in events_payload], ["run_started", "output_published", "run_succeeded"])
            self.assertEqual(errors_payload, [])
            self.assertEqual(len(raw_dir_contents), 1)
            raw_run_dir = module_dir / "outputs" / "raw" / raw_dir_contents[0]
            self.assertTrue((raw_run_dir / "exchange_info.json").exists())
            self.assertTrue((raw_run_dir / "ticker_24hr.json").exists())

    def test_empty_symbol_list_fails_without_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)
            with patch.dict("os.environ", {"COLLECTOR_BINANCE_SPOT__COLLECTION__SYMBOLS": ""}, clear=False):
                with self.assertRaises(ConfigurationError):
                    run_collection(module_dir, client=FakeBinanceSpotClient())

            self.assertFalse((module_dir / "outputs" / "status.json").exists())
            self.assertFalse((module_dir / "outputs" / "manifest.json").exists())
            self.assertFalse((module_dir / "outputs" / "latest.json").exists())

    def test_recoverable_http_failure_after_success_sets_degraded(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)
            run_collection(module_dir, client=FakeBinanceSpotClient())
            original_latest = self._read_json(module_dir / "outputs" / "latest.json")
            original_manifest = self._read_json(module_dir / "outputs" / "manifest.json")

            recoverable_error = HttpRequestError("HTTP request failed", status_code=429, headers={"Retry-After": "60"})
            with self.assertRaises(HttpRequestError):
                run_collection(module_dir, client=FailingBinanceSpotClient(recoverable_error))

            status_payload = self._read_json(module_dir / "outputs" / "status.json")
            latest_payload = self._read_json(module_dir / "outputs" / "latest.json")
            manifest_payload = self._read_json(module_dir / "outputs" / "manifest.json")
            errors_payload = self._read_jsonl(module_dir / "outputs" / "errors.jsonl")
            self.assertEqual(status_payload["state"], "degraded")
            self.assertTrue(status_payload["retryable"])
            self.assertEqual(status_payload["last_error_code"], "http_429")
            self.assertIsNotNone(status_payload["retry_after"])
            self.assertEqual(latest_payload, original_latest)
            self.assertEqual(manifest_payload, original_manifest)
            self.assertEqual(errors_payload[-1]["error_code"], "http_429")
            self.assertTrue(errors_payload[-1]["retryable"])
            self.assertIsNotNone(errors_payload[-1]["retry_after"])

    def test_ip_ban_http_418_is_retryable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)
            run_collection(module_dir, client=FakeBinanceSpotClient())
            original_latest = self._read_json(module_dir / "outputs" / "latest.json")
            original_manifest = self._read_json(module_dir / "outputs" / "manifest.json")

            ban_error = HttpRequestError("HTTP request failed", status_code=418, headers={"Retry-After": "120"})
            with self.assertRaises(HttpRequestError):
                run_collection(module_dir, client=FailingBinanceSpotClient(ban_error))

            status_payload = self._read_json(module_dir / "outputs" / "status.json")
            latest_payload = self._read_json(module_dir / "outputs" / "latest.json")
            manifest_payload = self._read_json(module_dir / "outputs" / "manifest.json")
            errors_payload = self._read_jsonl(module_dir / "outputs" / "errors.jsonl")
            self.assertEqual(status_payload["state"], "degraded")
            self.assertTrue(status_payload["retryable"])
            self.assertIsNotNone(status_payload["retry_after"])
            self.assertEqual(latest_payload, original_latest)
            self.assertEqual(manifest_payload, original_manifest)
            self.assertEqual(errors_payload[-1]["error_code"], "http_418")
            self.assertTrue(errors_payload[-1]["retryable"])
            self.assertIsNotNone(errors_payload[-1]["retry_after"])

    def test_non_retryable_http_failure_after_success_sets_failed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)
            run_collection(module_dir, client=FakeBinanceSpotClient())
            original_latest = self._read_json(module_dir / "outputs" / "latest.json")
            original_manifest = self._read_json(module_dir / "outputs" / "manifest.json")
            auth_error = HttpRequestError("HTTP request failed", status_code=400, headers={})
            with self.assertRaises(HttpRequestError):
                run_collection(module_dir, client=FailingBinanceSpotClient(auth_error))

            status_payload = self._read_json(module_dir / "outputs" / "status.json")
            latest_payload = self._read_json(module_dir / "outputs" / "latest.json")
            manifest_payload = self._read_json(module_dir / "outputs" / "manifest.json")
            errors_payload = self._read_jsonl(module_dir / "outputs" / "errors.jsonl")
            self.assertEqual(status_payload["state"], "failed")
            self.assertFalse(status_payload["retryable"])
            self.assertEqual(status_payload["last_error_code"], "http_400")
            self.assertEqual(latest_payload, original_latest)
            self.assertEqual(manifest_payload, original_manifest)
            self.assertEqual(errors_payload[-1]["error_code"], "http_400")
            self.assertEqual(errors_payload[-1]["error_class"], "non_recoverable")

    def _copy_real_config(self, module_dir: Path) -> None:
        shutil.copytree(REPO_ROOT / "modules" / "collector_binance_spot" / "config", module_dir / "config")

    def _read_json(self, path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def _read_jsonl(self, path: Path) -> list[dict[str, Any]]:
        with path.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]

    def _list_non_gitkeep(self, path: Path) -> list[str]:
        return sorted(entry.name for entry in path.iterdir() if entry.name != ".gitkeep")


if __name__ == "__main__":
    unittest.main()
