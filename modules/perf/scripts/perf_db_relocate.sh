#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MOD_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$MOD_DIR/../.." && pwd)"

LEGACY_DB="${LEGACY_DB:-$REPO_ROOT/perf/perf.db}"
CANONICAL_DB="${CANONICAL_DB:-$MOD_DIR/data/perf.db}"

show_status() {
  echo "legacy_db=$LEGACY_DB"
  echo "canonical_db=$CANONICAL_DB"
  [[ -f "$LEGACY_DB" ]] && echo "legacy_exists=1" || echo "legacy_exists=0"
  [[ -f "$CANONICAL_DB" ]] && echo "canonical_exists=1" || echo "canonical_exists=0"
  [[ -f "${LEGACY_DB}-wal" ]] && echo "legacy_wal=1" || echo "legacy_wal=0"
  [[ -f "${LEGACY_DB}-shm" ]] && echo "legacy_shm=1" || echo "legacy_shm=0"
}

copy_db() {
  if [[ ! -f "$LEGACY_DB" ]]; then
    echo "ERR: legacy DB not found: $LEGACY_DB" >&2
    exit 1
  fi

  mkdir -p "$(dirname "$CANONICAL_DB")"

  cp -a "$LEGACY_DB" "$CANONICAL_DB"
  [[ -f "${LEGACY_DB}-wal" ]] && cp -a "${LEGACY_DB}-wal" "${CANONICAL_DB}-wal"
  [[ -f "${LEGACY_DB}-shm" ]] && cp -a "${LEGACY_DB}-shm" "${CANONICAL_DB}-shm"

  echo "OK: copied PERF DB to canonical candidate location"
  echo "next_step: export PERF_DB_PATH=$CANONICAL_DB"
}

show_env() {
  echo "export PERF_DB_PATH=$CANONICAL_DB"
}

retire_legacy() {
  local ts retired
  ts="$(date +%Y%m%d_%H%M%S)"

  if [[ ! -f "$CANONICAL_DB" ]]; then
    echo "ERR: canonical DB not found: $CANONICAL_DB" >&2
    echo "     Run 'copy' first, then 'retire'." >&2
    exit 1
  fi

  if [[ ! -f "$LEGACY_DB" ]]; then
    echo "ERR: legacy DB not found: $LEGACY_DB" >&2
    exit 1
  fi

  retired="${LEGACY_DB}.retired_${ts}"
  mv "$LEGACY_DB" "$retired"
  [[ -f "${LEGACY_DB}-wal" ]] && mv "${LEGACY_DB}-wal" "${retired}-wal"
  [[ -f "${LEGACY_DB}-shm" ]] && mv "${LEGACY_DB}-shm" "${retired}-shm"

  echo "OK: legacy PERF DB retired: $retired"
  echo "canonical: $CANONICAL_DB"
  echo "rollback:  $(basename "$0") unretire"
}

unretire_legacy() {
  local latest_retired
  latest_retired="$(ls -1t "${LEGACY_DB}.retired_"* 2>/dev/null | head -1)" || true

  if [[ -z "$latest_retired" ]]; then
    echo "No retired legacy DB found matching: ${LEGACY_DB}.retired_*" >&2
    exit 1
  fi

  if [[ -f "$LEGACY_DB" ]]; then
    echo "WARN: legacy DB already present: $LEGACY_DB" >&2
    echo "      Skipping unretire to avoid overwrite." >&2
    exit 1
  fi

  mv "$latest_retired" "$LEGACY_DB"
  [[ -f "${latest_retired}-wal" ]] && mv "${latest_retired}-wal" "${LEGACY_DB}-wal"
  [[ -f "${latest_retired}-shm" ]] && mv "${latest_retired}-shm" "${LEGACY_DB}-shm"

  echo "OK: restored legacy PERF DB from $latest_retired"
}

usage() {
  cat <<EOF
Usage: $(basename "$0") {status|copy|retire|unretire|show-env}

status    Show current legacy/canonical DB state
copy      Copy legacy DB (+wal/+shm if present) to canonical candidate location
retire    Rename legacy DB to .retired_TIMESTAMP (requires canonical DB present)
unretire  Restore the most recently retired legacy DB
show-env  Print the PERF_DB_PATH export needed to activate the canonical DB path
EOF
}

case "${1:-}" in
  status) show_status ;;
  copy) copy_db ;;
  retire) retire_legacy ;;
  unretire) unretire_legacy ;;
  show-env) show_env ;;
  ""|-h|--help|help) usage ;;
  *) usage >&2; exit 1 ;;
esac
