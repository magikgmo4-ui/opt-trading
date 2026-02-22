#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root robustly, with minimal user input.
# Priority:
# 1) REPO_ROOT env
# 2) git toplevel from current directory or script directory
# 3) walk up from script directory to find modules/desk_pro
# 4) common paths

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -n "${REPO_ROOT:-}" && -d "${REPO_ROOT}" ]]; then
  echo "$REPO_ROOT"
  exit 0
fi

try_git() {
  local dir="$1"
  (cd "$dir" && git rev-parse --show-toplevel 2>/dev/null) || true
}

root="$(try_git "$PWD")"
[[ -n "$root" ]] && { echo "$root"; exit 0; }

root="$(try_git "$SCRIPT_DIR")"
[[ -n "$root" ]] && { echo "$root"; exit 0; }

# Walk up from script dir
d="$SCRIPT_DIR"
for _ in {1..8}; do
  if [[ -d "$d/modules/desk_pro" ]]; then
    echo "$d"
    exit 0
  fi
  d="$(dirname "$d")"
done

# Common locations
candidates=(
  "$HOME/admin-trading"
  "$HOME/dev/admin-trading"
  "/opt/trading"
  "/opt/admin-trading"
  "$HOME"
)
for c in "${candidates[@]}"; do
  [[ -d "$c/modules/desk_pro" ]] && { echo "$c"; exit 0; }
done

echo "FAIL"
exit 2
