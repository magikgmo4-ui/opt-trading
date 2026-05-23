import json
from pathlib import Path

import pytest

from modules.desk_pro.service.market_metrics_reader import (
    read_market_metrics,
    _normalize_asset,
    DC_MARKET_METRICS_VIEW,
    MARKET_METRICS_LEGACY,
)

_BITGET_FIXTURE = {
    "contract_version": "v1",
    "input_class": "market_metrics.v1",
    "module_id": "derivatives_collector",
    "provider_id": "bitget",
    "symbol": "BTCUSDT",
    "metrics_ts": "2026-05-23T00:00:00Z",
    "freshness_state": "fresh",
    "provider_coverage": {
        "status": "partial",
        "collectable_metrics": ["open_interest", "funding_rate", "volume_futures"],
        "missing_metrics": ["long_short_ratio", "liquidations_long", "liquidations_short"],
    },
    "metrics": {
        "open_interest": 18234.56,
        "funding_rate": 0.0001,
        "volume_futures": 67890123.45,
        "long_short_ratio": None,
        "liquidations_long": None,
        "liquidations_short": None,
    },
    "refs": {
        "primary_output": "data/derivatives/x.json",
        "meta_output": "data/derivatives/x.meta.json",
        "latest": "data/derivatives/latest.json",
        "status": "data/derivatives/status.json",
    },
    "warnings": ["provider missing metrics are explicit and not synthesized"],
}

_COINGLASS_FIXTURE = {
    "contract_version": "v1",
    "input_class": "market_metrics.v1",
    "module_id": "derivatives_collector",
    "provider_id": "coinglass",
    "symbol": "BTCUSDT",
    "metrics_ts": "2026-05-23T00:00:00Z",
    "freshness_state": "unknown",
    "provider_coverage": {
        "status": "not_proven_runtime_adapter",
        "collectable_metrics": [],
        "missing_metrics": ["open_interest", "funding_rate", "volume_futures",
                            "long_short_ratio", "liquidations_long", "liquidations_short"],
    },
    "metrics": {
        "open_interest": None, "funding_rate": None, "volume_futures": None,
        "long_short_ratio": None, "liquidations_long": None, "liquidations_short": None,
    },
    "refs": {"primary_output": "", "meta_output": "", "latest": "", "status": ""},
    "warnings": [],
}


class TestReadMarketMetricsAbsent:
    def test_missing_file_returns_empty(self, tmp_path):
        result = read_market_metrics(path=tmp_path / "nonexistent.json")
        assert result == []

    def test_returns_list_not_exception(self, tmp_path):
        metrics = read_market_metrics(path=tmp_path / "missing.json")
        assert isinstance(metrics, list)


class TestReadMarketMetricsMalformed:
    def test_malformed_json_returns_empty(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("{not valid json", encoding="utf-8")
        assert read_market_metrics(path=p) == []

    def test_wrong_input_class_returns_empty(self, tmp_path):
        p = tmp_path / "wrong.json"
        payload = {**_BITGET_FIXTURE, "input_class": "something_else"}
        p.write_text(json.dumps(payload), encoding="utf-8")
        assert read_market_metrics(path=p) == []

    def test_empty_json_object_returns_empty(self, tmp_path):
        p = tmp_path / "empty.json"
        p.write_text("{}", encoding="utf-8")
        assert read_market_metrics(path=p) == []


class TestReadMarketMetricsBitgetPartial:
    def test_returns_three_metrics(self, tmp_path):
        p = tmp_path / "latest.json"
        p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")
        result = read_market_metrics(path=p)
        assert len(result) == 3

    def test_metric_fields(self, tmp_path):
        p = tmp_path / "latest.json"
        p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")
        result = read_market_metrics(path=p)
        names = {m.metric for m in result}
        assert names == {"open_interest", "funding_rate", "volume_futures"}

    def test_null_metrics_excluded(self, tmp_path):
        p = tmp_path / "latest.json"
        p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")
        result = read_market_metrics(path=p)
        metric_names = {m.metric for m in result}
        assert "long_short_ratio" not in metric_names
        assert "liquidations_long" not in metric_names

    def test_source_is_provider_id(self, tmp_path):
        p = tmp_path / "latest.json"
        p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")
        result = read_market_metrics(path=p)
        assert all(m.source == "bitget" for m in result)

    def test_asset_normalized(self, tmp_path):
        p = tmp_path / "latest.json"
        p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")
        result = read_market_metrics(path=p)
        assert all(m.asset == "BTC" for m in result)

    def test_fresh_quality_095(self, tmp_path):
        p = tmp_path / "latest.json"
        p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")
        result = read_market_metrics(path=p)
        assert all(m.quality == 0.95 for m in result)

    def test_window_is_futures(self, tmp_path):
        p = tmp_path / "latest.json"
        p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")
        result = read_market_metrics(path=p)
        assert all(m.window == "futures" for m in result)


class TestReadMarketMetricsFreshness:
    def test_stale_quality_050(self, tmp_path):
        p = tmp_path / "latest.json"
        payload = {**_BITGET_FIXTURE, "freshness_state": "stale"}
        p.write_text(json.dumps(payload), encoding="utf-8")
        result = read_market_metrics(path=p)
        assert all(m.quality == 0.5 for m in result)

    def test_unknown_freshness_quality_030(self, tmp_path):
        p = tmp_path / "latest.json"
        payload = {**_BITGET_FIXTURE, "freshness_state": "unknown"}
        p.write_text(json.dumps(payload), encoding="utf-8")
        result = read_market_metrics(path=p)
        assert all(m.quality == 0.3 for m in result)


class TestReadMarketMetricsNotProven:
    def test_not_proven_returns_empty(self, tmp_path):
        p = tmp_path / "latest.json"
        p.write_text(json.dumps(_COINGLASS_FIXTURE), encoding="utf-8")
        result = read_market_metrics(path=p)
        assert result == []


class TestNormalizeAsset:
    def test_btcusdt(self):
        assert _normalize_asset("BTCUSDT") == "BTC"

    def test_btcusd(self):
        assert _normalize_asset("BTCUSD") == "BTC"

    def test_umcbl(self):
        assert _normalize_asset("BTCUSDT_UMCBL") == "BTCUSDT"

    def test_xauusd_strips_usd(self):
        assert _normalize_asset("XAUUSD") == "XAU"

    def test_unknown_passthrough(self):
        assert _normalize_asset("SOMETHING") == "SOMETHING"


class TestDefaultPathHierarchy:
    def test_dc_view_path_has_no_producer_id(self):
        path_str = str(DC_MARKET_METRICS_VIEW)
        assert "data/data_center/views/" in path_str
        assert "bitget" not in path_str
        assert "binance" not in path_str

    def test_reads_dc_view_by_default(self, tmp_path, monkeypatch):
        p = tmp_path / "latest.json"
        p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")
        import modules.desk_pro.service.market_metrics_reader as reader_mod
        monkeypatch.setattr(reader_mod, "DC_MARKET_METRICS_VIEW", p)
        monkeypatch.setattr(reader_mod, "MARKET_METRICS_LEGACY", tmp_path / "absent.json")
        result = read_market_metrics()
        assert len(result) == 3

    def test_fallback_legacy_when_dc_view_absent(self, tmp_path, monkeypatch):
        legacy_p = tmp_path / "legacy.json"
        legacy_p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")
        import modules.desk_pro.service.market_metrics_reader as reader_mod
        monkeypatch.setattr(reader_mod, "DC_MARKET_METRICS_VIEW", tmp_path / "absent_dc.json")
        monkeypatch.setattr(reader_mod, "MARKET_METRICS_LEGACY", legacy_p)
        result = read_market_metrics()
        assert len(result) == 3

    def test_both_absent_returns_empty(self, tmp_path, monkeypatch):
        import modules.desk_pro.service.market_metrics_reader as reader_mod
        monkeypatch.setattr(reader_mod, "DC_MARKET_METRICS_VIEW", tmp_path / "absent_dc.json")
        monkeypatch.setattr(reader_mod, "MARKET_METRICS_LEGACY", tmp_path / "absent_legacy.json")
        result = read_market_metrics()
        assert result == []

    def test_dc_view_invalid_fallback_to_legacy(self, tmp_path, monkeypatch):
        dc_p = tmp_path / "dc.json"
        dc_p.write_text("{not valid json", encoding="utf-8")
        legacy_p = tmp_path / "legacy.json"
        legacy_p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")
        import modules.desk_pro.service.market_metrics_reader as reader_mod
        monkeypatch.setattr(reader_mod, "DC_MARKET_METRICS_VIEW", dc_p)
        monkeypatch.setattr(reader_mod, "MARKET_METRICS_LEGACY", legacy_p)
        result = read_market_metrics()
        assert len(result) == 3

    def test_explicit_path_bypasses_default_resolution(self, tmp_path, monkeypatch):
        explicit_p = tmp_path / "explicit.json"
        explicit_p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")
        import modules.desk_pro.service.market_metrics_reader as reader_mod
        monkeypatch.setattr(reader_mod, "DC_MARKET_METRICS_VIEW", tmp_path / "absent.json")
        monkeypatch.setattr(reader_mod, "MARKET_METRICS_LEGACY", tmp_path / "absent.json")
        result = read_market_metrics(path=explicit_p)
        assert len(result) == 3


class TestAggregatorIntegration:
    def test_build_snapshot_augmented(self, tmp_path, monkeypatch):
        p = tmp_path / "latest.json"
        p.write_text(json.dumps(_BITGET_FIXTURE), encoding="utf-8")

        import modules.desk_pro.service.market_metrics_reader as reader_mod
        monkeypatch.setattr(reader_mod, "DC_MARKET_METRICS_VIEW", p)
        monkeypatch.setattr(reader_mod, "MARKET_METRICS_LEGACY", tmp_path / "absent.json")

        from modules.desk_pro.service.aggregator import build_snapshot
        snap = build_snapshot(source="fixture")
        mm_metrics = [m for m in snap.metrics if m.source == "bitget"]
        assert len(mm_metrics) == 3
        assert snap.meta.get("market_metrics") == "loaded"

    def test_build_snapshot_no_file_clean(self, tmp_path, monkeypatch):
        import modules.desk_pro.service.market_metrics_reader as reader_mod
        monkeypatch.setattr(reader_mod, "DC_MARKET_METRICS_VIEW", tmp_path / "absent.json")
        monkeypatch.setattr(reader_mod, "MARKET_METRICS_LEGACY", tmp_path / "absent_legacy.json")

        from modules.desk_pro.service.aggregator import build_snapshot
        snap = build_snapshot(source="fixture")
        assert snap.meta.get("market_metrics") is None
