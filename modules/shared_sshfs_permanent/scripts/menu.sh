#!/usr/bin/env bash
set -euo pipefail

SCRIPT="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT="$(readlink -f "$SCRIPT" 2>/dev/null || echo "$SCRIPT")"
fi
MOD="$(cd "$(dirname "$SCRIPT")/.." && pwd -P)"
NAME="$(basename "$MOD")"

if [[ "$(basename "$0")" == "menu-shared_sshfs_permanent" && -x "/opt/trading/scripts/shared_sshfs_permanent_menu.sh" ]]; then
  exec bash "/opt/trading/scripts/shared_sshfs_permanent_menu.sh"
fi

# WRAPPER MARKER (used by ops_wrappers)
echo
echo "=== MODULE MENU (wrapper) ==="
echo "name=$NAME"
echo "path=$MOD"
echo

readme=""
for f in "$MOD/README.md" "$MOD/README.txt" "$MOD/README"; do
  [ -f "$f" ] && readme="$f" && break
done

while true; do
  echo "1) Show README"
  echo "2) List files (maxdepth=2)"
  echo "3) Grep entrypoints (python __main__/click/typer/argparse)"
  echo "4) Git status (module only)"
  echo "5) Open a shell in module dir"
  echo "q) Quit"
  read -r -p "> " ans
  case "$ans" in
    1)
      if [ -n "$readme" ]; then
        sed -n '1,220p' "$readme" || true
      else
        echo "(no README found)"
      fi
      ;;
    2)
      (cd "$MOD" && find . -maxdepth 2 -type f | sed 's#^\./##' | sort) | sed -n '1,200p'
      ;;
    3)
      (cd "$MOD" && \
        grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ -E "if __name__ == '__main__'|typer|click|argparse" . \
        | head -n 120) || true
      ;;
    4)
      ROOT="/opt/trading"
      if [ -d "$ROOT/.git" ]; then
        (cd "$ROOT" && git status -sb -- "$MOD" 2>/dev/null) || true
      else
        echo "(no git repo at $ROOT)"
      fi
      ;;
    5)
      echo "Entering: $MOD"
      cd "$MOD"
      exec bash
      ;;
    q|Q) exit 0;;
    *) echo "?";;
  esac
done
