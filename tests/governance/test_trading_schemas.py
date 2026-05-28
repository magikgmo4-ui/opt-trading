"""Tests for trading JSON schemas — A06 test lock."""
import json
from pathlib import Path

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "docs" / "ot" / "trading" / "schemas"
EVENT_SCHEMA_PATH = SCHEMA_DIR / "trading_event_v1.schema.json"
TRADE_SCHEMA_PATH = SCHEMA_DIR / "trading_trade_v1.schema.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_event_schema_file_exists():
    assert EVENT_SCHEMA_PATH.exists()


def test_trade_schema_file_exists():
    assert TRADE_SCHEMA_PATH.exists()


def test_event_schema_is_valid_json():
    data = _load(EVENT_SCHEMA_PATH)
    assert isinstance(data, dict)


def test_trade_schema_is_valid_json():
    data = _load(TRADE_SCHEMA_PATH)
    assert isinstance(data, dict)


def test_event_schema_is_object_type():
    data = _load(EVENT_SCHEMA_PATH)
    assert data.get("type") == "object"
    assert "properties" in data
    assert "required" in data


def test_trade_schema_is_object_type():
    data = _load(TRADE_SCHEMA_PATH)
    assert data.get("type") == "object"
    assert "properties" in data
    assert "required" in data


def test_event_schema_required_keys():
    required = _load(EVENT_SCHEMA_PATH)["required"]
    for key in ("event_id", "event_ts", "strategy_id", "symbol", "mode"):
        assert key in required, f"Missing required key: {key}"


def test_trade_schema_required_keys():
    required = _load(TRADE_SCHEMA_PATH)["required"]
    for key in ("trade_id", "event_id_origin", "strategy_id", "symbol", "direction"):
        assert key in required, f"Missing required key: {key}"


def test_event_schema_has_meta():
    data = _load(EVENT_SCHEMA_PATH)
    assert "$schema" in data or "title" in data


def test_trade_schema_has_meta():
    data = _load(TRADE_SCHEMA_PATH)
    assert "$schema" in data or "title" in data
