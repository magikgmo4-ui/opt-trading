#!/usr/bin/env bash
# env_role_sync.sh — Sync /etc/opt-trading/env.d/roles/<role>.env to/from a remote machine via SSH.
# Usage:
#   scripts/env_role_sync.sh pull <machine> <role>   # import from remote
#   scripts/env_role_sync.sh push <machine> <role>   # export to remote
#   scripts/env_role_sync.sh list <machine>          # list deployed roles on remote
#   scripts/env_role_sync.sh diff <machine> <role>   # diff local vs remote (keys only, no values)
#
# Examples:
#   scripts/env_role_sync.sh pull fantome telegram_collector
#   scripts/env_role_sync.sh push fantome airtable_user
#   scripts/env_role_sync.sh list fantome
#
# Security:
#   - Values are NEVER displayed or logged.
#   - diff mode shows only key names, not values.
#   - Role files are written as chmod 600 root-owned.

set -euo pipefail

ROLES_DIR="/etc/opt-trading/env.d/roles"
CMD="${1:-}"
MACHINE="${2:-}"
ROLE="${3:-}"

usage() {
  echo "Usage: $0 pull|push|list|diff <machine> [role]"
  echo "  pull <machine> <role>   import role file from remote machine"
  echo "  push <machine> <role>   export role file to remote machine"
  echo "  list <machine>          list deployed role files on remote"
  echo "  diff <machine> <role>   compare key names (not values) local vs remote"
  exit 1
}

[[ -z "$CMD" || -z "$MACHINE" ]] && usage

case "$CMD" in
  pull)
    [[ -z "$ROLE" ]] && usage
    REMOTE_FILE="$ROLES_DIR/${ROLE}.env"
    echo "[env_role_sync] pull $ROLE from $MACHINE"
    sudo mkdir -p "$ROLES_DIR"
    ssh "$MACHINE" "cat $REMOTE_FILE" \
      | grep -E '^[A-Z][A-Z0-9_]*=' \
      | sudo tee "$ROLES_DIR/${ROLE}.env" > /dev/null
    sudo chmod 600 "$ROLES_DIR/${ROLE}.env"
    KEY_COUNT=$(sudo grep -c '^[A-Z]' "$ROLES_DIR/${ROLE}.env" 2>/dev/null || echo 0)
    echo "[env_role_sync] DONE — $KEY_COUNT keys written to $ROLES_DIR/${ROLE}.env"
    ;;

  push)
    [[ -z "$ROLE" ]] && usage
    LOCAL_FILE="$ROLES_DIR/${ROLE}.env"
    if ! sudo test -f "$LOCAL_FILE"; then
      echo "[env_role_sync] ERROR: $LOCAL_FILE not found locally" >&2
      exit 1
    fi
    echo "[env_role_sync] push $ROLE to $MACHINE"
    sudo cat "$LOCAL_FILE" \
      | grep -E '^[A-Z][A-Z0-9_]*=' \
      | ssh "$MACHINE" "sudo mkdir -p $ROLES_DIR && sudo tee $ROLES_DIR/${ROLE}.env > /dev/null && sudo chmod 600 $ROLES_DIR/${ROLE}.env"
    echo "[env_role_sync] DONE — pushed $ROLE to $MACHINE:$ROLES_DIR/${ROLE}.env"
    ;;

  list)
    echo "[env_role_sync] roles on $MACHINE:"
    ssh "$MACHINE" "ls $ROLES_DIR/*.env 2>/dev/null | xargs -I{} basename {} .env || echo '(none)'"
    ;;

  diff)
    [[ -z "$ROLE" ]] && usage
    LOCAL_FILE="$ROLES_DIR/${ROLE}.env"
    echo "[env_role_sync] diff $ROLE — local vs $MACHINE (keys only)"
    echo "--- local ---"
    sudo cat "$LOCAL_FILE" 2>/dev/null | grep -E '^[A-Z][A-Z0-9_]*=' | sed 's/=.*//' | sort || echo "(not found)"
    echo "--- $MACHINE ---"
    ssh "$MACHINE" "grep -E '^[A-Z][A-Z0-9_]*=' $ROLES_DIR/${ROLE}.env 2>/dev/null | sed 's/=.*//' | sort || echo '(not found)'"
    ;;

  *)
    usage
    ;;
esac
