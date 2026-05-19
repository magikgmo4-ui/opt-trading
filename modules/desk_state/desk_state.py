#!/usr/bin/env python3
import os, json, socket
from datetime import datetime
from typing import Any, Dict, Optional

def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")

def read_json(path: str) -> Optional[Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

def append_jsonl(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def parse_iso(ts: str) -> Optional[datetime]:
    try:
        if ts.endswith("Z"):
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return datetime.fromisoformat(ts)
    except Exception:
        return None

def build_state(cfg: Dict[str, str]) -> Dict[str, Any]:
    host = socket.gethostname()
    now = datetime.now().astimezone()
    now_s = now_iso()

    snapshot_index = read_json(cfg["SNAPSHOT_INDEX"]) or {}
    tv_inputs = read_json(cfg["TV_INPUTS"]) or {}
    cg_inputs = read_json(cfg["COINGLASS_INPUTS"]) or {}

    tf = cfg["TIMEFRAME"]
    symbols = [s for s in cfg["SYMBOLS"].split() if s.strip()]
    try:
        stale_min = int(cfg["STALE_MIN"])
    except Exception:
        stale_min = 45

    # add any extra symbols present
    if isinstance(snapshot_index, dict):
        for s in snapshot_index.keys():
            if s not in symbols:
                symbols.append(s)

    snapshots_out = {}
    for s in symbols:
        snap = snapshot_index.get(s) if isinstance(snapshot_index, dict) else None
        if not isinstance(snap, dict):
            snapshots_out[s] = None
            continue

        st = snap.get("snapshot_ts") or snap.get("snapshot_ts_iso") or snap.get("ts")
        dt = parse_iso(st) if isinstance(st, str) else None
        age_min = None
        stale = None
        if dt is not None:
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=now.tzinfo)
            age_min = int((now - dt).total_seconds() // 60)
            stale = bool(age_min > stale_min)

        snapshots_out[s] = {
            "symbol": s,
            "tf": snap.get("tf") or tf,
            "snapshot_ts": st,
            "path": snap.get("path"),
            "source": snap.get("source"),
            "host": snap.get("host"),
            "ingested_at": snap.get("ingested_at"),
            "age_min": age_min,
            "stale": stale,
        }

    return {
        "ts": now_s,
        "host": host,
        "timeframe": tf,
        "symbols": symbols,
        "snapshots": snapshots_out,
        "tv_inputs": tv_inputs if isinstance(tv_inputs, dict) else {},
        "coinglass_inputs": cg_inputs if isinstance(cg_inputs, dict) else {},
        "derived": {
            "dxy_trend": None,
            "corr": {"xau_dxy": None, "btc_dxy": None},
            "fear_greed": None,
            "liquidations": None,
        },
        "meta": {
            "schema": "desk_state.v1",
            "stale_min": stale_min,
            "sources": {
                "snapshot_index": cfg["SNAPSHOT_INDEX"],
                "tv_inputs": cfg["TV_INPUTS"],
                "coinglass_inputs": cfg["COINGLASS_INPUTS"],
            },
        },
    }

def main() -> None:
    cfg = {
        "SNAPSHOT_INDEX": os.getenv("SNAPSHOT_INDEX", "/opt/trading/desk/snapshots/latest.json"),
        "TV_INPUTS": os.getenv("TV_INPUTS", "/opt/trading/desk/inputs/tv_inputs_latest.json"),
        "COINGLASS_INPUTS": os.getenv("COINGLASS_INPUTS", "/opt/trading/desk/inputs/coinglass_latest.json"),
        "STATE_LATEST": os.getenv("STATE_LATEST", "/opt/trading/desk/state/latest.json"),
        "STATE_HISTORY": os.getenv("STATE_HISTORY", "/opt/trading/desk/state/history.jsonl"),
        "TIMEFRAME": os.getenv("TIMEFRAME", "H1"),
        "SYMBOLS": os.getenv("SYMBOLS", "BTCUSDT.P XAUUSD SOLUSDT.P ETHUSDT.P"),
        "STALE_MIN": os.getenv("STALE_MIN", "45"),
    }

    state = build_state(cfg)
    write_json(cfg["STATE_LATEST"], state)
    append_jsonl(cfg["STATE_HISTORY"], state)
    print(json.dumps({"ok": True, "latest": cfg["STATE_LATEST"], "history": cfg["STATE_HISTORY"], "ts": state["ts"]}))

if __name__ == "__main__":
    main()
