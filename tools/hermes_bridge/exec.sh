#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$BASE_DIR/output"
LOG_DIR="$BASE_DIR/logs"

mkdir -p "$LOG_DIR"

LATEST_SCRIPT=$(ls -t "$OUTPUT_DIR"/*.sh 2>/dev/null | head -n 1 || true)

if [ -z "$LATEST_SCRIPT" ]; then
  echo "[ERR] aucun script genere" >&2
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/exec_${TIMESTAMP}.log"

echo "[INFO] execution: $LATEST_SCRIPT"
bash "$LATEST_SCRIPT" > "$LOG_FILE" 2>&1

echo "[OK] execution terminee"
echo "[INFO] log: $LOG_FILE"
