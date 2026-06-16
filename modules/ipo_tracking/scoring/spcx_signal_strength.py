"""
spcx_signal_strength.py — cumulative SPCX signal strength scorer.  GO_SPCX_SIGNAL_STRENGTH_01

Reads signal_event.v1 CDP events for SPCX, scores each event (bullish + / bearish -),
applies time decay, and aggregates over sliding windows (24h, 3 sessions, 1 week).
Exposes SPCX_SIGNAL_STRENGTH 0→100 with classification.

Monitor-only — no execution, no broker, no order.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_SIGNAL_DIR = _VIEWS_DIR / "signal_event.v1" / "by_symbol" / "SPCX"
_HISTORY_PATH = _PROJECT_ROOT / "outputs" / "spcx_signal_strength" / "strength_history.jsonl"

# ── Event scoring weights (bullish + / bearish -) ──
EVENT_WEIGHTS = {
    # Bullish
    "orb_break_high": 25,
    "vwap_reclaim": 20,
    "breakout_high": 20,
    "volume_spike": 15,
    "volume_on_breakout": 15,
    "relative_volume_gt_2": 12,
    "relative_volume_gt_3": 15,
    "premarket_high_break": 15,
    "bos_bull": 12,
    "choch_bull": 10,
    "fvg_created": 8,
    "fvg_filled": 8,
    "liquidity_sweep_high": 18,
    "spcx_wire": 5,
    "heartbeat": 0,
    # Bearish
    "vwap_loss": -20,
    "orb_break_low": -25,
    "breakdown_low": -20,
    "opening_range_failure": -15,
    "premarket_low_loss": -15,
    "bos_bear": -12,
    "choch_bear": -10,
    "liquidity_sweep_low": -18,
}

HALF_LIFE_HOURS = 6
MAX_AGE_HOURS = 336  # 14 days


def _load_json(path: Path) -> dict | list | None:
    if not path.exists(): return None
    try: return json.loads(path.read_text(encoding="utf-8"))
    except: return None


def _decay(age_hours: float) -> float:
    if age_hours <= 0: return 1.0
    return max(0.0, 0.5 ** (age_hours / HALF_LIFE_HOURS))


def _classify(score: int) -> str:
    if score >= 81: return "Extreme"
    if score >= 61: return "Strong"
    if score >= 41: return "Moderate"
    if score >= 21: return "Neutral"
    return "Weak"


def _load_events() -> list[dict]:
    """Load SPCX CDP events from signal_event.v1."""
    events = []
    sym_file = _SIGNAL_DIR / "latest.json"
    data = _load_json(sym_file)
    if isinstance(data, list):
        events.extend(data)
    elif isinstance(data, dict):
        events.append(data)
    global_file = _VIEWS_DIR / "signal_event.v1" / "latest.json"
    gdata = _load_json(global_file)
    if isinstance(gdata, list):
        for e in gdata:
            if isinstance(e, dict) and ("SPCX" in str(e.get("symbol", ""))):
                if not any(ex.get("timestamp") == e.get("timestamp") and ex.get("event") == e.get("event") for ex in events):
                    events.append(e)
    return events


def compute_signal_strength() -> dict:
    """Score all SPCX CDP events with time decay + bullish/bearish netting."""
    now = datetime.now(timezone.utc)
    events = _load_events()

    scored = []
    windows = {"24h": {"bullish": 0.0, "bearish": 0.0, "net": 0.0, "count": 0},
               "3_sessions": {"bullish": 0.0, "bearish": 0.0, "net": 0.0, "count": 0},
               "1_week": {"bullish": 0.0, "bearish": 0.0, "net": 0.0, "count": 0}}
    total_raw = 0
    total_weighted = 0.0

    for evt in events:
        evt_name = evt.get("event", "")
        weight = EVENT_WEIGHTS.get(evt_name, 0)
        ts_str = evt.get("timestamp", "") or evt.get("written_at", "")
        if not ts_str or weight == 0:
            continue

        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except Exception:
            continue

        age_h = (now - ts).total_seconds() / 3600
        if age_h > MAX_AGE_HOURS:
            continue

        decay = _decay(age_h)
        weighted = weight * decay
        total_raw += abs(weight)
        total_weighted += weighted

        scored.append({
            "event": evt_name, "weight": weight, "age_hours": round(age_h, 1),
            "decay": round(decay, 2), "weighted": round(weighted, 1),
        })

        direction = "bullish" if weight > 0 else "bearish"
        for wkey, wmax in [("24h", 24), ("3_sessions", 72), ("1_week", 168)]:
            if age_h <= wmax:
                windows[wkey][direction] += weighted
                windows[wkey]["net"] += weighted
                windows[wkey]["count"] += 1

    # Top events
    scored.sort(key=lambda x: abs(x["weighted"]), reverse=True)
    top_events = scored[:5]

    # Dynamic normalization: max plausible = sum of all weights at t=0
    max_possible = max(25, sum(abs(s["weight"]) * _decay(s["age_hours"]) for s in scored))
    if max_possible < 20: max_possible = 25

    def _norm(net_val: float) -> int:
        return max(0, min(100, round(net_val / max_possible * 100)))

    strength_24h = _norm(windows["24h"]["net"])
    strength_3s = _norm(windows["3_sessions"]["net"])
    strength_1w = _norm(windows["1_week"]["net"])

    # Active events (fresh, not decayed to dust)
    active = [s["event"] for s in scored if abs(s["weighted"]) >= 3]

    return {
        "symbol": "SPCX",
        "as_of": now.isoformat(),
        "total_events": len(scored),
        "total_raw": total_raw,
        "total_weighted": round(total_weighted, 1),
        "signal_strength": {
            "24h": strength_24h, "3_sessions": strength_3s, "1_week": strength_1w,
            "classification": _classify(strength_24h),
        },
        "windows": {
            "24h": {"score": strength_24h, "events": windows["24h"]["count"],
                    "bullish": round(windows["24h"]["bullish"], 1),
                    "bearish": round(windows["24h"]["bearish"], 1),
                    "net": round(windows["24h"]["net"], 1),
                    "classification": _classify(strength_24h)},
            "3_sessions": {"score": strength_3s, "events": windows["3_sessions"]["count"],
                           "bullish": round(windows["3_sessions"]["bullish"], 1),
                           "bearish": round(windows["3_sessions"]["bearish"], 1),
                           "net": round(windows["3_sessions"]["net"], 1),
                           "classification": _classify(strength_3s)},
            "1_week": {"score": strength_1w, "events": windows["1_week"]["count"],
                       "bullish": round(windows["1_week"]["bullish"], 1),
                       "bearish": round(windows["1_week"]["bearish"], 1),
                       "net": round(windows["1_week"]["net"], 1),
                       "classification": _classify(strength_1w)},
        },
        "active_events": active,
        "top_events": top_events,
        "max_age_hours": MAX_AGE_HOURS,
        "monitor_only": True,
    }


def _compute_deltas(strength: dict, now: datetime) -> dict:
    """Read history and compute signal_strength delta vs 1h, 6h, 24h ago."""
    deltas = {"1h": None, "6h": None, "24h": None, "trend": "stable"}
    if not _HISTORY_PATH.exists():
        return deltas

    thresholds = {"1h": 1, "6h": 6, "24h": 24}
    best = {k: (None, 999) for k in thresholds}  # (score, age_diff_h)

    for line in _HISTORY_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        try: d = json.loads(line)
        except: continue
        ts_str = d.get("as_of", "")
        if not ts_str: continue
        try: ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except: continue
        diff_h = (now - ts).total_seconds() / 3600
        s24 = d.get("signal_strength", {}).get("24h", 0)
        for window, target_h in thresholds.items():
            gap = abs(diff_h - target_h)
            if gap < best[window][1]:
                best[window] = (s24, gap)

    for window, target_h in thresholds.items():
        prev_score, gap = best[window]
        if prev_score is not None and gap < target_h * 1.5:
            deltas[window] = strength["signal_strength"]["24h"] - prev_score

    # Trend
    if deltas["1h"] is not None:
        if deltas["1h"] > 5: deltas["trend"] = "rising"
        elif deltas["1h"] < -5: deltas["trend"] = "falling"
        else: deltas["trend"] = "stable"
    elif deltas["6h"] is not None:
        if deltas["6h"] > 8: deltas["trend"] = "rising"
        elif deltas["6h"] < -8: deltas["trend"] = "falling"

    return deltas


def _write_history(strength: dict) -> None:
    _HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {"as_of": strength["as_of"], "signal_strength": strength["signal_strength"],
             "total_events": strength["total_events"]}
    with open(_HISTORY_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, default=str) + "\n")


def compute_next_confirmation_needed(strength: dict, deltas: dict | None = None) -> dict:
    """Derive actionable next confirmations from signal_strength + trend."""
    score = strength["signal_strength"]["24h"]
    trend = (deltas or {}).get("trend", "stable")
    items = []
    reason = ""
    priority = "low"

    if score < 40:
        items = ["volume_spike", "breakout_above_190"]
        reason = "Signal Neutral/faible: besoin de confirmation volume ou breakout."
        priority = "high"
    elif score < 60:
        items = ["orb_high_hold", "higher_low", "volume_followthrough"]
        reason = "Signal Modere: confirmer maintien structurel."
        priority = "medium"
    elif score < 80:
        items = ["breakout_above_195", "hold_above_190"]
        reason = "Signal Fort: attendre expansion ou maintien au-dessus des niveaux cles."
        priority = "low"
    else:
        items = ["avoid_chase", "wait_pullback", "monitor_exhaustion"]
        reason = "Signal Extreme: risque d'extension, eviter achat impulsif."
        priority = "medium"

    # Trend modifiers
    if trend == "falling":
        items.extend(["vwap_hold", "no_orb_failure"])
        if not reason.endswith("."):
            reason += " Tendance baissiere: surveiller maintien VWAP et ORB."
        else:
            reason += " Tendance baissiere: surveiller maintien VWAP et ORB."
    elif trend == "rising":
        items.append("confirm_followthrough")
        reason += " Tendance haussiere: confirmer suivi du mouvement."

    return {"items": items, "reason": reason, "priority": priority}


# ── Confirmation alias normalizer ──
_CONFIRMATION_ALIASES = {
    "volume_spike": ["volume_spike", "VOLUME_SPIKE", "SPCX_VOLUME_SPIKE", "relative_volume_gt_2", "relative_volume_gt_3"],
    "breakout_above_190": ["breakout_above_190", "BREAK_190", "BREAKOUT_190", "breakout_high", "orb_break_high"],
    "breakout_above_195": ["breakout_above_195", "BREAK_195", "BREAKOUT_195"],
    "orb_high_hold": ["orb_high_hold", "ORB_HOLD", "ORB_HIGH_HOLD"],
    "higher_low": ["higher_low", "HIGHER_LOW"],
    "volume_followthrough": ["volume_followthrough", "VOLUME_FOLLOWTHROUGH", "volume_on_breakout"],
    "vwap_hold": ["vwap_hold", "VWAP_HOLD", "vwap_reclaim"],
    "no_orb_failure": ["no_orb_failure", "NO_ORB_FAILURE"],
    "confirm_followthrough": ["confirm_followthrough", "FOLLOWTHROUGH_CONFIRMATION", "volume_spike", "bos_bull"],
    "avoid_chase": ["avoid_chase"],
    "wait_pullback": ["wait_pullback"],
    "monitor_exhaustion": ["monitor_exhaustion"],
}


def compute_confirmation_boost(ncn: dict, active_events: list, score_24h: int, trend: str) -> dict:
    """Compute priority boost when a next_confirmation_needed item triggers.

    Returns dict with boost amount, triggered items, and reason — ready for Priority Engine.
    """
    if not ncn or not ncn.get("items"):
        return {"confirmation_boost": 0, "confirmation_triggered": False,
                "triggered_items": [], "reason": "No confirmation expected."}

    # Normalize active events to canonical names
    active_norm = set()
    for evt in active_events:
        evt_low = evt.lower().replace(" ", "_")
        for canonical, aliases in _CONFIRMATION_ALIASES.items():
            if evt_low in [a.lower() for a in aliases]:
                active_norm.add(canonical)
                break
        else:
            active_norm.add(evt_low)

    # Check which expected confirmations have triggered
    triggered = [item for item in ncn["items"] if item in active_norm]
    priority = ncn.get("priority", "low")

    # Base boost by priority
    boost_map = {"high": 18, "medium": 10, "low": 5}
    boost = boost_map.get(priority, 0) if triggered else 0

    # Anti-FOMO: score > 80 with avoid_chase → cap boost
    if score_24h > 80 and "avoid_chase" in ncn.get("items", []):
        boost = min(boost, 3)

    # Fatigue: falling trend → reduce
    if trend == "falling":
        boost = max(0, boost - 5)

    reason = ""
    if triggered:
        reason = f"Confirmation {', '.join(triggered)} detectee, boost +{boost}."
    elif priority == "high":
        reason = f"SPCX surveille: attente {', '.join(ncn['items'][:2])}."
    else:
        reason = f"Aucune confirmation declenchee (attendu: {', '.join(ncn['items'][:2])})."

    return {
        "confirmation_boost": boost,
        "confirmation_triggered": len(triggered) > 0,
        "triggered_items": triggered,
        "next_confirmation_priority": priority,
        "reason": reason,
    }


def strength_summary_for_voice() -> str:
    """Voice-friendly one-liner about signal strength + delta."""
    now = datetime.now(timezone.utc)
    strength = compute_signal_strength()
    _write_history(strength)
    deltas = _compute_deltas(strength, now)

    s24 = strength["signal_strength"]["24h"]
    cl = strength["signal_strength"]["classification"]
    trend = deltas.get("trend", "stable")
    trend_fr = {"rising": "en hausse", "falling": "en baisse", "stable": "stable"}.get(trend, trend)
    active = strength.get("active_events", [])
    if not active:
        return "SPCX signal strength: aucun evenement recent."

    parts = [f"SPCX signal strength {s24}/100 ({cl}), {trend_fr}"]
    if deltas.get("6h") is not None:
        parts.append(f"delta 6h {deltas['6h']:+d}")
    parts.append(f"Evenements: {', '.join(active[:3])}")
    # Next confirmation
    ncn = compute_next_confirmation_needed(strength, deltas)
    parts.append(f"Prochaines confirmations: {', '.join(ncn['items'][:3])}")
    return ". ".join(parts) + "."


if __name__ == "__main__":
    r = compute_signal_strength()
    print(json.dumps(r, indent=2, default=str))
