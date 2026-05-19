#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
MOD="${0%/*}/.."
MOD="$(cd "$MOD" && pwd -P)"
NAME="$(basename "$MOD")"

readme=""
for f in "$MOD/README.md" "$MOD/README.txt" "$MOD/README"; do
  [ -f "$f" ] && readme="$f" && break
done

echo
echo "=== MODULE MENU (wrapper) ==="
echo "name=$NAME"
echo "path=$MOD"
echo

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
