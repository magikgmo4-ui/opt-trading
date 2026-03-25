from __future__ import annotations

import importlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "packages" / "collectors_core" / "src"))
sys.path.insert(0, str(REPO_ROOT / "modules" / "collector_coingecko" / "src"))

load_runtime_config = importlib.import_module("collector_coingecko.config").load_runtime_config
run_collection = importlib.import_module("collector_coingecko.run").run_collection
run_sanity = importlib.import_module("collector_coingecko.run").run_sanity
ConfigurationError = importlib.import_module("collectors_core").ConfigurationError
HttpRequestError = importlib.import_module("collectors_core").HttpRequestError


class FakeCoinGeckoClient:
    def ping(self) -> dict[str, str]:
        return {"gecko_says": "(V3) To the Moon!"}

    def fetch_markets(self) -> list[dict[str, object]]:
        return [
            {
                "id": "bitcoin",
                "symbol": "btc",
                "name": "Bitcoin",
                "image": "https://example.test/bitcoin.png",
                "current_price": 50000.0,
                "market_cap": 900000000000,
                "market_cap_rank": 1,
                "total_volume": 32000000000,
                "high_24h": 50500.0,
                "low_24h": 49000.0,
                "price_change_percentage_24h": 1.25,
                "circulating_supply": 19600000.0,
                "total_supply": 21000000.0,
                "max_supply": 21000000.0,
                "last_updated": "2026-03-18T10:00:00Z",
            },
            {
                "id": "ethereum",
                "symbol": "eth",
                "name": "Ethereum",
                "image": "https://example.test/ethereum.png",
                "current_price": 3000.0,
                "market_cap": 350000000000,
                "market_cap_rank": 2,
                "total_volume": 18000000000,
                "high_24h": 3050.0,
                "low_24h": 2950.0,
                "price_change_percentage_24h": -0.8,
                "circulating_supply": 120000000.0,
                "total_supply": 120000000.0,
                "max_supply": None,
                "last_updated": "2026-03-18T10:00:05Z",
            },
        ]


class FailingCoinGeckoClient:
    def __init__(self, exc: Exception) -> None:
        self._exc = exc

    def ping(self) -> dict[str, str]:
        raise self._exc

    def fetch_markets(self) -> list[dict[str, object]]:
        raise self._exc


class CollectorCoinGeckoTests(unittest.TestCase):
    def test_env_override_changes_vs_currency(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)

            with patch.dict(
                os.environ,
                {
                    "COLLECTOR_COINGECKO__API__KEY": "demo-key",
                    "COLLECTOR_COINGECKO__COLLECTION__VS_CURRENCY": "eur",
                },
                clear=False,
            ):
                config = load_runtime_config(module_dir)

            self.assertEqual(config.collection_vs_currency, "eur")
            self.assertEqual(config.api_key, "demo-key")

    def test_run_sanity_returns_ok_without_writing_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)

            with patch.dict(os.environ, {"COLLECTOR_COINGECKO__API__KEY": "demo-key"}, clear=False):
                result = run_sanity(module_dir, client=FakeCoinGeckoClient())

            self.assertEqual(result["status"], "ok")
            self.assertIn("gecko_says", result["ping"])
            self.assertFalse((module_dir / "outputs" / "status.json").exists())

    def test_run_collection_writes_success_artifacts_and_no_secret_leaks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)

            with patch.dict(os.environ, {"COLLECTOR_COINGECKO__API__KEY": "demo-key"}, clear=False):
                result = run_collection(module_dir, client=FakeCoinGeckoClient())

            status_payload = self._read_json(module_dir / "outputs" / "status.json")
            latest_payload = self._read_json(module_dir / "outputs" / "latest.json")
            manifest_payload = self._read_json(module_dir / "outputs" / "manifest.json")
            normalized_payload = self._read_json(module_dir / result["normalized_output"])
            raw_payload = self._read_json(module_dir / result["raw_capture"])
            events_payload = self._read_jsonl(module_dir / "outputs" / "events.jsonl")

            self.assertEqual(result["status"], "healthy")
            self.assertEqual(status_payload["state"], "healthy")
            self.assertEqual(status_payload["freshness_state"], "fresh")
            self.assertEqual(latest_payload["summary"]["quote_currency"], "usd")
            self.assertEqual(latest_payload["record_count"], 2)
            self.assertEqual(manifest_payload["normalized_contract"]["entity_type"], "market_snapshot")
            self.assertEqual(normalized_payload["entity_type"], "market_snapshot")
            self.assertEqual(normalized_payload["quote_currency"], "usd")
            self.assertEqual([record["source"]["provider_asset_id"] for record in normalized_payload["records"]], ["bitcoin", "ethereum"])
            self.assertEqual(raw_payload["request"]["params"]["ids"], ["bitcoin", "ethereum"])
            self.assertEqual([event["event_type"] for event in events_payload], ["run_started", "output_published", "run_succeeded"])

            self._assert_text_not_contains(module_dir, "demo-key")

    def test_missing_secret_writes_failure_artifacts_without_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)

            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(ConfigurationError):
                    run_collection(module_dir, client=FakeCoinGeckoClient())

            status_payload = self._read_json(module_dir / "outputs" / "status.json")
            events_payload = self._read_jsonl(module_dir / "outputs" / "events.jsonl")
            errors_payload = self._read_jsonl(module_dir / "outputs" / "errors.jsonl")

            self.assertEqual(status_payload["state"], "failed")
            self.assertEqual(status_payload["last_error_code"], "configuration_error")
            self.assertFalse((module_dir / "outputs" / "manifest.json").exists())
            self.assertFalse((module_dir / "outputs" / "latest.json").exists())
            self.assertEqual([event["event_type"] for event in events_payload], ["run_started", "run_failed"])
            self.assertEqual(errors_payload[-1]["error_code"], "configuration_error")
            self.assertEqual(errors_payload[-1]["error_class"], "non_recoverable")
            self.assertEqual(self._list_non_gitkeep(module_dir / "outputs" / "raw"), [])
            self.assertEqual(self._list_non_gitkeep(module_dir / "outputs" / "normalized"), [])

    def test_recoverable_http_failure_after_success_sets_degraded_and_preserves_latest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)

            with patch.dict(os.environ, {"COLLECTOR_COINGECKO__API__KEY": "demo-key"}, clear=False):
                success_result = run_collection(module_dir, client=FakeCoinGeckoClient())
                original_latest = self._read_json(module_dir / "outputs" / "latest.json")
                original_manifest = self._read_json(module_dir / "outputs" / "manifest.json")

                recoverable_error = HttpRequestError(
                    message="HTTP request failed",
                    status_code=429,
                    headers={"Retry-After": "60"},
                )
                with self.assertRaises(HttpRequestError):
                    run_collection(module_dir, client=FailingCoinGeckoClient(recoverable_error))

            status_payload = self._read_json(module_dir / "outputs" / "status.json")
            latest_payload = self._read_json(module_dir / "outputs" / "latest.json")
            manifest_payload = self._read_json(module_dir / "outputs" / "manifest.json")
            errors_payload = self._read_jsonl(module_dir / "outputs" / "errors.jsonl")

            self.assertEqual(success_result["status"], "healthy")
            self.assertEqual(status_payload["state"], "degraded")
            self.assertEqual(status_payload["freshness_state"], "fresh")
            self.assertEqual(status_payload["last_error_code"], "http_429")
            self.assertTrue(status_payload["retryable"])
            self.assertIsNotNone(status_payload["retry_after"])
            self.assertEqual(latest_payload, original_latest)
            self.assertEqual(manifest_payload, original_manifest)
            self.assertEqual(errors_payload[-1]["error_code"], "http_429")
            self.assertTrue(errors_payload[-1]["retryable"])
            self.assertEqual(errors_payload[-1]["http_status"], 429)

    def test_auth_http_failure_after_success_sets_failed_and_preserves_latest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)

            with patch.dict(os.environ, {"COLLECTOR_COINGECKO__API__KEY": "demo-key"}, clear=False):
                run_collection(module_dir, client=FakeCoinGeckoClient())
                original_latest = self._read_json(module_dir / "outputs" / "latest.json")
                original_manifest = self._read_json(module_dir / "outputs" / "manifest.json")

                auth_error = HttpRequestError(
                    message="HTTP request failed",
                    status_code=401,
                    headers={},
                )
                with self.assertRaises(HttpRequestError):
                    run_collection(module_dir, client=FailingCoinGeckoClient(auth_error))

            status_payload = self._read_json(module_dir / "outputs" / "status.json")
            latest_payload = self._read_json(module_dir / "outputs" / "latest.json")
            manifest_payload = self._read_json(module_dir / "outputs" / "manifest.json")
            errors_payload = self._read_jsonl(module_dir / "outputs" / "errors.jsonl")

            self.assertEqual(status_payload["state"], "failed")
            self.assertFalse(status_payload["retryable"])
            self.assertEqual(status_payload["last_error_code"], "http_401")
            self.assertEqual(latest_payload, original_latest)
            self.assertEqual(manifest_payload, original_manifest)
            self.assertEqual(errors_payload[-1]["error_class"], "non_recoverable")
            self.assertEqual(errors_payload[-1]["http_status"], 401)

    def test_recoverable_http_failure_after_stale_success_sets_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            self._copy_real_config(module_dir)

            with patch.dict(os.environ, {"COLLECTOR_COINGECKO__API__KEY": "demo-key"}, clear=False):
                run_collection(module_dir, client=FakeCoinGeckoClient())

                status_path = module_dir / "outputs" / "status.json"
                status_payload = self._read_json(status_path)
                status_payload["last_success_at"] = "2000-01-01T00:00:00Z"
                status_payload["generated_at"] = "2000-01-01T00:00:00Z"
                status_payload["last_event_at"] = "2000-01-01T00:00:00Z"
                status_path.write_text(json.dumps(status_payload, indent=2) + "\n", encoding="utf-8")

                transient_error = HttpRequestError(
                    message="HTTP request failed",
                    status_code=503,
                    headers={},
                )
                with self.assertRaises(HttpRequestError):
                    run_collection(module_dir, client=FailingCoinGeckoClient(transient_error))

            updated_status = self._read_json(module_dir / "outputs" / "status.json")
            self.assertEqual(updated_status["state"], "stale")
            self.assertEqual(updated_status["freshness_state"], "stale")
            self.assertTrue(updated_status["retryable"])

    def _copy_real_config(self, module_dir: Path) -> None:
        shutil.copytree(REPO_ROOT / "modules" / "collector_coingecko" / "config", module_dir / "config")

    def _read_json(self, path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def _read_jsonl(self, path: Path) -> list[dict[str, Any]]:
        with path.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]

    def _list_non_gitkeep(self, path: Path) -> list[str]:
        return sorted(entry.name for entry in path.iterdir() if entry.name != ".gitkeep")

    def _assert_text_not_contains(self, module_dir: Path, secret_value: str) -> None:
        for path in module_dir.rglob("*"):
            if not path.is_file():
                continue
            if path.name == ".gitkeep":
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(secret_value, text, f"Unexpected secret value found in {path}")


if __name__ == "__main__":
    unittest.main()
