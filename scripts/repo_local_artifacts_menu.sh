#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

while true; do
  cat <<'EOF'
=== Repo Local Artifacts Menu ===
1) Apply .gitignore additions
2) Sanity check
q) Quit
EOF
  read -r -p "> " c
  case "$c" in
    1) bash "$ROOT_DIR/scripts/repo_local_artifacts_cmd.sh" apply ;;
    2) bash "$ROOT_DIR/scripts/repo_local_artifacts_cmd.sh" sanity ;;
    q|Q) exit 0 ;;
    *) echo "invalid" ;;
  esac
done
