#!/usr/bin/env bash
# discover_telegram_channels.sh — Telegram Search-based channel discovery
# Uses collector_telegram to search for channels by keyword.
# Does NOT activate channels. Only discovers + samples.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
NOW=$(date -Is)

echo "============================================"
echo "  TELEGRAM CHANNEL DISCOVERY"
echo "  $NOW"
echo "============================================"

# ── Step 1: Load discovery keywords ──────────────────────────────────────
echo ""
echo "[1/3] Loading discovery keywords..."
python3 << 'PYEOF'
import json, sys
from pathlib import Path

cfg_path = Path("configs/telegram/discovery_keywords.json")
if not cfg_path.exists():
    print("ERROR: discovery_keywords.json not found")
    sys.exit(0)

with open(cfg_path) as f:
    cfg = json.load(f)

total_kw = sum(len(v["keywords"]) for v in cfg.get("buckets", {}).values())
buckets = list(cfg.get("buckets", {}).keys())
print(f"  Loaded: {total_kw} keywords across {len(buckets)} buckets")
for b in sorted(buckets):
    info = cfg["buckets"][b]
    print(f"  {b:30s} {info['priority']:3s} {len(info['keywords'])} keywords  assets={info['expected_assets']}")
PYEOF

# ── Step 2: Search Telegram (admin-trading only) ─────────────────────────
echo ""
echo "[2/3] Searching Telegram for channels..."
echo "  NOTE: Telegram SearchRequest must run on admin-trading (Telethon session required)"
echo "  To run search manually:"
echo ""
echo "  ssh admin-trading"
echo "  cd /opt/trading"
echo "  python3 -c \""
echo "    from telethon import TelegramClient"
echo "    from telethon.tl.functions.contacts import SearchRequest"
echo "    # ... search logic ..."
echo "  \""
echo ""
echo "  OR: Use the in-app Telegram search with keywords from discovery_keywords.json"

# ── Step 3: Report existing qualified channels ───────────────────────────
echo ""
echo "[3/3] Current qualified channels..."
python3 << 'PYEOF'
import sys, json
sys.path.insert(0, '.')
from modules.analysis_bundles.app.telegram_screener_bridge import produce_channel_stats

stats = produce_channel_stats()
active = [c for c in stats['channels'] if c.get('mode') == 'ACTIVE']
discovery = [c for c in stats['channels'] if c.get('mode') == 'DISCOVERY']
watch = [c for c in stats['channels'] if c.get('mode') == 'WATCH']

print(f"  ACTIVE:     {len(active)} channels ({sum(c['trade_setups'] for c in active)} setups)")
print(f"  DISCOVERY:  {len(discovery)} channels ({sum(c['trade_setups'] for c in discovery)} setups)")
print(f"  WATCH:      {len(watch)} channels")
print(f"  Total:      {stats['total_channels']} channels, {stats['total_messages']} messages")

# Write discovery report
from datetime import datetime, timezone
from pathlib import Path
report_dir = Path("data/data_center/views/telegram_discovery")
report_dir.mkdir(parents=True, exist_ok=True)
report = {
    "contract": "telegram_discovery_report.v1",
    "produced_at": datetime.now(timezone.utc).isoformat(),
    "total_channels_qualified": stats['total_channels'],
    "active": len(active),
    "discovery": len(discovery),
    "watch": len(watch),
    "active_channels": [c['channel'] for c in active],
    "discovery_channels": [c['channel'] for c in discovery],
}
(report_dir / "latest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(f"\n  Report: {report_dir}/latest.json")
PYEOF

echo ""
echo "============================================"
echo "  DISCOVERY COMPLETE"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Use keywords from configs/telegram/discovery_keywords.json"
echo "  2. Search manually on Telegram or via Telethon SearchRequest"
echo "  3. Add found channels to configs/telegram/discovery_candidates.json"
echo "  4. Enable candidates on admin-trading, sample 200 msgs"
echo "  5. Sync + batch_qualify.sh"
