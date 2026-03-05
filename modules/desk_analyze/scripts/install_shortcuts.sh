#!/usr/bin/env bash
set -euo pipefail
SCRIPT="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT="$(readlink -f "$SCRIPT" 2>/dev/null || echo "$SCRIPT")"
fi
BASE="$(cd "$(dirname "$SCRIPT")/.." && pwd)"

ln -sf "$BASE/scripts/menu.sh" /usr/local/bin/menu-desk_analyze
ln -sf "$BASE/scripts/cmd.sh" /usr/local/bin/cmd-desk_analyze
ln -sf "$BASE/scripts/sanity_check.sh" /usr/local/bin/sanity-desk_analyze

echo "OK: installed shortcuts:"
ls -lah /usr/local/bin/menu-desk_analyze /usr/local/bin/cmd-desk_analyze /usr/local/bin/sanity-desk_analyze
