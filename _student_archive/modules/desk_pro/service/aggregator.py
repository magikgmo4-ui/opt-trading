from __future__ import annotations
from datetime import datetime, timezone
from modules.desk_pro.models import Snapshot, Metric

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def build_snapshot_mock() -> Snapshot:
    ts = now_iso()
    metrics = [
        Metric(source="mock", asset="BTC", metric="price", value=0, unit="USD", window="spot", notes="placeholder"),
        Metric(source="mock", asset="DXY", metric="trend", value="flat", unit="", window="D", notes="placeholder"),
    ]
    return Snapshot(ts_iso=ts, metrics=metrics, meta={"mode": "mock"})
