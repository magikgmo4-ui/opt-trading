\
#!/usr/bin/env bash
set -euo pipefail
CMD="cmd-winscp_transfer"

echo "winscp_transfer — menu"
echo
select opt in "Init shared dirs (sudo)" "List inbox" "List outbox" "Send file to student" "Deploy zip on student" "Fetch remote file from student" "Status" "Quit"; do
  case "$REPLY" in
    1) sudo $CMD init; break;;
    2) $CMD ls inbox; break;;
    3) $CMD ls outbox; break;;
    4) read -r -p "Filename (in inbox or path): " f; $CMD send student "$f"; break;;
    5) read -r -p "Zip filename (in inbox/modules or path): " z; $CMD deploy student "$z"; break;;
    6) read -r -p "Remote path on student: " rp; $CMD fetch student "$rp"; break;;
    7) $CMD status; break;;
    8) break;;
    *) echo "Choix invalide";;
  esac
done
