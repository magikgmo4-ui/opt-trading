#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/opt/trading}"
TS="$(TZ=America/Montreal date +%Y%m%d_%H%M%S)"
BKDIR="$ROOT/_student_archive/workflow/patch_backups/deepseek_hub_$TS"

echo "== deepseek_hub: apply patches =="
echo "ROOT:  $ROOT"
echo "BACKUP:$BKDIR"
mkdir -p "$BKDIR"

src_th="$ROOT/modules/deepseek_hub/patches/deepseek_thinking_cmd.sh"
src_rs="$ROOT/modules/deepseek_hub/patches/deepseek_response_cmd.sh"

dst_th="$ROOT/modules/deepseek_thinking/scripts/deepseek_thinking_cmd.sh"
dst_rs="$ROOT/modules/deepseek_response/scripts/deepseek_response_cmd.sh"

if [ ! -f "$src_th" ] || [ ! -f "$src_rs" ]; then
  echo "ERROR: patch sources missing under modules/deepseek_hub/patches/"
  exit 1
fi

# backup originals (if exist)
if [ -f "$dst_th" ]; then cp -a "$dst_th" "$BKDIR/"; fi
if [ -f "$dst_rs" ]; then cp -a "$dst_rs" "$BKDIR/"; fi

# apply
install -m 0755 "$src_th" "$dst_th"
install -m 0755 "$src_rs" "$dst_rs"

echo "Patched:"
echo " - $dst_th"
echo " - $dst_rs"
echo "Backup:"
echo " - $BKDIR"
