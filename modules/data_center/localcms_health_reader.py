from __future__ import annotations

from datetime import datetime, timezone

from modules.data_center.layout import load_consumers_registry, load_producers_registry

_CONSUMER_ID = "localcms__data_center_health"


def _load_producer_runtime() -> list:
    """Return per-producer runtime state from data/data_center/_registry/producers.json.

    Returns empty list if runtime registry does not exist yet (no writes yet).
    """
    try:
        from modules.data_center.runtime_registry import load_runtime_registry
        rt = load_runtime_registry()
        return [
            {
                "producer_id": info.get("producer_id"),
                "last_write": info.get("last_write"),
                "status": info.get("status"),
                "last_output_path": info.get("last_output_path"),
            }
            for info in rt.get("producers", {}).values()
        ]
    except Exception:
        return []


def read_data_center_health() -> dict:
    """Return a status-only summary of the Data Center registry.

    Implements the localcms__data_center_health consumer (access_pattern=status_only).
    Reads static registry (modules/data_center/registry/*.json) and, if available,
    the runtime registry (data/data_center/_registry/producers.json).
    """
    producers_reg = load_producers_registry()
    consumers_reg = load_consumers_registry()

    producers = producers_reg.get("producers", [])
    consumers = consumers_reg.get("consumers", [])

    implemented = [
        c["consumer_id"]
        for c in consumers
        if c.get("implementation_status") == "implemented"
    ]
    not_started = [
        c["consumer_id"]
        for c in consumers
        if c.get("implementation_status") == "not_started"
    ]
    contract_classes = sorted(
        {p["contract_class"] for p in producers if p.get("contract_class")}
    )

    return {
        "ok": True,
        "consumer_id": _CONSUMER_ID,
        "source": "data_center_registry",
        "producer_count": len(producers),
        "consumer_count": len(consumers),
        "implemented_consumers": implemented,
        "not_started_consumers": not_started,
        "contract_classes": contract_classes,
        "producer_runtime": _load_producer_runtime(),
        "warnings": [],
        "read_at": datetime.now(timezone.utc).isoformat(),
    }
