from __future__ import annotations

from datetime import datetime, timezone

from modules.data_center.layout import load_consumers_registry, load_producers_registry

_CONSUMER_ID = "localcms__data_center_health"


def read_data_center_health() -> dict:
    """Return a status-only summary of the Data Center registry.

    Implements the localcms__data_center_health consumer (access_pattern=status_only).
    Reads modules/data_center/registry/producers.json + consumers.json — no data/
    files touched.
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
        "warnings": [],
        "read_at": datetime.now(timezone.utc).isoformat(),
    }
