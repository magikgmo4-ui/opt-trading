from modules.data_center.validation.schema_validator import validate_blob, validate_schema


def test_validate_schema_unknown():
    valid, errors = validate_schema({"x": 1}, "nonexistent.v1")
    assert not valid
    assert "unknown schema" in errors[0]


def test_validate_schema_missing_required():
    valid, errors = validate_schema({}, "market_metrics.v1")
    assert not valid
    assert any("schema" in e for e in errors)
    assert any("timestamp" in e for e in errors)


def test_validate_schema_valid():
    blob = {
        "schema": "market_metrics.v1",
        "schema_version": "v1",
        "producer": "test",
        "symbol": "BTCUSDT",
        "timestamp": "2026-05-28T00:00:00Z",
        "data": {"price": 50000},
    }
    valid, errors = validate_schema(blob, "market_metrics.v1")
    assert valid, errors
    assert errors == []


def test_validate_schema_wrong_type():
    blob = {
        "schema": "market_metrics.v1",
        "schema_version": "v1",
        "producer": "test",
        "symbol": "BTCUSDT",
        "timestamp": "2026-05-28T00:00:00Z",
        "data": "not_a_dict",
    }
    valid, errors = validate_schema(blob, "market_metrics.v1")
    assert not valid
    assert any("data" in e for e in errors)


def test_validate_schema_null_field():
    blob = {
        "schema": "market_metrics.v1",
        "schema_version": "v1",
        "producer": "test",
        "symbol": "BTCUSDT",
        "timestamp": "2026-05-28T00:00:00Z",
        "data": None,
    }
    valid, errors = validate_schema(blob, "market_metrics.v1")
    assert not valid
    assert any("data" in e for e in errors)


def test_validate_blob_uses_schema_field():
    blob = {
        "schema": "oi.v1",
        "schema_version": "v1",
        "producer": "test",
        "symbol": "BTCUSDT",
        "timestamp": "2026-05-28T00:00:00Z",
        "data": {"open_interest": 100000},
    }
    valid, errors = validate_blob(blob)
    assert valid, errors


def test_validate_blob_missing_schema_field():
    valid, errors = validate_blob({"x": 1})
    assert not valid
    assert any("schema" in e for e in errors)


def test_validate_signal_v1():
    blob = {
        "schema": "signal.v1",
        "schema_version": "v1",
        "producer": "screener",
        "symbol": "BTCUSDT",
        "timestamp": "2026-05-28T00:00:00Z",
        "direction": "long",
        "price": 50000,
    }
    valid, errors = validate_blob(blob)
    assert valid, errors


def test_validate_signal_missing_direction():
    blob = {
        "schema": "signal.v1",
        "schema_version": "v1",
        "producer": "screener",
        "symbol": "BTCUSDT",
        "timestamp": "2026-05-28T00:00:00Z",
    }
    valid, errors = validate_blob(blob)
    assert not valid
    assert any("direction" in e for e in errors)


def test_validate_event_v1():
    blob = {
        "schema": "event.v1",
        "schema_version": "v1",
        "engine": "perf_engine",
        "event_type": "entry",
        "timestamp": "2026-05-28T00:00:00Z",
        "symbol": "BTCUSDT",
        "side": "long",
        "quantity": 0.5,
        "price": 50000.0,
    }
    valid, errors = validate_blob(blob)
    assert valid, errors
