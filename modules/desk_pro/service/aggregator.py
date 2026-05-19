from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import json
from modules.desk_pro.models import Snapshot, Metric

FIXTURE_PATH = Path(__file__).resolve().parent.parent / "fixtures" / "snapshot_fixture.json"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def build_snapshot(source: str = "fixture") -> Snapshot:
    if source == "fixture":
        snap = _build_snapshot_from_fixture()
        if snap is not None:
            return snap
    return _build_snapshot_mock()

def _build_snapshot_from_fixture() -> Snapshot | None:
    if not FIXTURE_PATH.exists():
        return None
    try:
        raw = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        meta = raw.get("meta", {})
        meta.setdefault("mode", "fixture")
        metrics = [Metric(**m) for m in raw.get("metrics", [])]
        return Snapshot(ts_iso=now_iso(), metrics=metrics, meta=meta)
    except Exception:
        return None

def _build_snapshot_mock() -> Snapshot:
    ts = now_iso()
    metrics = [
        Metric(source="mock", asset="BTC", metric="price", value=0, unit="USD", window="spot", notes="placeholder"),
        Metric(source="mock", asset="DXY", metric="trend", value="flat", unit="", window="D", notes="placeholder"),
    ]
    return Snapshot(ts_iso=ts, metrics=metrics, meta={"mode": "mock"})
