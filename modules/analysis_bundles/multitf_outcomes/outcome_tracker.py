"""
outcome_tracker.py — track live outcomes of multi-TF setups.

Reads multitf_setup_score.v1 and market_metrics, tracks open setups,
observes outcomes (hit TP, hit invalidation, MFE/MAE), generates
grade accuracy report.

Produces:
  outputs/multitf_outcomes/open_setups.jsonl
  outputs/multitf_outcomes/outcome_events.jsonl
  outputs/multitf_outcomes/grade_accuracy_report.json

Usage:
    python -m modules.analysis_bundles.multitf_outcomes.outcome_tracker

Invariants:
  - Monitor-only — no execution, no broker, no order
  - Read-only consumer of existing views
  - Observation only — writes to outputs/
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_SCORE_DIR = _VIEWS_DIR / "multitf_setup_score.v1" / "by_symbol"
_MM_DIR = _VIEWS_DIR / "market_metrics" / "by_symbol"
_OUT_DIR = _PROJECT_ROOT / "outputs" / "multitf_outcomes"
_OPEN_PATH = _OUT_DIR / "open_setups.jsonl"
_EVENTS_PATH = _OUT_DIR / "outcome_events.jsonl"
_REPORT_PATH = _OUT_DIR / "grade_accuracy_report.json"


def _load_json(path: Path) -> dict | None:
    if not path.exists(): return None
    try: return json.loads(path.read_text(encoding="utf-8"))
    except: return None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_current_price(symbol: str) -> float | None:
    """Get latest price from market_metrics or vision_analysis."""
    # Market metrics
    mm_map = {"BTC": "BTCUSDT.json", "ETH": "ETHUSDT.json", "SOL": "SOLUSDT.json",
              "XAUUSD": "XAUUSD.json", "SPCX": None}
    fn = mm_map.get(symbol)
    if fn:
        mm = _load_json(_MM_DIR / fn)
        if mm and isinstance(mm, dict):
            p = mm.get("last_price") or mm.get("price")
            if p: return float(p)
    # Vision analysis fallback
    va_map = {"BTC": "BTCUSDT.P", "ETH": "ETHUSDT.P", "SOL": "SOLUSDT.P",
              "XAUUSD": "OANDA:XAUUSD", "SPCX": "SPCX.P"}
    vf = va_map.get(symbol)
    if vf:
        va = _load_json(_VIEWS_DIR / "vision_analysis" / "by_symbol" / f"{vf}.json")
        if va:
            item = va[0] if isinstance(va, list) and va else va
            if isinstance(item, dict):
                sigs = item.get("signals", [])
                nums = [s["value"] for s in sigs if isinstance(s, dict) and isinstance(s.get("value"), (int, float))]
                if nums: return max(nums, key=lambda v: abs(v))
    return None


def track_outcomes() -> dict:
    """Main outcome tracking pipeline."""
    now = _now()
    _OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load previous open setups
    open_setups = _load_open_setups()
    current_ids = set()

    # Scan current setups
    new_count = 0
    resolution_count = 0
    if _SCORE_DIR.exists():
        for sf in sorted(_SCORE_DIR.glob("*.json")):
            d = _load_json(sf)
            if not d or not d.get("setups"): continue
            sym = d.get("symbol", "?")
            st = d["setups"][0]
            sid = st.get("setup_id", f"{sym}_{_now()[:10]}")

            # Resolve existing
            if sid in open_setups:
                prev = open_setups[sid]
                res = _resolve_outcome(prev, sym, st)
                if res:
                    _write_event(res)
                    resolution_count += 1
                    del open_setups[sid]
                    continue

            # New setup
            price_now = _get_current_price(sym)
            entry_zone = st.get("entry_zone", [])
            entry_price = (entry_zone[0] + entry_zone[-1]) / 2 if len(entry_zone) >= 2 else (entry_zone[0] if entry_zone else price_now)
            open_setups[sid] = {
                "setup_id": sid,
                "symbol": sym,
                "setup_type": st.get("setup_type", ""),
                "grade_at_signal": st.get("grade", "C"),
                "score_at_signal": st.get("score", 0),
                "probability_pct": st.get("probability_pct", 0),
                "confidence_pct": st.get("confidence_pct", 0),
                "trigger_strength": st.get("trigger_strength", ""),
                "trigger_quality_score": st.get("trigger_quality_score", 0),
                "lab_edge": _get_lab_edge(sym, st.get("setup_type", "")),
                "price_at_signal": entry_price or price_now,
                "invalidation": st.get("invalidation", 0),
                "target_1": st.get("targets", [None])[0],
                "target_2": st.get("targets", [None, None])[1] if len(st.get("targets", [])) > 1 else None,
                "direction": st.get("direction", "monitor_only"),
                "core_evidence": st.get("core_evidence", [])[:3],
                "downgrade_reasons": st.get("downgrade_reasons", [])[:2],
                "snapshot_at": now,
                "monitor_only": True,
            }
            current_ids.add(sid)
            new_count += 1

    # Keep unresolved setups
    for sid in list(open_setups.keys()):
        if sid not in current_ids:
            # Setup disappeared — mark as stale
            prev = open_setups[sid]
            _write_event({
                "setup_id": sid, "symbol": prev.get("symbol"),
                "outcome": "stale", "reason": "setup removed from scorer",
                "elapsed_minutes": _elapsed(prev.get("snapshot_at", "")),
                "monitor_only": True, "resolved_at": now,
            })
            del open_setups[sid]

    # Write open setups
    with open(_OPEN_PATH, "w", encoding="utf-8") as fh:
        for s in open_setups.values():
            fh.write(json.dumps(s, default=str) + "\n")

    # Generate report
    _write_accuracy_report()

    return {
        "tracked": len(open_setups) + resolution_count,
        "open": len(open_setups),
        "new": new_count,
        "resolved": resolution_count,
        "as_of": now,
    }


def _resolve_outcome(prev: dict, sym: str, st: dict) -> dict | None:
    """Check if setup reached invalidation or target."""
    price = _get_current_price(sym)
    if not price: return None

    inval = prev.get("invalidation", 0)
    tp1 = prev.get("target_1")
    tp2 = prev.get("target_2")
    entry = prev.get("price_at_signal", price)
    direction = prev.get("direction", "monitor_only")
    elapsed = _elapsed(prev.get("snapshot_at", ""))

    mfe_pct = 0
    mae_pct = 0
    if entry and entry > 0:
        if direction in ("short", "monitor_only") and st.get("setup_type", "").endswith("short"):
            mfe_pct = round((entry - price) / entry * 100, 2)
            mae_pct = round((price - entry) / entry * 100, 2) if price > entry else 0
        else:
            mfe_pct = round((price - entry) / entry * 100, 2)
            mae_pct = round((entry - price) / entry * 100, 2) if price < entry else 0

    outcome = "pending"
    reason = ""
    hit_tp1 = False
    hit_inval = False

    if inval and inval > 0:
        if direction == "short":
            hit_inval = price >= inval
        else:
            hit_inval = price <= inval

    if tp1:
        if direction == "short":
            hit_tp1 = price <= tp1
        else:
            hit_tp1 = price >= tp1

    if hit_inval:
        outcome = "failed"
        reason = f"Hit invalidation @ {inval}"
    elif hit_tp1:
        outcome = "confirmed"
        reason = f"Hit TP1 @ {tp1}"
    elif elapsed > 240:
        outcome = "neutral"
        reason = "Timeout — no resolution"

    if outcome == "pending":
        return None

    return {
        "setup_id": prev.get("setup_id"),
        "symbol": sym,
        "setup_type": prev.get("setup_type", ""),
        "grade_at_signal": prev.get("grade_at_signal", "C"),
        "score_at_signal": prev.get("score_at_signal", 0),
        "trigger_strength": prev.get("trigger_strength", ""),
        "direction": direction,
        "price_at_signal": entry,
        "current_price": price,
        "invalidation": inval,
        "target_1": tp1,
        "mfe_pct": mfe_pct,
        "mae_pct": mae_pct,
        "hit_tp1": hit_tp1,
        "hit_invalidation": hit_inval,
        "outcome": outcome,
        "reason": reason,
        "elapsed_minutes": elapsed,
        "resolved_at": _now(),
        "monitor_only": True,
    }


def _write_event(event: dict) -> None:
    with open(_EVENTS_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, default=str) + "\n")


def _load_open_setups() -> dict:
    """Load open setups indexed by setup_id."""
    setups = {}
    if not _OPEN_PATH.exists(): return setups
    for line in _OPEN_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        try:
            d = json.loads(line)
            setups[d.get("setup_id", "")] = d
        except json.JSONDecodeError:
            pass
    return setups


def _elapsed(snapshot_at: str) -> int:
    if not snapshot_at: return 0
    try:
        t = datetime.fromisoformat(snapshot_at.replace("Z", "+00:00"))
        return int((datetime.now(timezone.utc) - t).total_seconds() / 60)
    except: return 0


def _get_lab_edge(sym: str, setup_type: str) -> dict | None:
    lab = _PROJECT_ROOT / "outputs" / "lab_backtest" / "results" / "setup_edge_scores.jsonl"
    if not lab.exists(): return None
    for line in lab.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        try:
            d = json.loads(line)
            if d.get("symbol") == sym and d.get("setup_type") == setup_type:
                return {"recommendation": d.get("recommendation"), "edge_score": d.get("edge_score")}
        except: pass
    return None


def _write_accuracy_report() -> None:
    """Aggregate outcome events by grade and setup_type."""
    if not _EVENTS_PATH.exists(): return

    buckets: dict = {}
    for line in _EVENTS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        try: d = json.loads(line)
        except: continue

        grade = d.get("grade_at_signal", "?")
        stype = d.get("setup_type", "?")
        key = f"{grade}|{stype}"
        if key not in buckets:
            buckets[key] = {"grade": grade, "setup_type": stype, "count": 0,
                            "confirmed": 0, "failed": 0, "neutral": 0, "stale": 0,
                            "mfe_pcts": [], "mae_pcts": []}
        b = buckets[key]
        b["count"] += 1
        out = d.get("outcome", "pending")
        if out in ("confirmed", "failed", "neutral", "stale"):
            b[out] = b.get(out, 0) + 1
        mfe = d.get("mfe_pct")
        mae = d.get("mae_pct")
        if isinstance(mfe, (int, float)): b["mfe_pcts"].append(mfe)
        if isinstance(mae, (int, float)): b["mae_pcts"].append(mae)

    report = []
    for b in buckets.values():
        n = b["count"]
        mfes = b["mfe_pcts"]
        maes = b["mae_pcts"]
        report.append({
            "grade": b["grade"], "setup_type": b["setup_type"],
            "count": n,
            "confirmed_rate": round(b["confirmed"] / n, 2) if n else 0,
            "invalidation_rate": round(b["failed"] / n, 2) if n else 0,
            "avg_mfe_pct": round(sum(mfes) / len(mfes), 2) if mfes else 0,
            "avg_mae_pct": round(sum(maes) / len(maes), 2) if maes else 0,
            "median_mfe_pct": round(sorted(mfes)[len(mfes)//2], 2) if mfes else 0,
            "median_mae_pct": round(sorted(maes)[len(maes)//2], 2) if maes else 0,
        })

    _REPORT_PATH.write_text(json.dumps({
        "generated_at": _now(),
        "total_outcomes": sum(b["count"] for b in buckets.values()),
        "by_grade_setup": sorted(report, key=lambda r: (-r["count"], r["grade"])),
        "monitor_only": True,
    }, indent=2, default=str), encoding="utf-8")


if __name__ == "__main__":
    r = track_outcomes()
    print(f"Tracked: {r['tracked']} | Open: {r['open']} | New: {r['new']} | Resolved: {r['resolved']}")
