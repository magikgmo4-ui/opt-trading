#!/usr/bin/env bash
# batch_qualify.sh — Batch qualification runner for Telegram signal channels
# Runs 1-4x/day. Parses all available raw data, produces qualification matrix.
# No LLM/OCR. Regex text parsing only.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "============================================"
echo "  BATCH CHANNEL QUALIFICATION"
echo "  $(date -Is)"
echo "============================================"

# ── Step 1: Parse all raw messages ──────────────────────────────────────
echo ""
echo "[1/4] Parsing all raw messages..."
python3 << 'PYEOF'
import sys; sys.path.insert(0, '.')
from modules.analysis_bundles.app.telegram_screener_bridge import produce_channel_stats, produce_latest_index

idx = produce_latest_index()
stats = produce_channel_stats()

# Print qualification matrix
print(f"  Total channels: {stats['total_channels']}")
print(f"  Total messages: {stats['total_messages']}")
print(f"  Trade signals:  {idx['signals']}")
print(f"  Active: {idx['active_channels']}, Qualified: {idx['qualified_channels']}")
print()
print(f"  {'Channel':30s} {'Mode':12s} {'Msgs':>5s} {'Setups':>6s} {'Complete':>8s} {'Score':>5s}")
print(f"  {'-'*70}")
for ch in stats['channels']:
    name = ch['channel'][:28]
    mode = ch.get('mode', '?')
    msgs = ch['total_messages']
    setups = ch['trade_setups']
    complete = ch.get('complete_setups', 0)
    score = ch.get('candidate_score', 0)
    if msgs > 0 or mode in ('ACTIVE', 'QUALIFIED'):
        print(f"  {name:30s} {mode:12s} {msgs:>5d} {setups:>6d} {complete:>8d} {score:>5d}")
PYEOF

# ── Step 2: Archive complete signals ─────────────────────────────────────
echo ""
echo "[2/4] Archiving trade signals..."
python3 << 'PYEOF'
import sys; sys.path.insert(0, '.')
from modules.analysis_bundles.app.signal_tracker import archive_all_channels
result = archive_all_channels()
print(f"  Total archived: {result['total_signals']} signals")
for ch, info in result.get('channels', {}).items():
    if info.get('signals', 0) > 0:
        print(f"  {ch:30s} {info['signals']:>3d} signals  ({info.get('first_ts', '?')} → {info.get('last_ts', '?')})")
PYEOF

# ── Step 3: Check discovery catalog ──────────────────────────────────────
echo ""
echo "[3/4] Discovery catalog status..."
python3 << 'PYEOF'
import json
from pathlib import Path

cfg_path = Path("configs/telegram/discovery_channels.json")
if cfg_path.exists():
    with open(cfg_path) as f:
        cfg = json.load(f)
    channels = cfg.get('channels', cfg.get('discovery_channels', []))
    total = len(channels)
    enabled = sum(1 for c in channels if c.get('enabled'))
    print(f"  Catalog: {total} channels, {enabled} enabled, {total - enabled} pending discovery")
else:
    print("  No discovery catalog found")

# Check which DISCOVERY channels have data
raw_dir = Path("modules/collector_telegram/outputs/raw")
if raw_dir.exists():
    existing = {f.stem for f in raw_dir.glob("*.jsonl")}
    with_data = [c['alias'] for c in channels if c['alias'] in existing]
    print(f"  Channels with data: {len(with_data)}/{total}")
    if with_data:
        print(f"    {', '.join(with_data[:10])}...")
PYEOF

# ── Step 4: Write summary ────────────────────────────────────────────────
echo ""
echo "[4/4] Writing qualification summary..."
python3 << 'PYEOF'
import json
from datetime import datetime, timezone
from pathlib import Path

summary_path = Path("data/telegram_screener/qualification_summary.json")
summary_path.parent.mkdir(parents=True, exist_ok=True)

summary = {
    "contract": "telegram_qualification_summary.v1",
    "produced_at": datetime.now(timezone.utc).isoformat(),
    "mode": "regex_only",
    "llm_used": False,
    "ocr_used": False,
}
summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(f"  Written: {summary_path}")
PYEOF

echo ""
echo "============================================"
echo "  QUALIFICATION COMPLETE"
echo "  $(date -Is)"
echo "============================================"
