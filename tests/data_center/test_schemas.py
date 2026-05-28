from modules.data_center.schemas.registry import (
    get_schema,
    list_schemas,
    register_schema,
)


def test_list_schemas_returns_all():
    names = list_schemas()
    assert "market_metrics.v1" in names
    assert "oi.v1" in names
    assert "funding.v1" in names
    assert "liquidations.v1" in names
    assert "long_short.v1" in names
    assert "signal.v1" in names
    assert "event.v1" in names


def test_get_schema_known():
    spec = get_schema("market_metrics.v1")
    assert spec is not None
    assert "schema" in spec["required_fields"]


def test_get_schema_unknown():
    assert get_schema("nonexistent.v1") is None


def test_register_custom_schema():
    register_schema("test.v1", {"required_fields": ["x"]})
    spec = get_schema("test.v1")
    assert spec["required_fields"] == ["x"]


def test_schema_registry_idempotent():
    names_before = set(list_schemas())
    register_schema("dupe.v1", {"required_fields": ["a"]})
    register_schema("dupe.v1", {"required_fields": ["b"]})
    assert get_schema("dupe.v1")["required_fields"] == ["b"]


def test_market_metrics_required_fields():
    spec = get_schema("market_metrics.v1")
    assert "metrics_ts" in spec["required_fields"]
    assert "metrics" in spec["required_fields"]
    assert "produced_at" in spec["required_fields"]


def test_signal_v1_required_fields():
    spec = get_schema("signal.v1")
    assert "direction" in spec["required_fields"]
    assert "price" in spec["required_fields"]


def test_event_v1_optional_fields():
    spec = get_schema("event.v1")
    assert "symbol" in spec["optional_fields"]
    assert "pnl" in spec["optional_fields"]
