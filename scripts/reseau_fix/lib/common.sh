#!/usr/bin/env bash
set -euo pipefail

ts() { date +%Y%m%d_%H%M%S; }

need_root() {
  if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
    echo "ERROR: run as root (sudo)." >&2
    exit 1
  fi
}

backup_file() {
  local f="$1"
  if [[ -f "$f" ]]; then
    cp -a "$f" "$f.bak.$(ts)"
  fi
}

svc_ssh_name() {
  if systemctl list-unit-files | awk '{print $1}' | grep -qx 'ssh.service'; then
    echo "ssh"
  else
    echo "sshd"
  fi
}

restart_ssh() {
  local s
  s="$(svc_ssh_name)"
  systemctl restart "$s"
}

ufw_has() {
  local pat="$1"
  ufw status verbose 2>/dev/null | grep -Fq "$pat"
}

ufw_allow_rule() {
  # args are the ufw command tail (without 'ufw')
  # example: "allow from 192.168.16.0/24 to any port 22 proto tcp"
  ufw "$@" >/dev/null 2>&1 || true
}

ufw_delete_if_present() {
  # best-effort delete: "ufw delete allow 51820/udp"
  local rule="$*"
  if ufw status 2>/dev/null | grep -Fq "$(echo "$rule" | sed 's/^allow //')"; then
    yes y | ufw delete $rule >/dev/null 2>&1 || true
  fi
}

write_hosts_block() {
  local block_file="$1"
  local hosts="/etc/hosts"
  backup_file "$hosts"
  if grep -q '^# BEGIN RESEAU_SSH MANAGED' "$hosts"; then
    # replace existing block
    awk -v bf="$block_file" '
      BEGIN{inblk=0}
      /^# BEGIN RESEAU_SSH MANAGED/{inblk=1; system("cat " bf); next}
      /^# END RESEAU_SSH MANAGED/{inblk=0; next}
      inblk==0{print}
    ' "$hosts" > "${hosts}.tmp"
    mv "${hosts}.tmp" "$hosts"
  else
    printf "\n%s\n" "$(cat "$block_file")" >> "$hosts"
  fi
}

nonempty_file() { [[ -s "$1" ]]; }
