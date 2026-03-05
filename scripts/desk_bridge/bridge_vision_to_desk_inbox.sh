#!/usr/bin/env bash
set -euo pipefail

# bridge_vision_to_desk_inbox.sh (FIXED heredoc)
#
# Takes newest ShareX screen_*.png from vision_processed/vision_inbox,
# crops 2x2 into 4 quadrants, drops into shared/inbox with symbol_tf_ts naming,
# then runs desk_snapshot_ingest ingest_once to refresh latest.json.

VISION_PROCESSED="${VISION_PROCESSED:-/srv/sftp/shared_files/shared/vision_processed}"
VISION_INBOX="${VISION_INBOX:-/srv/sftp/shared_files/shared/vision_inbox}"
DESK_INBOX="${DESK_INBOX:-/srv/sftp/shared_files/shared/inbox}"
TF="${TF:-H1}"

# 2x2 mapping (row-major): TL, TR, BL, BR
MAP0="${MAP0:-BTCUSDT.P}"
MAP1="${MAP1:-XAUUSD}"
MAP2="${MAP2:-SOLUSDT.P}"
MAP3="${MAP3:-ETHUSDT.P}"

need_cmd() { command -v "$1" >/dev/null 2>&1; }

pick_latest() {
  local f=""
  f="$(ls -1t "$VISION_PROCESSED"/screen_*.png 2>/dev/null | head -n 1 || true)"
  if [[ -z "$f" ]]; then
    f="$(ls -1t "$VISION_INBOX"/screen_*.png 2>/dev/null | head -n 1 || true)"
  fi
  echo "$f"
}

parse_ts_from_name() {
  # screen_2026-03-03_12-36-17_5.png -> 20260303_123617
  local bn="$1"
  local core
  core="$(echo "$bn" | sed -E 's/^screen_([0-9]{4})-([0-9]{2})-([0-9]{2})_([0-9]{2})-([0-9]{2})-([0-9]{2}).*/\1\2\3_\4\5\6/')" || true
  if [[ "$core" =~ ^[0-9]{8}_[0-9]{6}$ ]]; then
    echo "$core"
  else
    date +%Y%m%d_%H%M%S
  fi
}

crop_with_convert() {
  local src="$1" outdir="$2"
  convert "$src" -crop 2x2@ +repage +adjoin "$outdir/q_%d.png"
  [[ -f "$outdir/q_0.png" && -f "$outdir/q_1.png" && -f "$outdir/q_2.png" && -f "$outdir/q_3.png" ]]
}

crop_with_python() {
  local src="$1" outdir="$2"
  python3 - "$src" "$outdir" <<'PY'
from PIL import Image
import sys

src = sys.argv[1]
outdir = sys.argv[2]

im = Image.open(src)
w, h = im.size
hw, hh = w // 2, h // 2

boxes = [
    (0, 0, hw, hh),     # TL
    (hw, 0, w, hh),     # TR
    (0, hh, hw, h),     # BL
    (hw, hh, w, h),     # BR
]

for i, b in enumerate(boxes):
    im.crop(b).save(f"{outdir}/q_{i}.png")
PY
  [[ -f "$outdir/q_0.png" && -f "$outdir/q_1.png" && -f "$outdir/q_2.png" && -f "$outdir/q_3.png" ]]
}

ensure_dirs() {
  mkdir -p "$DESK_INBOX"
  mkdir -p "$DESK_INBOX/_processed" || true
}

main() {
  ensure_dirs

  local src
  src="$(pick_latest)"
  if [[ -z "$src" ]]; then
    echo "ERROR: no screen_*.png found in:"
    echo "  $VISION_PROCESSED"
    echo "  $VISION_INBOX"
    exit 2
  fi

  local bn ts work
  bn="$(basename "$src")"
  ts="$(parse_ts_from_name "$bn")"
  work="/tmp/desk_bridge_${ts}"
  rm -rf "$work"
  mkdir -p "$work"

  echo "Using source: $src"
  echo "Parsed ts: $ts"
  echo "Workdir: $work"
  echo

  local ok=0
  if need_cmd convert; then
    echo "Cropping with ImageMagick convert..."
    crop_with_convert "$src" "$work" && ok=1 || ok=0
  fi

  if [[ "$ok" -ne 1 ]]; then
    echo "convert not available or failed. Trying Python (PIL)..."
    python3 -c "import PIL" >/dev/null 2>&1 || {
      echo "ERROR: Pillow (PIL) not installed."
      echo "Fix: sudo apt-get update && sudo apt-get install -y python3-pil"
      exit 3
    }
    crop_with_python "$src" "$work" && ok=1 || ok=0
  fi

  if [[ "$ok" -ne 1 ]]; then
    echo "ERROR: could not crop into 4 quadrants."
    exit 4
  fi

  declare -a syms=("$MAP0" "$MAP1" "$MAP2" "$MAP3")
  for i in 0 1 2 3; do
    local sym out
    sym="${syms[$i]}"
    out="$DESK_INBOX/${sym}_${TF}_${ts}.png"
    cp -v "$work/q_${i}.png" "$out"
  done

  echo
  echo "Dropped 4 files into: $DESK_INBOX"
  ls -lt "$DESK_INBOX" | head -n 12 || true
  echo

  if need_cmd cmd-desk_snapshot_ingest; then
    echo "Running ingest_once..."
    cmd-desk_snapshot_ingest ingest_once
  else
    echo "Running ingest_once via module path..."
    /opt/trading/modules/desk_snapshot_ingest/scripts/cmd.sh ingest_once
  fi

  echo
  echo "OK: latest.json refreshed. Next: run Telegram /analyze (should no longer be STALE)."
}

main "$@"
