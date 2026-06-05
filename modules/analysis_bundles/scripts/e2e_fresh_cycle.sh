#!/usr/bin/env bash
# e2e_fresh_cycle.sh — Full end-to-end fresh analysis cycle
# Produces: FRESH BTC chart + live Binance data → TRADABLE verdict
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "============================================"
echo "  E2E FRESH CYCLE"
echo "  $(date -Is)"
echo "============================================"

# ── Step 1: Capture + analyze BTC on admin-trading ──────────────────────
echo ""
echo "[1/5] Capturing BTC fresh screenshot on admin-trading..."
ssh admin-trading "
    cd /opt/trading/modules/bot_vision/headless_capture
    timeout 90 python3 scripts/run_vision_pipeline.py \
        --profile profiles.btcusdt_poc.json \
        --real-ocr \
        2>&1 | tail -5
" || echo "  WARN: capture may have timed out, continuing..."

# ── Step 2: Force OpenAI analysis + inject into datacenter ──────────────
echo ""
echo "[2/5] Running OpenAI analysis on latest BTC screenshot..."
ssh admin-trading '
    cd /opt/trading
    VENV=/opt/trading/.venvs/bot_vision_step2/bin/python
    BOT=/opt/trading/modules/bot_vision_step2/app/bot_vision_step2.py

    # Run analyze_latest
    $VENV $BOT analyze_latest 2>/dev/null

    # Find the latest summary.json
    RUNS_DIR=/opt/trading/data/deskpro/vision/runs
    LATEST_RUN=$(ls -td $RUNS_DIR/*/ 2>/dev/null | head -1)
    SUMMARY=$LATEST_RUN/summary.json

    if [ ! -f "$SUMMARY" ]; then
        echo "ERROR: no summary.json found"
        exit 1
    fi

    # Extract signals and inject into by_symbol
    python3 << '\''PYEOF'\''
import json, sys
from pathlib import Path
from datetime import datetime, timezone

runs_dir = Path("/opt/trading/data/deskpro/vision/runs")
runs = sorted(runs_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)

for run_dir in runs:
    summary_path = run_dir / "summary.json"
    if not summary_path.exists():
        continue
    with open(summary_path) as f:
        summary = json.load(f)

    src = summary.get("source_screenshot", "")
    if "tradingview_BTCUSDT" not in src:
        continue

    signals = summary.get("signals", {})
    charts = signals.get("charts", [])
    if not charts:
        # Try to extract from analysis_text
        text = summary.get("analysis_text", "")
        if text:
            import re
            m = re.search(r"bias.*?:\s*(\w+)", text)
            bias = m.group(1) if m else None
            # Use raw text as analysis
            charts = [{
                "slot": "single", "bias": bias or "neutre",
                "supports": [], "resistances": [],
                "plan": text[:200], "invalidation": "",
                "structure": ""
            }]
        else:
            continue

    chart = charts[0] if charts else {}
    now = datetime.now(timezone.utc).isoformat()

    # Build capture entry
    new_capture = {
        "input_class": "vision_analysis.v1",
        "capture_id": f"cap_fresh_{run_dir.name}",
        "screen_type": "CHART_TECHNICAL",
        "symbol": "BTCUSDT.P",
        "timeframe": "15m",
        "analysis_ts": summary.get("ts", now),
        "source_module": "bot_vision_step2",
        "source_module_version": "1.0.0",
        "freshness_state": "fresh",
        "capture_status": "ready",
        "run_id": run_dir.name,
        "signals": [],
        "analysis_summary": summary.get("analysis_text", ""),
    }

    # Build signals from chart
    for s_val in chart.get("supports", []):
        try:
            new_capture["signals"].append({
                "type": "support_level", "value": float(s_val),
                "confidence": 0.75, "note": "support_level from chart analysis"
            })
        except (ValueError, TypeError):
            pass
    for r_val in chart.get("resistances", []):
        try:
            new_capture["signals"].append({
                "type": "resistance_level", "value": float(r_val),
                "confidence": 0.75, "note": "resistance_level from chart analysis"
            })
        except (ValueError, TypeError):
            pass
    if chart.get("plan"):
        new_capture["signals"].append({
            "type": "analysis_note", "value": chart["plan"],
            "confidence": 0.6, "note": "plan from chart analysis"
        })
    if chart.get("invalidation"):
        new_capture["signals"].append({
            "type": "analysis_note", "value": chart["invalidation"],
            "confidence": 0.6, "note": "invalidation from chart analysis"
        })

    # Prepend to by_symbol
    by_sym = Path("/opt/trading/data/data_center/views/vision_analysis/by_symbol/BTCUSDT.P.json")
    with open(by_sym) as f:
        existing = json.load(f)
    existing.insert(0, new_capture)
    with open(by_sym, "w") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    signal_count = len(new_capture["signals"])
    total_count = len(existing)
    print(f"OK: injected fresh BTC analysis ({signal_count} signals, {total_count} total)")
    break
else:
    print("ERROR: no BTC chart analysis found in recent runs")
    sys.exit(1)
PYEOF
' || echo "  WARN: OpenAI analysis failed, using existing data"

# ── Step 3: Sync from admin-trading ─────────────────────────────────────
echo ""
echo "[3/5] Syncing data from admin-trading..."
bash "$PROJECT_ROOT/modules/analysis_bundles/scripts/sync_admin_trading.sh" 2>&1 | tail -2

# ── Step 4: Live market metrics + pipeline ───────────────────────────────
echo ""
echo "[4/5] Running live Binance collector + full pipeline..."
python3 << 'PYEOF'
import sys
sys.path.insert(0, '.')

from modules.analysis_bundles.app.market_metrics_writer import write_all
from modules.analysis_bundles.app.btc_core_producer import produce_btc_core
from modules.analysis_bundles.app.macro_producer import produce_macro
from modules.analysis_bundles.app.verdict_consumer import consume_and_write
from modules.analysis_bundles.app.analysis_pipeline import run_full_pipeline
from modules.analysis_bundles.app.vision_analysis_reader import extract_signals_from_vision

# Live market data
written = write_all()
print(f"Market metrics: {written}")

# BTC vision check
sig = extract_signals_from_vision("BTCUSDT.P")
print(f"BTC vision: fresh={sig['freshness']} bias={sig['bias']} supports={sig['supports'][:2]}")

# Produce bundles
btc = produce_btc_core()
macro = produce_macro()
verdict = consume_and_write(btc_bundle=btc.to_dict(), macro_bundle=macro.to_dict())

# Full report
run_full_pipeline()

bd = btc.to_dict()
md = macro.to_dict()
v = verdict.to_dict()
c = v["composite"]

print()
print("============================================")
print("  VERDICT")
print("============================================")
print(f"  BTC:       fresh={bd['freshness_state']:8s}  quality={bd.get('data_quality','?'):10s}  bias={bd['analysis']['bias_short_term']:10s}  conf={bd['analysis']['confidence']:8s}")
mm = bd['inputs']['market_metrics']
    price_str = str(mm.get('last_price', '?'))
    print(f"             mm_price={price_str:>10s}  provider={mm.get('provider','?')}")
print(f"  MACRO:     fresh={md['freshness_state']:8s}  quality={md.get('data_quality','?'):10s}  regime={md['analysis']['regime']:10s}  conf={md['analysis']['confidence']:8s}")
print(f"  VERDICT:   fresh={v['freshness_state']:8s}  align={c['alignment']:10s}  bias={c['overall_bias']:10s}  conf={c['confidence']:8s}  score={c['score']}")
print()

ok = c['confidence'] not in ('LOW','UNKNOWN') and v['freshness_state'] in ('FRESH',)
print(f"  TRADABLE: {'*** YES ***' if ok else 'NO'}  (gate: conf={c['confidence']}, fresh={v['freshness_state']})")
if not ok:
    print(f"  Blockers: ", end="")
    if c['confidence'] in ('LOW', 'UNKNOWN'): print(f"confidence={c['confidence']} ", end="")
    if v['freshness_state'] != 'FRESH': print(f"freshness={v['freshness_state']} ", end="")
    print()
print("============================================")
PYEOF

echo ""
echo "[5/5] Done. Runtime outputs refreshed:"
echo "  data/deskpro/inputs/analysis_verdict/latest.json"
echo "  data/deskpro/inputs/analysis_report/latest.json"
echo "  data/data_center/views/market_metrics/latest.json"
