#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"
source venv/bin/activate 2>/dev/null || true

python3 - "$REPO_ROOT" <<'PYEOF'
import json, sys, os
from pathlib import Path
from datetime import datetime, timezone
from statistics import mean

repo = Path(sys.argv[1])
snap_path = repo / "data/ipo/spacex/scored/latest_snapshot.json"
event_path = repo / "data/ipo/spacex/raw/events.jsonl"
outdir = repo / "reports/ipo/spacex/war_room"
outdir.mkdir(parents=True, exist_ok=True)
ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

SNAPSHOT = repo / "data/ipo/spacex/scored/latest_snapshot.json"
STATE_PATH = repo / "data/ipo/spacex/_open_state.json"

def load_json(p, default=None):
    if not p.exists():
        return default or {}
    return json.loads(p.read_text())

def load_jsonl(p):
    if not p.exists():
        return []
    results = []
    with p.open() as f:
        for line in f:
            line = line.strip()
            if line:
                try: results.append(json.loads(line))
                except: continue
    return results

def save_json(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w") as f:
        json.dump(data, f, indent=2, default=str)

snapshot = load_json(SNAPSHOT, {})
price = snapshot.get("price")
volume = snapshot.get("relative_volume_estimate")
ipo_price = snapshot.get("ipo_price", 135)
scores = snapshot.get("scores", {})
signals = snapshot.get("signals", [])

prev_state = load_json(STATE_PATH, {"was_open": False, "open_detected_at": None, "first_price": None, "first_volume": None})

is_open_now = (price is not None and price != ipo_price) or (volume is not None and volume > 0)
just_opened = is_open_now and not prev_state.get("was_open", False)
was_open = prev_state.get("was_open", False)

# Update state
new_state = {
    "was_open": is_open_now or was_open,
    "open_detected_at": prev_state.get("open_detected_at") or (datetime.now(timezone.utc).isoformat() if just_opened else None),
    "first_price": prev_state.get("first_price") or (price if just_opened else None),
    "first_volume": prev_state.get("first_volume") or (volume if just_opened else None),
    "last_checked": datetime.now(timezone.utc).isoformat(),
    "just_opened": just_opened,
}
save_json(STATE_PATH, new_state)

if not is_open_now and was_open:
    pass  # Market closed — still produce report
elif not is_open_now and not was_open:
    # Pre-market — periodic check
    events = load_jsonl(event_path)
    summary = {
        "status": "PRE_MARKET",
        "checked_at": new_state["last_checked"],
        "price": price,
        "ipo_price": ipo_price,
        "total_events": len(events),
        "signals": signals,
        "scores": scores,
        "message": "SPCX not yet trading. Waiting for open.",
    }
    save_json(outdir / f"war_room_{ts}.json", summary)
    print(json.dumps(summary, indent=2, default=str))
    sys.exit(0)

# ============================================================
# MARKET IS OPEN — WAR ROOM
# ============================================================
events = load_jsonl(event_path)
enriched = load_json(repo / "data/ipo/spacex/enriched/latest.json", {})
indicators = enriched.get("indicators", {})
smart_money = enriched.get("smart_money", {})
consensus = enriched.get("consensus", {})

if just_opened:
    print("=== OPEN DETECTED! Market is now live. ===")

# --- Opening Gap ---
gap_pct = indicators.get("ipo_gap_pct", 0) or 0
gap_class = (
    "STRONG_GAP" if abs(gap_pct) > 5 else
    "MODERATE_GAP" if abs(gap_pct) > 2 else
    "FLAT_OPEN"
)

# --- Opening Range ---
or5 = indicators.get("opening_range_5m", {})
or15 = indicators.get("opening_range_15m", {})
or30 = indicators.get("opening_range_30m", {})

orb_valid = bool(or5.get("high") and or5.get("low"))
orb_5m_range = (or5.get("high") - or5.get("low")) if orb_valid else None
orb_15m_range = (or15.get("high") - or15.get("low")) if or15.get("high") and or15.get("low") else None

# --- VWAP State ---
vwap_val = indicators.get("vwap")
vwap_dist = indicators.get("vwap_distance_pct", 0) or 0
vwap_state = (
    "ABOVE_VWAP" if vwap_dist > 0.2 else
    "BELOW_VWAP" if vwap_dist < -0.2 else
    "ON_VWAP"
)

# --- Volume State ---
rel_vol = indicators.get("relative_volume", 1) or 1
vol_z = indicators.get("volume_zscore", 0) or 0
vol_class = (
    "EXPLOSIVE" if rel_vol > 3 or vol_z > 2.5 else
    "ELEVATED" if rel_vol > 1.5 or vol_z > 1.0 else
    "NORMAL" if rel_vol > 0.7 else
    "ANEMIC"
)

# --- News State ---
news_count = enriched.get("context", {}).get("news_count", 0)
filing_count = enriched.get("context", {}).get("sec_filings_count", 0)
news_class = (
    "HOT" if news_count > 5 else
    "MODERATE" if news_count > 2 else
    "LOW" if news_count > 0 else
    "NONE"
)

# --- Consensus State ---
disagreement = consensus.get("source_disagreement_score", 0) or 0
trust = consensus.get("weighted_trust_score", 0) or 0
stale_count = len(consensus.get("stale_sources", []))
consensus_class = (
    "STRONG" if trust > 0.7 and disagreement < 5 else
    "MODERATE" if trust > 0.4 else
    "WEAK" if trust > 0 else
    "NO_CONSENSUS"
)

# --- OPEN SCORE (0-100) ---
open_score = 0.0
if gap_pct > 0:
    open_score += min(25, abs(gap_pct) * 3)
if rel_vol and rel_vol > 1:
    open_score += min(25, (rel_vol - 1) * 8)
if news_class in ("HOT", "MODERATE"):
    open_score += min(15, news_count * 3)
if consensus_class == "STRONG":
    open_score += 10
if consensus_class == "MODERATE":
    open_score += 5
if smart_money.get("fvg_bullish"):
    open_score += 10
if smart_money.get("bos"):
    open_score += 15
open_score = round(min(100, open_score))

# --- Classification ---
if open_score >= 85:
    classification = "A+_IPO_MOMENTUM"
elif open_score >= 70:
    classification = "A_IPO_MOMENTUM"
elif open_score >= 55 and vwap_state == "ABOVE_VWAP":
    classification = "A_VWAP_RECLAIM"
elif open_score >= 45 and smart_money.get("fvg_bullish"):
    classification = "A_FVG_RECLAIM"
elif open_score >= 30:
    classification = "B_WATCH"
else:
    classification = "NO_TRADE"

# --- Active Setups ---
setups_active = []
if classification in ("A+_IPO_MOMENTUM", "A_IPO_MOMENTUM"):
    setups_active.append({"setup": "IPO_ORB_5M", "confidence": "HIGH" if open_score >= 85 else "MODERATE"})
    setups_active.append({"setup": "GAP_AND_GO", "confidence": "HIGH" if gap_pct > 5 else "MODERATE"})
if classification == "A_VWAP_RECLAIM":
    setups_active.append({"setup": "VWAP_RECLAIM", "confidence": "HIGH"})
if classification == "A_FVG_RECLAIM":
    setups_active.append({"setup": "FVG_RECLAIM", "confidence": "HIGH"})
if classification == "B_WATCH":
    setups_active.append({"setup": "WEEKLY_MOMENTUM", "confidence": "LOW"})

war_room = {
    "status": "MARKET_OPEN" if just_opened else "MARKET_OPEN_CONTINUING",
    "war_room_id": ts,
    "produced_at": datetime.now(timezone.utc).isoformat(),
    "open_detected_at": new_state.get("open_detected_at"),
    "first_price": new_state.get("first_price"),
    "first_volume": new_state.get("first_volume"),
    "current": {
        "price": price,
        "ipo_price": ipo_price,
        "gap_pct": gap_pct,
        "gap_class": gap_class,
        "volume_class": vol_class,
        "relative_volume": rel_vol,
        "volume_zscore": vol_z,
        "vwap": vwap_val,
        "vwap_state": vwap_state,
        "vwap_distance_pct": vwap_dist,
        "news_class": news_class,
        "consensus_class": consensus_class,
        "consensus_disagreement": disagreement,
        "consensus_trust": trust,
    },
    "opening_range": {
        "orb_5m": or5,
        "orb_15m": or15,
        "orb_30m": or30,
        "orb_5m_range": orb_5m_range,
        "orb_15m_range": orb_15m_range,
        "orb_15m_valid": bool(or15.get("high")),
    },
    "smart_money": {
        "fvg_bullish": smart_money.get("fvg_bullish"),
        "fvg_bearish": smart_money.get("fvg_bearish"),
        "bos": smart_money.get("bos"),
        "choch": smart_money.get("choch"),
        "smc_bias": smart_money.get("smc_bias"),
        "smc_score": smart_money.get("smc_score"),
    },
    "scores": {
        "open_score": open_score,
        "classification": classification,
        "trade_ready": scores.get("trade_ready", 0),
        "accumulation": scores.get("accumulation", 0),
        "momentum": scores.get("momentum", 0),
        "risk": scores.get("risk", 0),
    },
    "active_setups": setups_active,
    "active_signals": signals,
    "event_log": {
        "raw_events": len(events),
        "sources": list(set(e.get("source", "unknown") for e in events)),
    },
}

save_json(outdir / f"war_room_{ts}.json", war_room)
save_json(outdir / "war_room_latest.json", war_room)
save_json(repo / "ui/spacex_desk/war_room.json", war_room)

# MD report
md = [
    f"# SpaceX Opening War Room — {classification}",
    "",
    f"Generated: {war_room['produced_at']}",
    f"Status: {war_room['status']}",
    "",
    "## Opening Metrics",
    "",
    f"| Metric | Value | Class |",
    f"|---|---|---|",
    f"| Price | ${price} | |",
    f"| Gap vs IPO | {gap_pct}% | {gap_class} |",
    f"| Volume | {rel_vol}x | {vol_class} |",
    f"| VWAP | {vwap_val} | {vwap_state} |",
    f"| Consensus | trust={trust} disagree={disagreement}% | {consensus_class} |",
    f"| News | {news_count} articles | {news_class} |",
    f"| FVG | bull={'YES' if smart_money.get('fvg_bullish') else 'no'} bear={'YES' if smart_money.get('fvg_bearish') else 'no'} | |",
    f"| BOS | {'YES' if smart_money.get('bos') else 'no'} | |",
    "",
    "## Opening Range",
    "",
    f"| ORB | High | Low | Range |",
    f"|---|---:|---:|---:|",
    f"| 5M | {or5.get('high')} | {or5.get('low')} | {orb_5m_range} |",
    f"| 15M | {or15.get('high')} | {or15.get('low')} | {orb_15m_range} |",
    "",
    f"## Score: {open_score}/100 → **{classification}**",
    "",
    "## Active Setups",
    "",
]
for s in setups_active:
    md.append(f"- **{s['setup']}** ({s['confidence']})")

try:
    from modules.ipo_tracking.ipo_analogs import compute_analog_score
    spcx = {
        "gap_pct": gap_pct,
        "relative_volume": rel_vol,
        "fvg_bullish": smart_money.get("fvg_bullish"),
        "bos": smart_money.get("bos"),
        "vwap_distance_pct": vwap_dist,
        "ipo_price": ipo_price,
    }
    analog = compute_analog_score(spcx)
    if analog.get("top_match"):
        war_room["ipo_analog"] = analog
        md.append("")
        md.append("## IPO Analog Score")
        md.append("")
        for r in analog.get("top3", []):
            md.append(f"- **{r['symbol']}** ({r['name']}): {r['score']} -- Day1 return: {r['day1_return']}% ORB: {r['orb_5m']}%")
        if analog.get("analog_consensus"):
            ac = analog["analog_consensus"]
            md.append("")
            md.append(f"Direction: **{ac.get('direction', 'NEUTRAL')}**")
            md.append(f"Avg day1 return: {ac.get('avg_day1_return_pct')}%")
            md.append(f"Likely setups: {', '.join(ac.get('likely_setups', []))}")
except ImportError:
    pass

md.append("")
md.append("## Signals")
for s in signals:
    md.append(f"- `{s}`")
md.append("")
md.append("## Monitor-Only")
md.append("")
md.append("No automated execution. Decision support only.")

md_path = outdir / f"war_room_{ts}.md"
md_path.write_text("\n".join(md))

md_latest = outdir / "war_room_latest.md"
md_latest.write_text("\n".join(md))

print(json.dumps(war_room, indent=2, default=str))
if just_opened:
    print("SPACEX_OPEN_DETECTED")
else:
    print("SPACEX_WAR_ROOM_OK")
PYEOF
