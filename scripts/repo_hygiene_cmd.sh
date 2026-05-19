#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/modules/repo_hygiene/repo_hygiene_lib.sh"

usage() {
  cat <<'EOF'
cmd-repo_hygiene <command>

Commands:
  sanity                           Run repo hygiene sanity checks
  scan                             Run all scans (non-failing report)
  fix-leading-backslash [--apply]  Remove first '\' line (after review)
  cleanup-artifacts [--apply]      Remove *.db-wal/shm, *.sqlite-wal/shm (after review)
EOF
}

cmd_sanity() {
  bash "$ROOT/modules/repo_hygiene/sanity_check.sh"
}

cmd_scan() {
  rh_banner
  echo "[root] $ROOT"
  echo

  echo "[leading-backslash]"
  rh_find_leading_backslash "$ROOT" || true
  echo

  echo "[sqlite artifacts]"
  rh_find_sqlite_artifacts "$ROOT" || true
  echo

  echo "[*.bak_*]"
  rh_find_bak_underscore "$ROOT" || true
  echo

  echo "[student legacy recursion]"
  if rh_detect_student_legacy_loop "$ROOT"; then
    echo "(detected)"
  else
    echo "(none)"
  fi
}

cmd_fix_leading_backslash() {
  rh_fix_leading_backslash "$ROOT" "${1:-}"
}

cmd_cleanup_artifacts() {
  local apply="${1:-}"
  local art
  art="$(rh_find_sqlite_artifacts "$ROOT" || true)"
  if [[ -z "$art" ]]; then
    echo "OK: no sqlite artifacts found."
    return 0
  fi
  echo "FOUND sqlite artifacts:"
  echo "$art"
  echo
  if [[ "$apply" != "--apply" ]]; then
    echo "DRY-RUN: pass --apply to delete these files."
    return 0
  fi
  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    rm -f "$ROOT/$rel"
    echo "DELETED $rel"
  done <<<"$art"
}

main() {
  local c="${1:-}"
  shift || true
  case "$c" in
    sanity) cmd_sanity "$@" ;;
    scan) cmd_scan "$@" ;;
    fix-leading-backslash) cmd_fix_leading_backslash "$@" ;;
    cleanup-artifacts) cmd_cleanup_artifacts "$@" ;;
    ""|-h|--help|help) usage ;;
    *) echo "Unknown command: $c" ; usage ; exit 1 ;;
  esac
}

main "$@"
