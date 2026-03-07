#!/usr/bin/env bash
set -euo pipefail
MOD="${0%/*}/.."
MOD="$(cd "$MOD" && pwd -P)"
NAME="$(basename "$MOD")"

# If called as cmd-deepseek_thinking via symlink, or directly
cmd="${1:-help}"

case "$cmd" in
  run|tail|roadmap_module)
    # Dispatch to the real implementation script
    # Shift so that $2 becomes $1 for the target script, etc.
    # But wait, deepseek_thinking_cmd.sh expects: CMD [MODEL] [ARG1] [ARG2]
    # Here $1 is CMD. So we just pass all args.
    exec bash "$MOD/scripts/deepseek_thinking_cmd.sh" "$@"
    ;;

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
    # Show usage for both generic and specific commands
    echo "Usage: cmd-$NAME {run|tail|roadmap_module|info|readme|ls|grep|menu}"
    exit 1
    ;;
esac
