"""
spcx_event_calibrator.py — calibrate SPCX event weights from historical outcomes.

Reads SPCX CDP events, captures price at T0, tracks outcomes at +1h/+6h/+24h/+48h,
computes reliability scores per event type, and generates calibrated weights.

Monitor-only — no execution, no broker, no order.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_SIGNAL_DIR = _VIEWS_DIR / "signal_event.v1" / "by_symbol" / "SPCX"
_OUT_DIR = _PROJECT_ROOT / "outputs" / "spcx_signal_strength"
_OUTCOMES_PATH = _OUT_DIR / "event_outcomes.jsonl"
_RELIABILITY_PATH = _OUT_DIR / "event_reliability.json"

TRACKING_HOURS = [1, 6, 24, 48]
MIN_SAMPLES = 5  # Minimum events to consider a score reliable


def _load_json(path: Path) -> dict | list | None:
    if not path.exists(): return None
    try: return json.loads(path.read_text(encoding="utf-8"))
    except: return None


def _get_spcx_price() -> float | None:
    """Get latest SPCX price from market_metrics or command_center."""
    # Command center (primary)
    cc = _load_json(_PROJECT_ROOT / "data" / "ipo" / "spacex" / "command_center" / "latest.json")
    if isinstance(cc, dict) and cc.get("price"):
        return float(cc["price"])
    # Vision analysis
    va = _load_json(_VIEWS_DIR / "vision_analysis" / "by_symbol" / "SPCX.P.json")
    if isinstance(va, list) and va:
        va = va[0]
    if isinstance(va, dict):
        sigs = va.get("signals", [])
        nums = [s["value"] for s in sigs if isinstance(s, dict) and isinstance(s.get("value"), (int, float))]
        if nums: return max(nums)
    return None


def _load_events() -> list[dict]:
    """Load SPCX CDP events with timestamps."""
    events = []
    f = _SIGNAL_DIR / "latest.json"
    data = _load_json(f)
    if isinstance(data, list):
        events = data
    elif isinstance(data, dict):
        events = [data]
    # Add global events
    gf = _VIEWS_DIR / "signal_event.v1" / "latest.json"
    gdata = _load_json(gf)
    if isinstance(gdata, list):
        for e in gdata:
            if isinstance(e, dict) and "SPCX" in str(e.get("symbol", "")):
                if not any(ex.get("timestamp") == e.get("timestamp") and ex.get("event") == e.get("event") for ex in events):
                    events.append(e)
    return events


def capture_event_outcomes() -> dict:
    """For each past SPCX event, record price at T0 and store for tracking."""
    now = datetime.now(timezone.utc)
    events = _load_events()
    current_price = _get_spcx_price()
    captured = 0

    # Load existing outcomes
    existing_ids = set()
    if _OUTCOMES_PATH.exists():
        for line in _OUTCOMES_PATH.read_text(encoding="utf-8").splitlines():
            if not line.strip(): continue
            try: d = json.loads(line); existing_ids.add(d.get("event_id", ""))
            except: pass

    _OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(_OUTCOMES_PATH, "a", encoding="utf-8") as fh:
        for evt in events:
            evt_name = evt.get("event", "")
            ts_str = evt.get("timestamp", "") or evt.get("written_at", "")
            event_id = f"{evt_name}_{ts_str[:16]}"
            if event_id in existing_ids:
                continue

            try: ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            except: ts = now

            age_h = (now - ts).total_seconds() / 3600

            outcome = {
                "event_id": event_id,
                "event": evt_name,
                "timestamp": ts.isoformat(),
                "price_at_t0": evt.get("price") or current_price,
                "age_hours": round(age_h, 1),
                "outcomes": {},
            }

            # For past events where we have current price, compute outcomes
            if current_price and outcome["price_at_t0"] and age_h >= 1:
                p0 = float(outcome["price_at_t0"])
                for h in TRACKING_HOURS:
                    if age_h >= h:
                        # Use current price as proxy for final outcome
                        # In production: use historical snapshots
                        outcome["outcomes"][f"{h}h_pct"] = round((current_price - p0) / p0 * 100, 2)

            fh.write(json.dumps(outcome, default=str) + "\n")
            captured += 1

    return {"captured": captured, "total_events": len(events), "as_of": now.isoformat()}


def compute_event_reliability() -> dict:
    """Compute win rate and avg return per event type from historical outcomes."""
    if not _OUTCOMES_PATH.exists():
        return {"error": "No outcome data yet"}

    stats: dict[str, dict] = {}
    for line in _OUTCOMES_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        try: d = json.loads(line)
        except: continue

        evt = d.get("event", "?")
        outcomes = d.get("outcomes", {})
        if evt not in stats:
            stats[evt] = {"count": 0, "wins": 0, "returns": [], "max_return": 0, "min_return": 0}

        s = stats[evt]
        s["count"] += 1
        for h in TRACKING_HOURS:
            pct = outcomes.get(f"{h}h_pct")
            if pct is not None:
                s["returns"].append(pct)
                if pct > 0: s["wins"] += 1
                s["max_return"] = max(s["max_return"], pct)
                s["min_return"] = min(s["min_return"], pct)

    reliability = {}
    for evt, s in stats.items():
        n = s["count"]
        returns = s["returns"]
        avg_ret = round(sum(returns) / len(returns), 2) if returns else 0
        win_rate = round(s["wins"] / len(returns), 2) if returns else 0
        # Reliability score: sample_weight * win_rate * avg_return_factor
        sample_factor = min(1.0, n / MIN_SAMPLES)
        reliability[evt] = {
            "count": n,
            "win_rate": win_rate,
            "avg_return_pct": avg_ret,
            "max_return_pct": s["max_return"],
            "min_return_pct": s["min_return"],
            "sample_sufficient": n >= MIN_SAMPLES,
            "reliability_score": round(sample_factor * win_rate * max(0, 1 + avg_ret / 10), 2),
        }

    # Write reliability report
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "min_samples": MIN_SAMPLES,
        "by_event": dict(sorted(reliability.items(), key=lambda x: -x[1]["reliability_score"])),
        "monitor_only": True,
    }
    _RELIABILITY_PATH.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    return report


def get_calibrated_weights() -> dict:
    """Return calibrated event weights, falling back to defaults if insufficient data."""
    from modules.ipo_tracking.scoring.spcx_signal_strength import EVENT_WEIGHTS

    report = compute_event_reliability()
    by_event = report.get("by_event", {})

    calibrated = dict(EVENT_WEIGHTS)  # Start with defaults
    for evt, data in by_event.items():
        if not data.get("sample_sufficient"):
            continue
        rel = data["reliability_score"]
        # Scale: reliability 0.0-1.0 → weight 0-30
        old_weight = EVENT_WEIGHTS.get(evt, 10)
        direction = 1 if old_weight >= 0 else -1
        new_weight = int(direction * max(3, min(30, abs(old_weight) * rel * 1.3)))
        if evt in calibrated:
            calibrated[evt] = new_weight

    return calibrated


if __name__ == "__main__":
    r = capture_event_outcomes()
    print(f"Captured: {r['captured']} new outcomes, {r['total_events']} total events")
    rel = compute_event_reliability()
    if "error" not in rel:
        for evt, d in rel.get("by_event", {}).items():
            print(f"  {evt:25s} n={d['count']:>3d} wr={d['win_rate']:.0%} avg={d['avg_return_pct']:>+6.1f}% rel={d['reliability_score']:.2f}")
    print(f"\nCalibrated weights: {json.dumps({k: v for k, v in sorted(get_calibrated_weights().items()) if v != __import__('modules.ipo_tracking.scoring.spcx_signal_strength', fromlist=['EVENT_WEIGHTS']).EVENT_WEIGHTS.get(k)}, indent=2)}")
