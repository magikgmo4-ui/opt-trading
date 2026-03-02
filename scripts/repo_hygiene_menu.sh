#!/usr/bin/env bash
set -euo pipefail

while true; do
  cat <<'EOF'
=== Repo Hygiene Menu ===
1) Sanity check (fails on P0)
2) Scan report (non-failing)
3) Fix leading-backslash (DRY-RUN)
4) Fix leading-backslash (--apply)
5) Cleanup sqlite artifacts (DRY-RUN)
6) Cleanup sqlite artifacts (--apply)
q) Quit
EOF
  read -r -p "> " choice
  case "$choice" in
    1) cmd-repo_hygiene sanity ;;
    2) cmd-repo_hygiene scan ;;
    3) cmd-repo_hygiene fix-leading-backslash ;;
    4) cmd-repo_hygiene fix-leading-backslash --apply ;;
    5) cmd-repo_hygiene cleanup-artifacts ;;
    6) cmd-repo_hygiene cleanup-artifacts --apply ;;
    q|Q) exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
  echo
done
