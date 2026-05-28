import json
import tempfile
from pathlib import Path

import pytest

from modules.data_center.schemas.registry import get_schema, list_schemas
from modules.data_center.validation.schema_validator import validate_blob
from modules.data_center.spot_snapshot_dc_writer import write_spot_snapshot_to_data_center

_VALID_PAYLOAD = {
    "schema": "pair_market_snapshot.v1",
    "contract_version": "v1",
    "schema_version": "v1",
    "module_id": "collector_binance_spot",
    "provider_id": "binance_spot",
    "run_id": "20260528_000000_test",
    "generated_at": "2026-05-28T00:00:00Z",
    "entity_type": "pair_market_snapshot",
    "records": [
        {
            "pair_symbol": "BTCUSDT",
            "base_asset": "BTC",
            "quote_asset": "USDT",
            "trading_status": "TRADING",
            "is_spot_trading_allowed": True,
            "last_price": "67800.00",
            "open_price_24h": "66500.00",
            "high_price_24h": "68200.00",
            "low_price_24h": "66100.00",
            "price_change_percent_24h": "1.95",
            "volume_base_24h": "1500.00000000",
            "volume_quote_24h": "101700000.00000000",
            "trade_count_24h": 250000,
            "window_open_at": "2026-05-27T00:00:00Z",
            "window_close_at": "2026-05-28T00:00:00Z",
            "weighted_avg_price_24h": "67600.00",
            "source": {"provider_symbol": "BTCUSDT"},
        }
    ],
}


def test_pair_market_snapshot_v1_registered():
    names = list_schemas()
    assert "pair_market_snapshot.v1" in names


def test_get_schema_pair_market_snapshot():
    spec = get_schema("pair_market_snapshot.v1")
    assert spec is not None
    assert "contract_version" in spec["required_fields"]
    assert "records" in spec["required_fields"]
    assert spec["field_types"]["records"] == list
    assert spec["field_types"]["entity_type"] == str


def test_validate_valid_pair_market_snapshot():
    valid, errors = validate_blob(_VALID_PAYLOAD)
    assert valid, errors
    assert errors == []


def test_validate_pair_market_snapshot_missing_required():
    payload = dict(_VALID_PAYLOAD)
    del payload["records"]
    valid, errors = validate_blob(payload)
    assert not valid
    assert any("records" in e for e in errors)


def test_validate_pair_market_snapshot_wrong_type():
    payload = dict(_VALID_PAYLOAD, records="not_a_list")
    valid, errors = validate_blob(payload)
    assert not valid
    assert any("records" in e for e in errors)


def test_dc_writer_validates_before_write():
    td = Path(tempfile.mkdtemp())
    result = write_spot_snapshot_to_data_center(_VALID_PAYLOAD, root=td, update_registry=False)
    producer_path = td / "data/data_center/spot/collector_binance_spot/latest.json"
    assert producer_path.exists()
    assert result["producer_latest"] == str(producer_path)


def test_dc_writer_writes_manifest():
    td = Path(tempfile.mkdtemp())
    write_spot_snapshot_to_data_center(_VALID_PAYLOAD, root=td, update_registry=False)
    manifest_path = td / "data/data_center/spot/collector_binance_spot/manifest.json"
    assert manifest_path.exists()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert data["producer_id"] == "collector_binance_spot"
    assert data["schema"] == "pair_market_snapshot.v1"
    assert data["status"] == "ok"
    assert data["extra"]["run_id"] == "20260528_000000_test"


def test_dc_writer_writes_view():
    td = Path(tempfile.mkdtemp())
    write_spot_snapshot_to_data_center(_VALID_PAYLOAD, root=td, update_registry=False)
    view_path = td / "data/data_center/views/pair_market_snapshot/latest.json"
    assert view_path.exists()


def test_dc_writer_updates_runtime_registry():
    td = Path(tempfile.mkdtemp())
    write_spot_snapshot_to_data_center(_VALID_PAYLOAD, root=td, update_registry=True)
    registry_path = td / "data/data_center/_registry/producers.json"
    assert registry_path.exists()
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    producers = data.get("producers", {})
    assert "collector_binance_spot" in producers
    assert producers["collector_binance_spot"]["contract_class"] == "pair_market_snapshot.v1"


def test_dc_writer_invalid_payload_raises():
    td = Path(tempfile.mkdtemp())
    bad_payload = dict(_VALID_PAYLOAD, contract_version=None)
    with pytest.raises(ValueError, match="Schema validation failed"):
        write_spot_snapshot_to_data_center(bad_payload, root=td)


def test_dc_writer_wrong_entity_type_raises():
    td = Path(tempfile.mkdtemp())
    bad_payload = dict(_VALID_PAYLOAD, schema="pair_market_snapshot.v1", entity_type="other")
    with pytest.raises(ValueError, match="entity_type must be"):
        write_spot_snapshot_to_data_center(bad_payload, root=td, update_registry=False)
