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
    required_fields=[
        "schema",
        "contract_version",
        "input_class",
        "module_id",
        "provider_id",
        "symbol",
        "metrics_ts",
        "freshness_state",
        "provider_coverage",
        "metrics",
        "refs",
        "produced_at",
    ],
    optional_fields=["warnings"],
    field_types={
        "schema": str,
        "contract_version": str,
        "input_class": str,
        "module_id": str,
        "provider_id": str,
        "symbol": str,
        "metrics_ts": str,
        "freshness_state": str,
        "provider_coverage": dict,
        "metrics": dict,
        "refs": dict,
        "produced_at": str,
        "warnings": list,
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

PAIR_MARKET_SNAPSHOT_V1 = _make_spec(
    required_fields=[
        "schema", "contract_version", "schema_version", "module_id", "provider_id",
        "run_id", "generated_at", "entity_type", "records",
    ],
    field_types={
        "schema": str,
        "contract_version": str,
        "schema_version": str,
        "module_id": str,
        "provider_id": str,
        "run_id": str,
        "generated_at": str,
        "entity_type": str,
        "records": list,
    },
)

register_schema("market_metrics.v1", MARKET_METRICS_V1)
register_schema("oi.v1", OI_V1)
register_schema("funding.v1", FUNDING_V1)
register_schema("liquidations.v1", LIQUIDATIONS_V1)
register_schema("long_short.v1", LONG_SHORT_V1)
register_schema("signal.v1", SIGNAL_V1)
register_schema("event.v1", EVENT_V1)
register_schema("pair_market_snapshot.v1", PAIR_MARKET_SNAPSHOT_V1)
