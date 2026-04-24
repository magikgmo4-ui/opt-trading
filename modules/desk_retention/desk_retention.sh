#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
CFG="$BASE_DIR/config/desk_retention.env"

# defaults
KEEP_DAYS="${KEEP_DAYS:-7}"
PRUNE_EMPTY_DIRS="${PRUNE_EMPTY_DIRS:-1}"
PRUNE_PATHS="${PRUNE_PATHS:-/opt/trading/desk/snapshots}"
EXCLUDE_REGEX="${EXCLUDE_REGEX:-latest\.json$|history\.jsonl$|\.keep$}"
LOG_DIR="${LOG_DIR:-/opt/trading/tmp/logs}"

if [ -f "$CFG" ]; then
  # shellcheck disable=SC1090
  source "$CFG"
fi

mkdir -p "$LOG_DIR" || true
NOW="$(date +%Y%m%d_%H%M%S)"
LOG="$LOG_DIR/desk_retention_${NOW}.log"

DRY_RUN="${1:-0}"  # 1 = dry run

echo "=== desk_retention ===" | tee -a "$LOG"
echo "ts: $(date -Iseconds)" | tee -a "$LOG"
echo "KEEP_DAYS=$KEEP_DAYS DRY_RUN=$DRY_RUN" | tee -a "$LOG"
echo "PRUNE_EMPTY_DIRS=$PRUNE_EMPTY_DIRS" | tee -a "$LOG"
echo "EXCLUDE_REGEX=$EXCLUDE_REGEX" | tee -a "$LOG"
echo "PRUNE_PATHS=$PRUNE_PATHS" | tee -a "$LOG"
echo | tee -a "$LOG"

deleted=0
candidates=0

for P in $PRUNE_PATHS; do
  if [ ! -d "$P" ]; then
    echo "SKIP: not a dir: $P" | tee -a "$LOG"
    continue
  fi

  echo "--- PATH: $P ---" | tee -a "$LOG"
  mapfile -t files < <(find "$P" -type f -mtime "+$KEEP_DAYS" 2>/dev/null | grep -Ev "$EXCLUDE_REGEX" || true)
  n="${#files[@]}"
  candidates=$((candidates + n))
  echo "candidates: $n" | tee -a "$LOG"

  if [ "$n" -gt 0 ]; then
    if [ "$DRY_RUN" = "1" ]; then
      printf "%s\n" "${files[@]}" | sed 's/^/DRY_DELETE: /' | tee -a "$LOG"
    else
      for f in "${files[@]}"; do
        rm -f -- "$f" && deleted=$((deleted+1)) || true
      done
      echo "deleted: $n" | tee -a "$LOG"
    fi
  fi

  if [ "$PRUNE_EMPTY_DIRS" = "1" ]; then
    if [ "$DRY_RUN" = "1" ]; then
      find "$P" -type d -empty 2>/dev/null | sed 's/^/DRY_RMDIR: /' | tee -a "$LOG" || true
    else
      find "$P" -type d -empty -delete 2>/dev/null || true
    fi
  fi
done

echo | tee -a "$LOG"
echo "SUMMARY: candidates=$candidates deleted=$deleted dry_run=$DRY_RUN" | tee -a "$LOG"
echo "LOG: $LOG" | tee -a "$LOG"

if [ "$DRY_RUN" = "1" ]; then
  echo "{"ok":true,"dry_run":true,"candidates":$candidates,"deleted":0,"log":"$LOG"}"
else
  echo "{"ok":true,"dry_run":false,"candidates":$candidates,"deleted":$deleted,"log":"$LOG"}"
fi
