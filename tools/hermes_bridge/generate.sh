#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="$BASE_DIR/prompt.txt"
OUTPUT_DIR="$BASE_DIR/output"
LOG_DIR="$BASE_DIR/logs"

mkdir -p "$OUTPUT_DIR" "$LOG_DIR"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
OUT_FILE="$OUTPUT_DIR/generated_${TIMESTAMP}.sh"
LOG_FILE="$LOG_DIR/generate_${TIMESTAMP}.log"

if ! command -v hermes >/dev/null 2>&1; then
  echo "[ERR] hermes introuvable dans le PATH" >&2
  exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
  echo "[ERR] prompt introuvable: $PROMPT_FILE" >&2
  exit 1
fi

echo "[INFO] generation via Hermes"
hermes chat < "$PROMPT_FILE" > "$OUT_FILE" 2> "$LOG_FILE"
chmod +x "$OUT_FILE"

echo "[OK] script genere: $OUT_FILE"
echo "[INFO] log: $LOG_FILE"
