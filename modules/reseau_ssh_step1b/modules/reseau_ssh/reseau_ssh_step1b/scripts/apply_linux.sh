#!/usr/bin/env bash
set -euo pipefail

APPLY="${1:-}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOSTS_BLOCK="$ROOT_DIR/templates/hosts.block"
SSH_CFG_SRC="$ROOT_DIR/templates/ssh_config.linux"

usage() {
  cat <<EOF
Usage:
  $(basename "$0")            # dry-run (shows what would change)
  $(basename "$0") --apply    # applies changes (requires sudo)

Actions:
- Update /etc/hosts with managed reseau_ssh block
- Install ~/.ssh/config (canonical aliases)
- Fix permissions (~/.ssh 700, config 600)
EOF
}

if [[ "$APPLY" == "-h" || "$APPLY" == "--help" ]]; then
  usage; exit 0
fi

mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"

echo "=== reseau_ssh apply_linux ==="
date -Is
echo "[whoami] $(whoami) @ $(hostname)"
echo "[mode] ${APPLY:-dry-run}"
echo

if [[ "$APPLY" != "--apply" ]]; then
  echo "DRY-RUN ONLY."
  echo "Would install: $SSH_CFG_SRC -> $HOME/.ssh/config"
  echo "Would update:  /etc/hosts (managed block from $HOSTS_BLOCK)"
  echo "Run with --apply to make changes."
  exit 0
fi

CFG="$HOME/.ssh/config"
if [[ -f "$CFG" ]]; then
  cp -a "$CFG" "$CFG.bak.$(date +%F_%H%M%S)"
fi
cp -a "$SSH_CFG_SRC" "$CFG"
chmod 600 "$CFG"

TMP="$(mktemp)"
sudo cp -a /etc/hosts "/etc/hosts.bak.reseau_ssh.$(date +%F_%H%M%S)"

sudo awk '
  BEGIN{inblk=0}
  /^# === reseau_ssh BEGIN ===/{inblk=1; next}
  /^# === reseau_ssh END ===/{inblk=0; next}
  { if(!inblk) print $0 }
' /etc/hosts > "$TMP"

printf "\n" >> "$TMP"
cat "$HOSTS_BLOCK" >> "$TMP"
sudo cp "$TMP" /etc/hosts
rm -f "$TMP"

echo "OK: applied ~/.ssh/config and /etc/hosts"
