\
#!/usr/bin/env bash
set -euo pipefail
DROP="/opt/trading/drop"
ARCH="/opt/trading/archive"
JSON="/opt/trading/journal/events/events.jsonl"
mkdir -p "$DROP" "$ARCH"

inotifywait -m -e close_write,moved_to --format '%w%f' "$DROP" | while read -r f; do
  TS="$(date -Is)"
  DAY="$(date +%F)"
  mkdir -p "$ARCH/$DAY"
  BN="$(basename "$f")"
  DEST="$ARCH/$DAY/$BN"
  mv "$f" "$DEST"
  SHA="$(sha256sum "$DEST" | awk '{print $1}')"
  printf '{"ts":"%s","host":"%s","type":"artifact","title":"drop","path":"%s","sha256":"%s"}\n' \
    "$TS" "$(hostname)" "$DEST" "$SHA" >> "$JSON"
  echo "Archived: $DEST"
done
