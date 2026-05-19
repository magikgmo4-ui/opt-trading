#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

while true; do
  cat <<'EOF'
=== Repo Ownership Guard Menu ===
1) Sanity scan (read-only)
2) Fix (dry-run)
3) Fix (apply)
q) Quit
EOF
  read -r -p "> " c
  case "$c" in
    1) bash "$ROOT_DIR/scripts/repo_ownership_guard_cmd.sh" sanity ;;
    2) bash "$ROOT_DIR/scripts/repo_ownership_guard_cmd.sh" fix --dry-run ;;
    3) bash "$ROOT_DIR/scripts/repo_ownership_guard_cmd.sh" fix ;;
    q|Q) exit 0 ;;
    *) echo "invalid" ;;
  esac
done
