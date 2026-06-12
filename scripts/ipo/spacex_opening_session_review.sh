#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"
source venv/bin/activate 2>/dev/null || true

OUTDIR="$REPO_ROOT/reports/ipo/spacex/session_reviews"
mkdir -p "$OUTDIR"
TS="$(date -u +%Y%m%d_%H%M%S)"

echo "=== SpaceX Opening Session Review ($TS) ==="

python3 - "$OUTDIR" "$TS" <<'PYEOF'
import json, sys, os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from statistics import mean, stdev
from collections import Counter

outdir = Path(sys.argv[1])
ts = sys.argv[2]
repo = Path("/opt/trading")

def load_jsonl(path):
    if not path.exists():
        return []
    results = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return results

def load_json(path, default=None):
    if not path.exists():
        return default or {}
    return json.loads(path.read_text())

raw = load_jsonl(repo / "data/ipo/spacex/raw/events.jsonl")
normalized = load_jsonl(repo / "data/ipo/spacex/normalized/events.jsonl")
snapshot = load_json(repo / "data/ipo/spacex/scored/latest_snapshot.json", {})
enriched = load_json(repo / "data/ipo/spacex/enriched/latest.json", {})
enriched_history = sorted(
    (repo / "data/ipo/spacex/enriched/history").glob("*.json"),
    key=lambda p: p.stat().st_mtime, reverse=True
) if (repo / "data/ipo/spacex/enriched/history").exists() else []

now = datetime.now(timezone.utc).isoformat()

def source_name(src):
    names = {
        "yahoo_chart": "Yahoo Chart",
        "sec_edgar": "SEC EDGAR",
        "yahoo_news_rss": "Yahoo News RSS",
        "tradingview_webhook": "TradingView Webhook",
        "bot_vision_adapter": "Bot Vision",
    }
    return names.get(src, src)

# ============================================================
# AUDIT 1 — SOURCE HEALTH
# ============================================================
print("--- Audit 1: Source Health ---")

sources = {}
for e in raw:
    src = e.get("source", "unknown")
    if src not in sources:
        sources[src] = {"events": 0, "ok": 0, "errors": 0, "latencies": [], "stale": False}
    sources[src]["events"] += 1
    if e.get("ok"):
        sources[src]["ok"] += 1
    else:
        sources[src]["errors"] += 1
    ct = e.get("collected_at")
    if ct:
        try:
            age = (datetime.now(timezone.utc) - datetime.fromisoformat(ct.replace("Z", "+00:00"))).total_seconds()
            sources[src]["latencies"].append(age)
        except (ValueError, TypeError):
            pass

source_report = []
for src, data in sorted(sources.items()):
    lats = data["latencies"]
    min_lat = min(lats) if lats else None
    max_lat = max(lats) if lats else None
    avg_lat = mean(lats) if lats else None
    error_rate = data["errors"] / max(1, data["events"]) * 100
    stale_thresholds = {"yahoo_chart": 300, "tradingview_webhook": 600, "bot_vision_adapter": 1200, "sec_edgar": 86400, "yahoo_news_rss": 3600}
    is_stale = avg_lat and avg_lat > stale_thresholds.get(src, 600) if avg_lat else False

    source_report.append({
        "source": source_name(src),
        "source_id": src,
        "events_received": data["events"],
        "ok_events": data["ok"],
        "error_rate_pct": round(error_rate, 1),
        "latency_min_s": round(min_lat, 1) if min_lat else None,
        "latency_max_s": round(max_lat, 1) if max_lat else None,
        "latency_avg_s": round(avg_lat, 1) if avg_lat else None,
        "stale": is_stale,
        "status": "STALE" if is_stale else ("HEALTHY" if error_rate < 30 else "DEGRADED"),
    })

report1_path = outdir / f"source_health_{ts}.json"
json.dump({"audit": "source_health", "produced_at": now, "sources": source_report, "total_events": len(raw)}, open(report1_path, "w"), indent=2, default=str)

md = ["# SpaceX Source Health Audit", "", f"Generated: {now}", "", "| Source | Events | OK | Error% | Latency Avg | Status |",
      "|---|---:|---:|---:|---:|---|"]
for s in source_report:
    md.append(f"| {s['source']} | {s['events_received']} | {s['ok_events']} | {s['error_rate_pct']}% | {s['latency_avg_s']}s | {s['status']} |")
md_path = outdir / f"source_health_{ts}.md"
md_path.write_text("\n".join(md))
print(f"  Source health: {report1_path} ({len(source_report)} sources)")

# ============================================================
# AUDIT 2 — CONSENSUS
# ============================================================
print("--- Audit 2: Consensus ---")

consensus = enriched.get("consensus", {})
consensus_report = {
    "audit": "consensus",
    "produced_at": now,
    "consensus_price": consensus.get("consensus_price"),
    "source_count": consensus.get("source_count", 0),
    "trusted_source_count": consensus.get("trusted_source_count", 0),
    "disagreement_score": consensus.get("source_disagreement_score", 0),
    "trust_score": consensus.get("weighted_trust_score", 0),
    "stale_sources": consensus.get("stale_sources", []),
    "missing_sources": consensus.get("missing_sources", []),
}

report2_path = outdir / f"consensus_{ts}.json"
json.dump(consensus_report, open(report2_path, "w"), indent=2, default=str)

md2 = ["# SpaceX Consensus Report", "", f"Generated: {now}", "",
       f"- Consensus price: ${consensus_report['consensus_price']}", 
       f"- Sources contributing: {consensus_report['source_count']}/{consensus_report['trusted_source_count']} trusted",
       f"- Disagreement score: {consensus_report['disagreement_score']}%",
       f"- Trust score: {consensus_report['trust_score']}",
       f"- Stale sources: {', '.join(consensus_report.get('stale_sources', [])) or 'none'}",
       f"- Missing sources: {', '.join(consensus_report.get('missing_sources', [])) or 'none'}", ""]
md2_path = outdir / f"consensus_{ts}.md"
md2_path.write_text("\n".join(md2))
print(f"  Consensus: {report2_path} (disagreement={consensus_report['disagreement_score']}%)")

# ============================================================
# AUDIT 3 — FEATURE ACTIVITY
# ============================================================
print("--- Audit 3: Feature Activity ---")

indicators = enriched.get("indicators", {})
smart_money = enriched.get("smart_money", {})
scores = enriched.get("scores", {})

feature_report = []
all_features = {**indicators, **smart_money, **scores}
for name, val in sorted(all_features.items()):
    if val is None:
        status = "MISSING"
    elif isinstance(val, bool):
        status = "ACTIVE" if val else "INACTIVE"
    elif isinstance(val, (int, float)):
        status = "ACTIVE"
    else:
        status = "ACTIVE"
    feature_report.append({"feature": name, "value": val, "status": status})

dead = [f["feature"] for f in feature_report if f["status"] == "MISSING"]
noisy_candidates = [f["feature"] for f in feature_report if f["status"] == "INACTIVE" and isinstance(f.get("value"), bool)]

report3_path = outdir / f"feature_activity_{ts}.json"
json.dump({
    "audit": "feature_activity",
    "produced_at": now,
    "total_features": len(feature_report),
    "dead_features": len(dead),
    "dead_list": dead,
    "noisy_features": len(noisy_candidates),
    "noisy_list": noisy_candidates,
    "features": feature_report,
}, open(report3_path, "w"), indent=2, default=str)

md3 = ["# SpaceX Feature Activity Report", "", f"Generated: {now}", "",
       f"| Total | Dead | Noisy | Active |",
       f"|---|---:|---:|---:|",
       f"| {len(feature_report)} | {len(dead)} | {len(noisy_candidates)} | {len(feature_report)-len(dead)} |", "",
       "## Dead Features (MISSING)", ""]
for d in dead:
    md3.append(f"- `{d}`")
md3 += ["", "## Inactive Boolean Features", ""]
for n in noisy_candidates:
    md3.append(f"- `{n}`")
md3_path = outdir / f"feature_activity_{ts}.md"
md3_path.write_text("\n".join(md3))
print(f"  Features: {report3_path} ({len(dead)} dead, {len(noisy_candidates)} noisy)")

# ============================================================
# AUDIT 4 — ALERT REVIEW
# ============================================================
print("--- Audit 4: Alert Review ---")

alert_path = repo / "data/ipo/spacex/alerts/log.jsonl"
alerts = load_jsonl(alert_path)

signals = snapshot.get("signals", [])
scores_data = snapshot.get("scores", {})

alert_report = {
    "audit": "alert_review",
    "produced_at": now,
    "active_signals": signals,
    "active_signal_count": len(signals),
    "alert_log_entries": len(alerts),
    "trade_ready": scores_data.get("trade_ready", 0),
    "accumulation": scores_data.get("accumulation", 0),
    "risk": scores_data.get("risk", 0),
}

report4_path = outdir / f"alert_review_{ts}.json"
json.dump(alert_report, open(report4_path, "w"), indent=2, default=str)

md4 = ["# SpaceX Alert Review", "", f"Generated: {now}", "",
       f"- Active signals: {len(signals)}", 
       f"- Alert log entries: {len(alerts)}",
       f"- Trade ready: {scores_data.get('trade_ready', 0)}",
       f"- Accumulation: {scores_data.get('accumulation', 0)}",
       f"- Risk: {scores_data.get('risk', 0)}", ""]
if signals:
    md4.append("## Active Signals")
    for s in signals:
        md4.append(f"- `{s}`")
md4_path = outdir / f"alert_review_{ts}.md"
md4_path.write_text("\n".join(md4))
print(f"  Alerts: {report4_path} ({len(signals)} active signals)")

# ============================================================
# AUDIT 5 — OPENING RANGE
# ============================================================
print("--- Audit 5: Opening Range ---")

or5 = indicators.get("opening_range_5m", {})
or15 = indicators.get("opening_range_15m", {})
price = snapshot.get("price", 135)
ipo_price = snapshot.get("ipo_price", 135)

orb_report = {
    "audit": "opening_range",
    "produced_at": now,
    "price": price,
    "ipo_price": ipo_price,
    "ipo_gap_pct": indicators.get("ipo_gap_pct"),
    "prev_gap_pct": indicators.get("prev_gap_pct"),
    "vwap": indicators.get("vwap"),
    "vwap_distance_pct": indicators.get("vwap_distance_pct"),
    "relative_volume": indicators.get("relative_volume"),
    "volume_zscore": indicators.get("volume_zscore"),
    "opening_range_5m_high": or5.get("high"),
    "opening_range_5m_low": or5.get("low"),
    "opening_range_15m_high": or15.get("high"),
    "opening_range_15m_low": or15.get("low"),
    "atr_14": indicators.get("atr_14"),
    "rsi_14": indicators.get("rsi_14"),
    "fvg_bullish": smart_money.get("fvg_bullish"),
    "fvg_bearish": smart_money.get("fvg_bearish"),
    "bos": smart_money.get("bos"),
}

# Setup grading
def grade_setup(or_high, or_low, price_val, rel_vol, ipo_gap_pct):
    if not price_val or not rel_vol:
        return "NO_TRADE"
    if or_high and price_val > or_high and rel_vol > 1.5 and (ipo_gap_pct or 0) > 5:
        return "A_PLUS"
    if or_high and price_val > or_high and rel_vol > 1.2:
        return "A"
    if or_low and price_val > or_low and rel_vol > 0.8:
        return "B"
    return "NO_TRADE"

orb_report["or15_setup_grade"] = grade_setup(
    or15.get("high"), or15.get("low"), price,
    indicators.get("relative_volume", 1.0),
    indicators.get("ipo_gap_pct", 0)
)

report5_path = outdir / f"opening_range_{ts}.json"
json.dump(orb_report, open(report5_path, "w"), indent=2, default=str)

md5 = ["# SpaceX Opening Range Review", "", f"Generated: {now}", "",
       f"- Price: ${price}", f"- IPO gap: {indicators.get('ipo_gap_pct')}%", 
       f"- Rel vol: {indicators.get('relative_volume')}", f"- VWAP: {indicators.get('vwap')}",
       f"- ATR 14: {indicators.get('atr_14')}", f"- RSI 14: {indicators.get('rsi_14')}", "",
       f"## Opening Range 5M", f"- High: {or5.get('high')}", f"- Low: {or5.get('low')}", "",
       f"## Opening Range 15M", f"- High: {or15.get('high')}", f"- Low: {or15.get('low')}", "",
       f"## Setup Grade: **{orb_report['or15_setup_grade']}**",
       f"- FVG bullish: {smart_money.get('fvg_bullish')}", f"- FVG bearish: {smart_money.get('fvg_bearish')}",
       f"- BOS: {smart_money.get('bos')}", ""]
md5_path = outdir / f"opening_range_{ts}.md"
md5_path.write_text("\n".join(md5))
print(f"  Opening range: {report5_path} (grade={orb_report['or15_setup_grade']})")

# ============================================================
# FINAL SUMMARY
# ============================================================
summary = {
    "review_id": ts,
    "produced_at": now,
    "total_raw_events": len(raw),
    "total_normalized_events": len(normalized),
    "total_enriched_snapshots": len(enriched_history),
    "source_count": len(sources),
    "stale_sources": [s["source"] for s in source_report if s["stale"]],
    "dead_features": dead,
    "active_signals": signals,
    "opening_range_grade": orb_report.get("or15_setup_grade"),
    "reports": {
        "source_health": str(report1_path),
        "consensus": str(report2_path),
        "feature_activity": str(report3_path),
        "alert_review": str(report4_path),
        "opening_range": str(report5_path),
    },
}
summary_path = outdir / f"review_summary_{ts}.json"
json.dump(summary, open(summary_path, "w"), indent=2, default=str)
print(f"\n=== Review Complete ===")
print(f"Summary: {summary_path}")
print(f"Total events: {len(raw)} raw, {len(normalized)} normalized")
print(f"Sources: {len(sources)} ({sum(1 for s in source_report if s['stale'])} stale)")
print(f"Features: {len(feature_report)} ({len(dead)} dead)")
print(f"Opening range grade: {orb_report['or15_setup_grade']}")
PYEOF

echo "SPACEX_OPENING_SESSION_REVIEW_OK"
