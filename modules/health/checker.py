#!/usr/bin/env python3
"""
Health check local pour le flux webhook/perf/router/risk config.
Lecture seule, pas de réseau.
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = ROOT / "state"


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def check_router_state() -> Dict[str, Any]:
    path = STATE_DIR / "router_state.json"
    if not path.exists():
        return {"ok": False, "check": "router_state", "error": "file missing"}
    try:
        data = _read_json(path)
    except Exception as e:
        return {"ok": False, "check": "router_state", "error": f"invalid JSON: {e}"}
    active = data.get("active_engine")
    if not active:
        return {"ok": False, "check": "router_state", "error": "active_engine empty"}
    return {"ok": True, "check": "router_state", "active_engine": active}


def check_engine_registered(active_engine: str) -> Dict[str, Any]:
    sys.path.insert(0, str(ROOT))
    try:
        from modules.engines.registry import get_engine
    except Exception as e:
        return {"ok": False, "check": "engine_registry", "error": f"import failed: {e}"}
    handler = get_engine(active_engine)
    if handler is None:
        return {"ok": False, "check": "engine_registry", "error": f"'{active_engine}' not registered"}
    return {"ok": True, "check": "engine_registry", "engine": active_engine}


def check_risk_config() -> Dict[str, Any]:
    path = STATE_DIR / "risk_config.json"
    if not path.exists():
        return {"ok": False, "check": "risk_config", "error": "file missing"}
    try:
        data = _read_json(path)
    except Exception as e:
        return {"ok": False, "check": "risk_config", "error": f"invalid JSON: {e}"}
    return {"ok": True, "check": "risk_config", "accounts": list(data.get("accounts", {}).keys())}


def check_all() -> List[Dict[str, Any]]:
    results = []

    # 1. router_state
    r1 = check_router_state()
    results.append(r1)

    # 2. engine registry (only if router_state is ok)
    if r1["ok"]:
        r2 = check_engine_registered(r1["active_engine"])
        results.append(r2)
    else:
        results.append({"ok": False, "check": "engine_registry", "error": "skipped (router_state failed)"})

    # 3. risk_config
    r3 = check_risk_config()
    results.append(r3)

    return results


def main():
    results = check_all()
    all_ok = all(r["ok"] for r in results)

    for r in results:
        status = "OK" if r["ok"] else "FAIL"
        detail = r.get("error", r.get("engine", r.get("active_engine", r.get("accounts", ""))))
        print(f"  [{status}] {r['check']}: {detail}")

    print(f"\nOverall: {'PASS' if all_ok else 'FAIL'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
