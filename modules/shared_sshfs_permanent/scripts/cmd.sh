#!/usr/bin/env bash
set -euo pipefail

SCRIPT="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT="$(readlink -f "$SCRIPT" 2>/dev/null || echo "$SCRIPT")"
fi
MOD="$(cd "$(dirname "$SCRIPT")/.." && pwd -P)"
NAME="$(basename "$MOD")"

if [[ "$(basename "$0")" == "cmd-shared_sshfs_permanent" && -x "/opt/trading/scripts/shared_sshfs_permanent_cmd.sh" ]]; then
  exec bash "/opt/trading/scripts/shared_sshfs_permanent_cmd.sh" "$@"
fi

cmd="${1:-help}"
case "$cmd" in
  info) echo "name=$NAME"; echo "path=$MOD";;
  readme)
    for f in "$MOD/README.md" "$MOD/README.txt" "$MOD/README"; do
      [ -f "$f" ] && sed -n '1,220p' "$f" && exit 0
    done
    echo "(no README found)"
    ;;
  ls)
    (cd "$MOD" && find . -maxdepth 2 -type f | sed 's#^\./##' | sort) | sed -n '1,200p'
    ;;
  grep)
    (cd "$MOD" && \
      grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ -E "if __name__ == '__main__'|typer|click|argparse" . \
      | head -n 120) || true
    ;;
  menu) exec bash "$MOD/scripts/menu.sh";;
  *)
    echo "Usage: cmd-$NAME info|readme|ls|grep|menu"
    exit 1
    ;;
esac
