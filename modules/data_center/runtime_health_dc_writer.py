"""
runtime_health_dc_writer.py — route runtime health events to data_center.

Produces:
    runtime_health.v1 — per-service health views
    Writes to: data/data_center/views/runtime_health/latest.json

Usage:
    python -m modules.data_center.runtime_health_dc_writer
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_HEALTH_PATH = _PROJECT_ROOT / "data" / "runtime_health" / "latest.json"


def _atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp") as fh:
        json.dump(payload, fh, indent=2, default=str)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def produce_runtime_health_views() -> dict:
    """Read runtime health data and publish to data_center."""
    now = datetime.now(timezone.utc).isoformat()

    if _HEALTH_PATH.exists():
        try:
            health_data = json.loads(_HEALTH_PATH.read_text(encoding="utf-8"))
        except Exception:
            health_data = {}
    else:
        health_data = {}

    payload = {
        "input_class": "runtime_health.v1",
        "provider_id": "runtime_health",
        "produced_at": now,
        "health": health_data,
        "services_status": {
            "webhook": "active" if _check_port(8000) else "unknown",
            "perf": "active" if _check_port(8010) else "unknown",
            "localcms": "active" if _check_port(8700) else "unknown",
        },
    }
    _atomic_write(_VIEWS_DIR / "runtime_health" / "latest.json", payload)

    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write(
        producer_id="runtime_health",
        contract_class="runtime_health.v1",
        output_path=str(_VIEWS_DIR / "runtime_health" / "latest.json"),
        status="ok",
    )

    return payload


def _check_port(port: int) -> bool:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except Exception:
        return False


if __name__ == "__main__":
    result = produce_runtime_health_views()
    print(f"runtime_health.v1 published. Services:", json.dumps(result.get("services_status", {}), indent=2))
