#!/usr/bin/env bash
set -euo pipefail

ts() { date -Is; }

log() { echo "[$(ts)] $*"; }

need_root() {
  if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
    echo "ERROR: run as root (sudo)." >&2
    exit 1
  fi
}

backup_file() {
  local f="$1"
  if [[ -f "$f" ]]; then
    mkdir -p /var/backups/reseau_ssh
    local b="/var/backups/reseau_ssh/$(basename "$f").$(date +%Y%m%d_%H%M%S).bak"
    cp -a "$f" "$b"
    log "backup: $f -> $b"
  fi
}

detect_lan_cidr() {
  # best-effort: pick first non-lo interface IPv4 and assume /24 if unknown
  local ip
  ip="$(ip -4 -o addr show scope global | awk '{print $4}' | head -n1 || true)"
  if [[ -n "$ip" ]]; then
    echo "$ip" | awk -F'/' '{print $1"/"$2}'
  else
    echo "192.168.16.0/24"
  fi
}

ufw_allow_from_cidr() {
  local cidr="$1"
  local port="$2"
  local proto="${3:-tcp}"
  ufw allow from "$cidr" to any port "$port" proto "$proto" >/dev/null
}

is_debian_like() {
  [[ -f /etc/debian_version ]]
}
