#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cmd="${1:-help}"; shift || true

source "$ROOT_DIR/modules/repo_local_artifacts/repo_local_artifacts_lib.sh"

usage() {
  cat <<'EOF'
repo_local_artifacts_cmd

Usage:
  bash scripts/repo_local_artifacts_cmd.sh apply
  bash scripts/repo_local_artifacts_cmd.sh sanity
EOF
}

apply() {
  ensure_git_root
  append_unique_lines "$ROOT_DIR/modules/repo_local_artifacts/gitignore_additions.txt" "$ROOT_DIR/.gitignore"
  echo "OK: updated .gitignore (idempotent)"
}

sanity() {
  ensure_git_root
  bash "$ROOT_DIR/modules/repo_local_artifacts/sanity_check.sh"
}

case "$cmd" in
  apply) apply ;;
  sanity) sanity ;;
  help|-h|--help) usage ;;
  *) usage; exit 2 ;;
esac
