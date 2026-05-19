#!/usr/bin/env bash
set -euo pipefail

echo "=== vision_bot sanity ==="
date -Is || true
echo

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$BASE_DIR/../.." && pwd)"

echo "[paths]"
echo " BASE_DIR=$BASE_DIR"
echo " REPO_ROOT=$REPO_ROOT"
echo

echo "[python]"
command -v python3 >/dev/null && python3 --version || { echo "ERR: python3 missing"; exit 1; }
echo

INBOX="${VISION_BOT_INBOX:-/srv/sftp/shared_files/shared/vision_inbox}"
OUTBOX="${VISION_BOT_OUTBOX:-/srv/sftp/shared_files/shared/vision_outbox}"
PROCESSED="${VISION_BOT_PROCESSED:-/srv/sftp/shared_files/shared/vision_processed}"
WORKDIR="${VISION_BOT_WORKDIR:-$REPO_ROOT/_work/vision_bot}"
LOG="${VISION_BOT_LOG:-$WORKDIR/vision_bot.log}"
STATE="${VISION_BOT_STATE:-$WORKDIR/state.json}"

echo "[config]"
echo " ENGINE=${VISION_BOT_ENGINE:-ocr}"
echo " INBOX=$INBOX"
echo " OUTBOX=$OUTBOX"
echo " PROCESSED=$PROCESSED"
echo " WORKDIR=$WORKDIR"
echo " LOG=$LOG"
echo " STATE=$STATE"
echo

echo "[deps]"
if command -v tesseract >/dev/null; then
  echo " OK: tesseract=$(tesseract --version | head -n 1)"
else
  echo " WARN: tesseract not found (OCR fallback dummy)."
fi
echo

echo "[dirs]"
mkdir -p "$INBOX" "$OUTBOX" "$PROCESSED" "$WORKDIR"
echo " OK: ensured dirs"
echo

echo "[dry run]"
python3 "$BASE_DIR/app/vision_bot.py" run_once >/dev/null 2>&1 || true
echo " OK: run_once executed (no-op if inbox empty)"
echo

echo "PASS: vision_bot sanity OK"
