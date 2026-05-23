#!/usr/bin/env bash
set -euo pipefail

RESEAU_SSH_ENTRY_SOURCE="${BASH_SOURCE[0]}"
RESEAU_SSH_SOURCE_PATH="${BASH_SOURCE[0]}"
while [ -L "$RESEAU_SSH_SOURCE_PATH" ]; do
  RESEAU_SSH_SOURCE_DIR="$(cd "$(dirname "$RESEAU_SSH_SOURCE_PATH")" && pwd -P)"
  RESEAU_SSH_SOURCE_PATH="$(readlink "$RESEAU_SSH_SOURCE_PATH")"
  case "$RESEAU_SSH_SOURCE_PATH" in
    /*) ;;
    *) RESEAU_SSH_SOURCE_PATH="$RESEAU_SSH_SOURCE_DIR/$RESEAU_SSH_SOURCE_PATH" ;;
  esac
done
RESEAU_SSH_SOURCE_DIR="$(cd "$(dirname "$RESEAU_SSH_SOURCE_PATH")" && pwd -P)"
# shellcheck source=./_reseau_ssh_common.sh
source "$RESEAU_SSH_SOURCE_DIR/_reseau_ssh_common.sh"

CMD="$RESEAU_SSH_TOP_CMD"

while true; do
  echo
  echo "=== reseau_ssh — canonical facade ==="
  echo "name=$RESEAU_SSH_CANONICAL_NAME"
  echo "module_root=$RESEAU_SSH_MODULE_DIR"
  echo
  echo "1) Sanity (canonical facade)"
  echo "2) Bootstrap (packages + UFW + Fail2Ban) [SAFE]"
  echo "3) SSH hardening SAFE (drop-in)"
  echo "4) SSH lockdown (disable password auth)"
  echo "5) WireGuard / firewall menu (step2 implementation)"
  echo "6) Baseline dry-run"
  echo "7) Baseline apply"
  echo "8) Baseline hostname"
  echo "9) Baseline sanity"
  echo "a) Show baseline hosts template"
  echo "b) Show baseline ssh template"
  echo "i) Show path info"
  echo "r) Show README"
  echo "q) Quit"
  read -r -p "> " ans
  case "$ans" in
    1) bash "$CMD" sanity ;;
    2) sudo bash "$CMD" bootstrap ;;
    3) sudo bash "$CMD" ssh-hardening-safe ;;
    4) sudo bash "$CMD" ssh-lockdown ;;
    5)
      reseau_ssh_require_exec "$RESEAU_SSH_IMPL_MENU"
      bash "$RESEAU_SSH_IMPL_MENU"
      ;;
    6) bash "$CMD" baseline-dry-run ;;
    7) bash "$CMD" baseline-apply ;;
    8)
      read -r -p "Target hostname: " hn
      bash "$CMD" baseline-hostname "$hn"
      ;;
    9) bash "$CMD" baseline-sanity ;;
    a|A) bash "$CMD" baseline-show-hosts ;;
    b|B) bash "$CMD" baseline-show-ssh ;;
    i|I) bash "$CMD" info ;;
    r|R) bash "$CMD" readme ;;
    q|Q) exit 0 ;;
    *) echo "?" ;;
  esac
done
