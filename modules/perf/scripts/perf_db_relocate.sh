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

usage() {
  cat <<EOF
Usage: $(basename "$0") {status|copy|show-env}

status    Show current legacy/canonical DB state
copy      Copy legacy DB (+wal/+shm if present) to canonical candidate location
show-env  Print the PERF_DB_PATH export needed to activate the canonical DB path
EOF
}

case "${1:-}" in
  status) show_status ;;
  copy) copy_db ;;
  show-env) show_env ;;
  ""|-h|--help|help) usage ;;
  *) usage >&2; exit 1 ;;
esac
