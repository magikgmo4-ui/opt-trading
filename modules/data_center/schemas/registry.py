_SCHEMA_REGISTRY: dict[str, dict] = {}


def register_schema(name: str, spec: dict) -> None:
    _SCHEMA_REGISTRY[name] = spec


def get_schema(name: str) -> dict | None:
    return _SCHEMA_REGISTRY.get(name)


def list_schemas() -> list[str]:
    return list(_SCHEMA_REGISTRY)


def _make_spec(
    required_fields: list[str],
    optional_fields: list[str] | None = None,
    field_types: dict[str, type] | None = None,
) -> dict:
    return {
        "required_fields": required_fields,
        "optional_fields": optional_fields or [],
        "field_types": field_types or {},
    }


MARKET_METRICS_V1 = _make_spec(
    required_fields=["schema", "schema_version", "producer", "symbol", "timestamp", "data"],
    optional_fields=["coverage"],
    field_types={
        "schema": str,
        "schema_version": str,
        "producer": str,
        "symbol": str,
        "timestamp": str,
        "data": dict,
    },
)

OI_V1 = _make_spec(
    required_fields=["schema", "schema_version", "producer", "symbol", "timestamp", "data"],
    field_types={
        "schema": str,
        "schema_version": str,
        "producer": str,
        "symbol": str,
        "timestamp": str,
        "data": dict,
    },
)

FUNDING_V1 = _make_spec(
    required_fields=["schema", "schema_version", "producer", "symbol", "timestamp", "data"],
    field_types={
        "schema": str,
        "schema_version": str,
        "producer": str,
        "symbol": str,
        "timestamp": str,
        "data": dict,
    },
)

LIQUIDATIONS_V1 = _make_spec(
    required_fields=["schema", "schema_version", "producer", "symbol", "timestamp", "data"],
    field_types={
        "schema": str,
        "schema_version": str,
        "producer": str,
        "symbol": str,
        "timestamp": str,
        "data": dict,
    },
)

LONG_SHORT_V1 = _make_spec(
    required_fields=["schema", "schema_version", "producer", "symbol", "timestamp", "data"],
    field_types={
        "schema": str,
        "schema_version": str,
        "producer": str,
        "symbol": str,
        "timestamp": str,
        "data": dict,
    },
)

SIGNAL_V1 = _make_spec(
    required_fields=["schema", "schema_version", "producer", "symbol", "timestamp", "direction", "price"],
    field_types={
        "schema": str,
        "schema_version": str,
        "producer": str,
        "symbol": str,
        "timestamp": str,
        "direction": str,
        "price": (int, float),
    },
)

EVENT_V1 = _make_spec(
    required_fields=["schema", "schema_version", "engine", "event_type", "timestamp"],
    optional_fields=["symbol", "side", "quantity", "price", "pnl"],
    field_types={
        "schema": str,
        "schema_version": str,
        "engine": str,
        "event_type": str,
        "timestamp": str,
        "symbol": str,
        "side": str,
        "quantity": (int, float),
        "price": (int, float),
        "pnl": (int, float),
    },
)

register_schema("market_metrics.v1", MARKET_METRICS_V1)
register_schema("oi.v1", OI_V1)
register_schema("funding.v1", FUNDING_V1)
register_schema("liquidations.v1", LIQUIDATIONS_V1)
register_schema("long_short.v1", LONG_SHORT_V1)
register_schema("signal.v1", SIGNAL_V1)
register_schema("event.v1", EVENT_V1)
