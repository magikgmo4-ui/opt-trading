\
    #!/usr/bin/env bash
    set -euo pipefail

    ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
    CMD="$ROOT/modules/install_module/scripts/cmd.sh"

    prompt() { read -r -p "$1" ans; echo "$ans"; }

    while true; do
      echo
      echo "=== INSTALL MODULE ==="
      echo "root=$ROOT"
      echo
      echo "1) List packages in /shared"
      echo "2) Sync/Validate (git push + pull on student/db-layer)"
      echo "q) Quit"
      echo -n "> "
      read -r choice || exit 0

      case "$choice" in
        1)
          echo
          echo "--- packages ---"
          "$CMD" list || true
          ;;
        2)
          echo
          hosts="$(prompt "Hosts (default: student db-layer): ")"
          commit="$(prompt "Auto-commit message (empty = do NOT auto-commit): ")"
          if [ -z "$hosts" ]; then hosts="student db-layer"; fi
          if [ -n "$commit" ]; then
            "$CMD" sync_validate --hosts "$hosts" --auto-commit --commit "$commit"
          else
            "$CMD" sync_validate --hosts "$hosts"
          fi
          ;;
        q|Q) exit 0;;
        *) echo "Invalid.";;
      esac
    done
