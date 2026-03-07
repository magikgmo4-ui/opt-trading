#!/usr/bin/env bash
set -euo pipefail

# Resolve symlink to find the real directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

# If called as cmd-deepseek_thinking via symlink, or directly
cmd="${1:-help}"

case "$cmd" in
  run|tail|roadmap_module)
    # Dispatch to the real implementation script in the same directory
    exec bash "$SCRIPT_DIR/deepseek_thinking_cmd.sh" "$@"
    ;;

  info) echo "name=deepseek_thinking"; echo "path=$SCRIPT_DIR/..";;
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
    # Show usage for both generic and specific commands
    echo "Usage: cmd-deepseek_thinking {run|tail|roadmap_module|info|readme|ls|grep|menu}"
    exit 1
    ;;
esac
