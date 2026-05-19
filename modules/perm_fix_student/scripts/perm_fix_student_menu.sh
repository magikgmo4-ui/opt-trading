\
#!/usr/bin/env bash
set -euo pipefail

CMD="cmd-perm_fix_student"

echo "perm_fix_student — menu"
echo
select opt in "Fix journal perms" "Fix ALL /opt/trading perms (optional)" "Test Ollama + API" "Status" "Quit"; do
  case "$REPLY" in
    1) sudo $CMD fix_journal; break;;
    2) sudo $CMD fix_all; break;;
    3) $CMD ollama_test; break;;
    4) $CMD status; break;;
    5) break;;
    *) echo "Choix invalide";;
  esac
done
