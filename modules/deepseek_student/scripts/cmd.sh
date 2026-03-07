#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cmd="${1:-help}"

case "$cmd" in
  roadmap|pull|test|sanity)
    # Dispatch to the real implementation script in the same directory
    exec bash "$SCRIPT_DIR/deepseek_student_cmd.sh" "$@"
    ;;

  info) echo "name=deepseek_student"; echo "path=$SCRIPT_DIR/..";;
  readme)
    MOD="$SCRIPT_DIR/.."
    for f in "$MOD/README.md" "$MOD/README.txt" "$MOD/README"; do
      [ -f "$f" ] && sed -n '1,220p' "$f" && exit 0
    done
    echo "(no README found)"
    ;;
  ls)
    MOD="$SCRIPT_DIR/.."
    (cd "$MOD" && find . -maxdepth 2 -type f | sed 's#^\./##' | sort) | sed -n '1,200p'
    ;;
  grep)
    MOD="$SCRIPT_DIR/.."
    (cd "$MOD" && \
      grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ -E "if __name__ == '__main__'|typer|click|argparse" . \
      | head -n 120) || true
    ;;
  menu) exec bash "$SCRIPT_DIR/menu.sh";;
  *)
    echo "Usage: cmd-deepseek_student {roadmap|pull|test|sanity|info|readme|ls|grep|menu}"
    exit 1
    ;;
esac
