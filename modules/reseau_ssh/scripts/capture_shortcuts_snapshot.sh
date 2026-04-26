#!/usr/bin/env bash
set -euo pipefail

show_cmd() {
  local name="$1"
  if command -v "$name" >/dev/null 2>&1; then
    printf '%s=%s\n' "$name" "$(command -v "$name")"
  else
    printf '%s=%s\n' "$name" "MISSING"
  fi
}

show_link() {
  local path="$1"
  if [ -e "$path" ]; then
    if readlink -f "$path" >/dev/null 2>&1; then
      printf '%s -> %s\n' "$path" "$(readlink -f "$path")"
    else
      printf '%s -> %s\n' "$path" "UNRESOLVED"
    fi
  else
    printf '%s -> %s\n' "$path" "MISSING"
  fi
}

echo "=== reseau_ssh shortcut snapshot ==="
echo "host=$(hostname)"
echo "user=$(whoami)"
echo

show_cmd menu-reseau_ssh
show_cmd cmd-reseau_ssh
show_cmd sanity-reseau_ssh
show_cmd menu-reseau_ssh_step2
show_cmd cmd-reseau_ssh_step2
show_cmd sanity-reseau_ssh_step2

echo
show_link /usr/local/bin/menu-reseau_ssh
show_link /usr/local/bin/cmd-reseau_ssh
show_link /usr/local/bin/sanity-reseau_ssh
show_link /usr/local/bin/menu-reseau_ssh_step2
show_link /usr/local/bin/cmd-reseau_ssh_step2
show_link /usr/local/bin/sanity-reseau_ssh_step2

echo
show_link /opt/trading/scripts/reseau_ssh
show_link /opt/trading/modules/reseau_ssh
show_link /opt/trading/modules/reseau_ssh_step1b
