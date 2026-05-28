import json
import tempfile
from pathlib import Path
from datetime import datetime, timezone

import pytest

from modules.derivatives_collector.app.market_metrics_v1 import (
    MarketMetricsV1, ProviderCoverage, MetricsPayload, Refs,
)
from modules.derivatives_collector.app.market_metrics_writer import (
    enrich_produced_at,
    write_market_metrics_to_data_center,
    write_market_metrics_view,
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


# --- enrich_produced_at tests ---


def test_enrich_produced_at_adds_schema():
    payload = _binance_full()
    result = enrich_produced_at(payload)
    assert result["schema"] == "market_metrics.v1"


def test_enrich_produced_at_adds_timestamp():
    payload = _binance_full()
    before = datetime.now(timezone.utc).isoformat()
    result = enrich_produced_at(payload)
    after = datetime.now(timezone.utc).isoformat()
    assert "produced_at" in result
    assert before <= result["produced_at"] <= after


def test_enrich_produced_at_override():
    payload = _binance_full()
    ts = "2026-05-28T12:00:00Z"
    result = enrich_produced_at(payload, override_timestamp=ts)
    assert result["produced_at"] == ts


def test_enrich_produced_at_accepts_dataclass():
    payload = _binance_full()
    result = enrich_produced_at(payload)
    assert result["symbol"] == "BTCUSDT"
    assert result["metrics"]["open_interest"] == 72145.89


def test_enrich_produced_at_accepts_dict():
    payload = _binance_full().to_dict()
    result = enrich_produced_at(payload)
    assert result["symbol"] == "BTCUSDT"
    assert result["schema"] == "market_metrics.v1"


def test_enrich_produced_at_does_not_mutate_original():
    payload = _binance_full()
    original = payload.to_dict()
    enrich_produced_at(payload)
    assert "schema" not in original
    assert "produced_at" not in original


# --- DC writer validation + manifest tests ---


def test_dc_writer_validates_and_writes_manifest():
    td = Path(tempfile.mkdtemp())
    payload = _binance_full()
    result = write_market_metrics_to_data_center(payload, root=td, update_registry=False)
    assert result is not None
    manifest_path = td / "data/data_center/derivatives/derivatives_collector__binance/manifest.json"
    assert manifest_path.exists()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert data["producer_id"] == "derivatives_collector__binance"
    assert data["schema"] == "market_metrics.v1"
    assert data["status"] == "ok"


def test_dc_writer_validates_latest_json():
    td = Path(tempfile.mkdtemp())
    payload = _binance_full()
    result = write_market_metrics_to_data_center(payload, root=td, update_registry=False)
    latest_path = td / "data/data_center/derivatives/derivatives_collector__binance/latest.json"
    assert latest_path.exists()
    data = json.loads(latest_path.read_text(encoding="utf-8"))
    assert data["schema"] == "market_metrics.v1"
    assert data["produced_at"] is not None
    assert data["symbol"] == "BTCUSDT"


def test_dc_writer_enriches_before_validation():
    td = Path(tempfile.mkdtemp())
    payload_dict = _binance_full().to_dict()
    assert "schema" not in payload_dict
    result = write_market_metrics_to_data_center(payload_dict, root=td, update_registry=False)
    assert result is not None
    latest_path = td / "data/data_center/derivatives/derivatives_collector__binance/latest.json"
    data = json.loads(latest_path.read_text(encoding="utf-8"))
    assert data["schema"] == "market_metrics.v1"


def test_dc_writer_invalid_payload_raises():
    td = Path(tempfile.mkdtemp())
    payload = _binance_full().to_dict()
    del payload["symbol"]
    del payload["metrics"]
    with pytest.raises(ValueError, match="Schema validation failed"):
        write_market_metrics_to_data_center(payload, root=td)


def test_dc_view_writer_validates_and_writes():
    td = Path(tempfile.mkdtemp())
    payload = _binance_full()
    result = write_market_metrics_view(payload, root=td)
    assert result is not None
    view_path = td / "data/data_center/views/market_metrics/latest.json"
    assert view_path.exists()
    data = json.loads(view_path.read_text(encoding="utf-8"))
    assert data["schema"] == "market_metrics.v1"


def test_dc_writer_writes_by_symbol_schema_enriched():
    td = Path(tempfile.mkdtemp())
    payload = _binance_full()
    result = write_market_metrics_to_data_center(payload, root=td, update_registry=False)
    by_symbol_path = td / "data/data_center/derivatives/derivatives_collector__binance/cache/by_symbol/BTCUSDT.json"
    assert by_symbol_path.exists()
    data = json.loads(by_symbol_path.read_text(encoding="utf-8"))
    assert data["schema"] == "market_metrics.v1"
    assert data["produced_at"] is not None
