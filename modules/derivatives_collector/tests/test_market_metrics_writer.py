import sys
import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.derivatives_collector.app.market_metrics_v1 import (
    MarketMetricsV1,
    ProviderCoverage,
    MetricsPayload,
    Refs,
)
from modules.derivatives_collector.app.market_metrics_writer import (
    write_market_metrics_latest,
    write_market_metrics_by_symbol,
    publish_market_metrics_for_deskpro,
    write_market_metrics_to_data_center,
    write_market_metrics_view,
    publish_market_metrics,
)

_REFS = Refs(
    primary_output="data/collectors/derivatives/derivatives_20260523_000000.json",
    meta_output="data/collectors/derivatives/derivatives_20260523_000000.meta.json",
    latest="data/collectors/derivatives/latest.json",
    status="data/collectors/derivatives/status.json",
)


def _binance_full() -> MarketMetricsV1:
    return MarketMetricsV1(
        contract_version="v1",
        input_class="market_metrics.v1",
        module_id="derivatives_collector",
        provider_id="binance_derivatives",
        symbol="BTCUSDT",
        metrics_ts="2026-05-23T00:00:00Z",
        freshness_state="fresh",
        provider_coverage=ProviderCoverage(
            status="full",
            collectable_metrics=[
                "open_interest", "funding_rate", "volume_futures",
                "long_short_ratio", "liquidations_long", "liquidations_short",
            ],
            missing_metrics=[],
        ),
        metrics=MetricsPayload(
            open_interest=72145.89,
            funding_rate=0.000125,
            volume_futures=4890123456.78,
            long_short_ratio=1.8234,
            liquidations_long=987654.32,
            liquidations_short=123456.78,
        ),
        refs=_REFS,
        warnings=[],
    )


def _bitget_full() -> MarketMetricsV1:
    return MarketMetricsV1(
        contract_version="v1",
        input_class="market_metrics.v1",
        module_id="derivatives_collector",
        provider_id="bitget",
        symbol="BTCUSDT",
        metrics_ts="2026-05-23T00:00:00Z",
        freshness_state="fresh",
        provider_coverage=ProviderCoverage(
            status="full",
            collectable_metrics=[
                "open_interest", "funding_rate", "volume_futures",
                "long_short_ratio", "liquidations_long", "liquidations_short",
            ],
            missing_metrics=[],
        ),
        metrics=MetricsPayload(
            open_interest=18234.56,
            funding_rate=0.0001,
            volume_futures=67890123.45,
            long_short_ratio=1.42,
            liquidations_long=234567.89,
            liquidations_short=98765.43,
        ),
        refs=_REFS,
        warnings=[],
    )


def _bitget_partial() -> MarketMetricsV1:
    return MarketMetricsV1(
        contract_version="v1",
        input_class="market_metrics.v1",
        module_id="derivatives_collector",
        provider_id="bitget",
        symbol="ETHUSDT",
        metrics_ts="2026-05-23T00:00:00Z",
        freshness_state="fresh",
        provider_coverage=ProviderCoverage(
            status="partial",
            collectable_metrics=["open_interest", "funding_rate", "volume_futures"],
            missing_metrics=["long_short_ratio", "liquidations_long", "liquidations_short"],
        ),
        metrics=MetricsPayload(
            open_interest=18234.56,
            funding_rate=0.0001,
            volume_futures=67890123.45,
        ),
        refs=_REFS,
        warnings=["provider missing metrics are explicit and not synthesized"],
    )


def _coinglass_not_proven() -> MarketMetricsV1:
    return MarketMetricsV1(
        contract_version="v1",
        input_class="market_metrics.v1",
        module_id="derivatives_collector",
        provider_id="coinglass",
        symbol="BTCUSDT",
        metrics_ts="2026-05-23T00:00:00Z",
        freshness_state="unknown",
        provider_coverage=ProviderCoverage(
            status="not_proven_runtime_adapter",
            collectable_metrics=[],
            missing_metrics=[
                "open_interest", "funding_rate", "volume_futures",
                "long_short_ratio", "liquidations_long", "liquidations_short",
            ],
        ),
        metrics=MetricsPayload(),
        refs=_REFS,
        warnings=[],
    )


class TestWriteMarketMetricsLatest(unittest.TestCase):
    def test_writes_latest_json(self, tmp_path=None):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp()) if tmp_path is None else tmp_path
        try:
            result = write_market_metrics_latest(_binance_full(), root=td)
            expected = td / "data/collectors/derivatives/latest.json"
            self.assertEqual(result, expected)
            self.assertTrue(expected.exists(), "latest.json should exist")
        finally:
            if tmp_path is None:
                shutil.rmtree(td)

    def test_creates_missing_directories(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            target_dir = td / "data/collectors/derivatives"
            self.assertFalse(target_dir.exists())
            write_market_metrics_latest(_binance_full(), root=td)
            self.assertTrue(target_dir.exists())
        finally:
            shutil.rmtree(td)

    def test_written_content_is_valid_json(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            dest = write_market_metrics_latest(_binance_full(), root=td)
            data = json.loads(dest.read_text(encoding="utf-8"))
            self.assertEqual(data["input_class"], "market_metrics.v1")
            self.assertEqual(data["symbol"], "BTCUSDT")
        finally:
            shutil.rmtree(td)

    def test_refuses_wrong_input_class(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            bad = {"input_class": "something_else", "symbol": "BTCUSDT"}
            with self.assertRaises(ValueError) as ctx:
                write_market_metrics_latest(bad, root=td)
            self.assertIn("input_class", str(ctx.exception))
        finally:
            shutil.rmtree(td)

    def test_refuses_missing_input_class_key(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            with self.assertRaises(ValueError):
                write_market_metrics_latest({}, root=td)
        finally:
            shutil.rmtree(td)

    def test_not_proven_runtime_adapter_skipped(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_latest(_coinglass_not_proven(), root=td)
            self.assertIsNone(result)
            dest = td / "data/collectors/derivatives/latest.json"
            self.assertFalse(dest.exists(), "no file should be written for not_proven_runtime_adapter")
        finally:
            shutil.rmtree(td)

    def test_preserves_null_metrics(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            dest = write_market_metrics_latest(_bitget_partial(), root=td)
            data = json.loads(dest.read_text(encoding="utf-8"))
            self.assertIsNone(data["metrics"]["long_short_ratio"])
            self.assertIsNone(data["metrics"]["liquidations_long"])
            self.assertIsNone(data["metrics"]["liquidations_short"])
        finally:
            shutil.rmtree(td)

    def test_accepts_dataclass_payload(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            payload = _binance_full()
            result = write_market_metrics_latest(payload, root=td)
            self.assertIsNotNone(result)
        finally:
            shutil.rmtree(td)

    def test_accepts_dict_payload(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            payload = _binance_full().to_dict()
            result = write_market_metrics_latest(payload, root=td)
            self.assertIsNotNone(result)
        finally:
            shutil.rmtree(td)


class TestWriteMarketMetricsBySymbol(unittest.TestCase):
    def test_writes_by_symbol_file(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_by_symbol(_binance_full(), root=td)
            expected = td / "data/collectors/derivatives/cache/by_symbol/BTCUSDT.json"
            self.assertEqual(result, expected)
            self.assertTrue(expected.exists())
        finally:
            shutil.rmtree(td)

    def test_symbol_used_as_filename(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_by_symbol(_bitget_partial(), root=td)
            self.assertIn("ETHUSDT.json", str(result))
        finally:
            shutil.rmtree(td)

    def test_creates_missing_cache_directories(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            cache_dir = td / "data/collectors/derivatives/cache/by_symbol"
            self.assertFalse(cache_dir.exists())
            write_market_metrics_by_symbol(_binance_full(), root=td)
            self.assertTrue(cache_dir.exists())
        finally:
            shutil.rmtree(td)

    def test_not_proven_runtime_adapter_skipped(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_by_symbol(_coinglass_not_proven(), root=td)
            self.assertIsNone(result)
            cache_dir = td / "data/collectors/derivatives/cache/by_symbol"
            self.assertFalse(cache_dir.exists())
        finally:
            shutil.rmtree(td)

    def test_refuses_wrong_input_class(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            with self.assertRaises(ValueError):
                write_market_metrics_by_symbol({"input_class": "bad"}, root=td)
        finally:
            shutil.rmtree(td)

    def test_preserves_null_metrics(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            dest = write_market_metrics_by_symbol(_bitget_partial(), root=td)
            data = json.loads(dest.read_text(encoding="utf-8"))
            self.assertIsNone(data["metrics"]["long_short_ratio"])
        finally:
            shutil.rmtree(td)

    def test_written_content_roundtrips_input_class(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            dest = write_market_metrics_by_symbol(_binance_full(), root=td)
            data = json.loads(dest.read_text(encoding="utf-8"))
            self.assertEqual(data["input_class"], "market_metrics.v1")
        finally:
            shutil.rmtree(td)


class TestPublishMarketMetricsForDeskpro(unittest.TestCase):
    def test_writes_deskpro_latest(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics_for_deskpro(_binance_full(), root=td)
            self.assertIsNotNone(result)
            self.assertTrue(result["latest"].exists())
        finally:
            shutil.rmtree(td)

    def test_writes_deskpro_by_symbol(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics_for_deskpro(_binance_full(), root=td)
            self.assertTrue(result["by_symbol"].exists())
            self.assertIn("BTCUSDT.json", str(result["by_symbol"]))
        finally:
            shutil.rmtree(td)

    def test_creates_missing_deskpro_directories(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            deskpro_dir = td / "data/deskpro/inputs/market_metrics"
            self.assertFalse(deskpro_dir.exists())
            publish_market_metrics_for_deskpro(_binance_full(), root=td)
            self.assertTrue(deskpro_dir.exists())
        finally:
            shutil.rmtree(td)

    def test_not_proven_runtime_adapter_skipped(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics_for_deskpro(_coinglass_not_proven(), root=td)
            self.assertIsNone(result)
            deskpro_latest = td / "data/deskpro/inputs/market_metrics/latest.json"
            self.assertFalse(deskpro_latest.exists())
        finally:
            shutil.rmtree(td)

    def test_refuses_wrong_input_class(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            with self.assertRaises(ValueError):
                publish_market_metrics_for_deskpro({"input_class": "wrong"}, root=td)
        finally:
            shutil.rmtree(td)

    def test_deskpro_reader_can_reread_published_latest(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics_for_deskpro(_binance_full(), root=td)
            from modules.desk_pro.service.market_metrics_reader import read_market_metrics
            metrics = read_market_metrics(path=result["latest"])
            self.assertGreater(len(metrics), 0)
            names = {m.metric for m in metrics}
            self.assertIn("open_interest", names)
            self.assertIn("funding_rate", names)
        finally:
            shutil.rmtree(td)

    def test_latest_and_by_symbol_content_match(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics_for_deskpro(_binance_full(), root=td)
            latest_data = json.loads(result["latest"].read_text(encoding="utf-8"))
            by_symbol_data = json.loads(result["by_symbol"].read_text(encoding="utf-8"))
            self.assertEqual(latest_data["symbol"], by_symbol_data["symbol"])
            self.assertEqual(latest_data["metrics"], by_symbol_data["metrics"])
        finally:
            shutil.rmtree(td)

    def test_preserves_null_metrics_in_deskpro_output(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics_for_deskpro(_bitget_partial(), root=td)
            data = json.loads(result["latest"].read_text(encoding="utf-8"))
            self.assertIsNone(data["metrics"]["long_short_ratio"])
            self.assertIsNone(data["metrics"]["liquidations_long"])
        finally:
            shutil.rmtree(td)

    def test_deskpro_reader_returns_empty_for_not_proven(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            # Write a dummy coinglass-like file manually to check reader behaviour
            coinglass_dict = _coinglass_not_proven().to_dict()
            dest = td / "latest.json"
            dest.write_text(json.dumps(coinglass_dict), encoding="utf-8")
            from modules.desk_pro.service.market_metrics_reader import read_market_metrics
            metrics = read_market_metrics(path=dest)
            self.assertEqual(metrics, [])
        finally:
            shutil.rmtree(td)


class TestWriteToDataCenter(unittest.TestCase):
    def test_writes_dc_latest_for_binance(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_to_data_center(_binance_full(), root=td)
            expected = td / "data/data_center/derivatives/derivatives_collector__binance/latest.json"
            self.assertEqual(result["latest"], expected)
            self.assertTrue(expected.exists())
        finally:
            shutil.rmtree(td)

    def test_writes_dc_by_symbol_for_binance(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_to_data_center(_binance_full(), root=td)
            expected = td / "data/data_center/derivatives/derivatives_collector__binance/cache/by_symbol/BTCUSDT.json"
            self.assertEqual(result["by_symbol"], expected)
            self.assertTrue(expected.exists())
        finally:
            shutil.rmtree(td)

    def test_writes_dc_latest_for_bitget(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_to_data_center(_bitget_full(), root=td)
            expected = td / "data/data_center/derivatives/derivatives_collector__bitget/latest.json"
            self.assertEqual(result["latest"], expected)
            self.assertTrue(expected.exists())
        finally:
            shutil.rmtree(td)

    def test_writes_dc_by_symbol_for_bitget(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_to_data_center(_bitget_full(), root=td)
            by_sym = result["by_symbol"]
            self.assertIn("derivatives_collector__bitget", str(by_sym))
            self.assertTrue(by_sym.exists())
        finally:
            shutil.rmtree(td)

    def test_not_proven_returns_none(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_to_data_center(_coinglass_not_proven(), root=td)
            self.assertIsNone(result)
        finally:
            shutil.rmtree(td)

    def test_unknown_provider_returns_none(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            unknown = _binance_full().to_dict()
            unknown["provider_id"] = "unknown_exchange"
            result = write_market_metrics_to_data_center(unknown, root=td)
            self.assertIsNone(result)
        finally:
            shutil.rmtree(td)

    def test_dc_dir_created_automatically(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            write_market_metrics_to_data_center(_binance_full(), root=td)
            dc_dir = td / "data/data_center/derivatives/derivatives_collector__binance"
            self.assertTrue(dc_dir.is_dir())
        finally:
            shutil.rmtree(td)

    def test_dc_content_is_valid_market_metrics_v1(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_to_data_center(_bitget_full(), root=td)
            data = json.loads(result["latest"].read_text(encoding="utf-8"))
            self.assertEqual(data["input_class"], "market_metrics.v1")
            self.assertEqual(data["provider_coverage"]["status"], "full")
            self.assertEqual(len(data["provider_coverage"]["missing_metrics"]), 0)
        finally:
            shutil.rmtree(td)

    def test_dc_producer_path_differs_from_legacy_path(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            dc_result = write_market_metrics_to_data_center(_binance_full(), root=td)
            legacy_result = write_market_metrics_latest(_binance_full(), root=td)
            self.assertNotEqual(str(dc_result["latest"]), str(legacy_result))
        finally:
            shutil.rmtree(td)


class TestPublishMarketMetrics(unittest.TestCase):
    def test_publish_writes_data_center(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics(_binance_full(), root=td)
            self.assertIsNotNone(result["data_center"])
            self.assertTrue(result["data_center"]["latest"].exists())
        finally:
            shutil.rmtree(td)

    def test_publish_writes_legacy_by_default(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics(_binance_full(), root=td)
            self.assertIsNotNone(result["legacy"])
            self.assertTrue(result["legacy"]["latest"].exists())
        finally:
            shutil.rmtree(td)

    def test_publish_writes_deskpro_by_default(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics(_binance_full(), root=td)
            self.assertIsNotNone(result["deskpro"])
            self.assertTrue(result["deskpro"]["latest"].exists())
        finally:
            shutil.rmtree(td)

    def test_publish_legacy_disabled(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics(_binance_full(), root=td, include_legacy_mirror=False)
            self.assertIsNone(result["legacy"])
            legacy_path = td / "data/collectors/derivatives/latest.json"
            self.assertFalse(legacy_path.exists())
        finally:
            shutil.rmtree(td)

    def test_publish_deskpro_disabled(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics(_binance_full(), root=td, include_deskpro_view=False)
            self.assertIsNone(result["deskpro"])
            deskpro_path = td / "data/deskpro/inputs/market_metrics/latest.json"
            self.assertFalse(deskpro_path.exists())
        finally:
            shutil.rmtree(td)

    def test_publish_not_proven_returns_none(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics(_coinglass_not_proven(), root=td)
            self.assertIsNone(result)
        finally:
            shutil.rmtree(td)

    def test_deskpro_reader_can_read_after_full_publish(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics(_bitget_full(), root=td)
            from modules.desk_pro.service.market_metrics_reader import read_market_metrics
            metrics = read_market_metrics(path=result["deskpro"]["latest"])
            self.assertGreater(len(metrics), 0)
            names = {m.metric for m in metrics}
            self.assertIn("long_short_ratio", names)
            self.assertIn("liquidations_long", names)
        finally:
            shutil.rmtree(td)

    def test_publish_dc_path_differs_per_provider(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            r_binance = publish_market_metrics(_binance_full(), root=td)
            r_bitget = publish_market_metrics(_bitget_full(), root=td)
            self.assertNotEqual(
                str(r_binance["data_center"]["latest"]),
                str(r_bitget["data_center"]["latest"]),
            )
        finally:
            shutil.rmtree(td)


class TestWriteContractClassView(unittest.TestCase):
    def test_view_writes_latest(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_view(_binance_full(), root=td)
            expected = td / "data/data_center/views/market_metrics/latest.json"
            self.assertEqual(result["latest"], expected)
            self.assertTrue(expected.exists())
        finally:
            shutil.rmtree(td)

    def test_view_writes_by_symbol(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_view(_binance_full(), root=td)
            expected = td / "data/data_center/views/market_metrics/by_symbol/BTCUSDT.json"
            self.assertEqual(result["by_symbol"], expected)
            self.assertTrue(expected.exists())
        finally:
            shutil.rmtree(td)

    def test_view_path_decoupled_from_producer_id(self):
        """Both binance and bitget write to the same view latest path — consumer is decoupled."""
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            r_binance = write_market_metrics_view(_binance_full(), root=td)
            r_bitget = write_market_metrics_view(_bitget_full(), root=td)
            self.assertEqual(r_binance["latest"], r_bitget["latest"])
            view_path = str(r_binance["latest"])
            self.assertNotIn("bitget", view_path)
            self.assertNotIn("binance", view_path)
        finally:
            shutil.rmtree(td)

    def test_view_by_symbol_decoupled_from_producer_id(self):
        """Both binance and bitget by_symbol write to the same view path — no producer_id."""
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            r_binance = write_market_metrics_view(_binance_full(), root=td)
            r_bitget = write_market_metrics_view(_bitget_full(), root=td)
            # same symbol (BTCUSDT) → same view by_symbol path
            self.assertEqual(r_binance["by_symbol"], r_bitget["by_symbol"])
            path_str = str(r_binance["by_symbol"])
            self.assertNotIn("bitget", path_str)
            self.assertNotIn("binance", path_str)
            self.assertIn("views/market_metrics/by_symbol", path_str)
        finally:
            shutil.rmtree(td)

    def test_view_not_proven_returns_none(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_view(_coinglass_not_proven(), root=td)
            self.assertIsNone(result)
            view_path = td / "data/data_center/views/market_metrics/latest.json"
            self.assertFalse(view_path.exists())
        finally:
            shutil.rmtree(td)

    def test_view_content_is_valid_market_metrics_v1(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = write_market_metrics_view(_bitget_full(), root=td)
            data = json.loads(result["latest"].read_text(encoding="utf-8"))
            self.assertEqual(data["input_class"], "market_metrics.v1")
            self.assertEqual(data["provider_coverage"]["status"], "full")
            self.assertEqual(len(data["provider_coverage"]["missing_metrics"]), 0)
        finally:
            shutil.rmtree(td)

    def test_view_path_differs_from_producer_dc_path(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            view = write_market_metrics_view(_binance_full(), root=td)
            dc = write_market_metrics_to_data_center(_binance_full(), root=td)
            self.assertNotEqual(view["latest"], dc["latest"])
            self.assertIn("views/market_metrics", str(view["latest"]))
            self.assertIn("derivatives/derivatives_collector__binance", str(dc["latest"]))
        finally:
            shutil.rmtree(td)


class TestPublishMarketMetricsView(unittest.TestCase):
    def test_publish_writes_contract_view_by_default(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics(_binance_full(), root=td)
            self.assertIsNotNone(result["view"])
            self.assertTrue(result["view"]["latest"].exists())
            self.assertIn("views/market_metrics", str(result["view"]["latest"]))
        finally:
            shutil.rmtree(td)

    def test_publish_contract_view_disabled(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics(_binance_full(), root=td, include_contract_view=False)
            self.assertIsNone(result["view"])
            view_path = td / "data/data_center/views/market_metrics/latest.json"
            self.assertFalse(view_path.exists())
        finally:
            shutil.rmtree(td)

    def test_publish_view_same_path_for_any_provider(self):
        """publish_market_metrics from different providers feeds the same view."""
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            r_binance = publish_market_metrics(_binance_full(), root=td)
            r_bitget = publish_market_metrics(_bitget_full(), root=td)
            self.assertEqual(r_binance["view"]["latest"], r_bitget["view"]["latest"])
        finally:
            shutil.rmtree(td)

    def test_publish_result_has_all_keys(self):
        import tempfile, shutil
        td = Path(tempfile.mkdtemp())
        try:
            result = publish_market_metrics(_binance_full(), root=td)
            self.assertIn("data_center", result)
            self.assertIn("view", result)
            self.assertIn("legacy", result)
            self.assertIn("deskpro", result)
        finally:
            shutil.rmtree(td)


if __name__ == "__main__":
    unittest.main()
