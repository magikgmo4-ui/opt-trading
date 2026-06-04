#!/usr/bin/env bash
# Sync fresh data from admin-trading to local repo
# Run periodically (cron or manual) before analysis pipeline

set -euo pipefail
LOCAL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
REMOTE="admin-trading:/opt/trading"
DRY=${1:-}

sync_dir() {
    local src="$1"
    local dst="$2"
    if [ -n "$DRY" ]; then
        echo "[DRY] rsync $src -> $dst"
    else
        mkdir -p "$dst"
        rsync -avz --timeout=10 "$src" "$dst" 2>/dev/null || echo "[WARN] sync failed: $src"
    fi
}

echo "=== sync admin-trading -> local ==="
echo "local: $LOCAL_ROOT"
date -Is

sync_dir "$REMOTE/data/data_center/views/vision_analysis/by_symbol/" \
         "$LOCAL_ROOT/data/data_center/views/vision_analysis/by_symbol/"

sync_dir "$REMOTE/data/data_center/views/vision_analysis/history/" \
         "$LOCAL_ROOT/data/data_center/views/vision_analysis/history/"

sync_dir "$REMOTE/data/deskpro/inputs/vision_context/coinglass/latest.json" \
         "$LOCAL_ROOT/data/deskpro/inputs/vision_context/coinglass/"

echo "OK sync done"
