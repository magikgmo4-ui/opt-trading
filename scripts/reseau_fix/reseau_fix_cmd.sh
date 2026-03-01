#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/scripts/reseau_fix"
# shellcheck source=/dev/null
source "$BASE/lib/common.sh"

LAN_CIDR="192.168.16.0/24"
WG_MGMT_CIDR="10.66.66.0/24"

usage() {
  cat <<'USAGE'
cmd-reseau_fix <command>

Commands:
  status                 Show quick status (ip/ufw/wg/sshd)
  apply-safe             Apply SAFE baseline: /etc/hosts + sshd safe drop-in + UFW baseline
  apply-lockdown         Disable SSH password auth (requires authorized_keys non-empty for main user)
  disable-dblayer-wg0    Disable wg0 on db-layer to avoid overlap/confusion (optional)
USAGE
}

status() {
  echo "host=$(hostname -s) time=$(date -Is)"
  echo "--- ip ---"
  ip -br addr | sed -n '1,80p' || true
  echo "--- routes ---"
  ip route | sed -n '1,30p' || true
  echo "--- wg ---"
  wg show interfaces 2>/dev/null || true
  wg show 2>/dev/null | sed -n '1,80p' || true
  echo "--- ufw ---"
  ufw status verbose 2>/dev/null | sed -n '1,80p' || true
  echo "--- sshd effective ---"
  sshd -T 2>/dev/null | egrep -i 'permitrootlogin|maxauthtries|clientaliveinterval|clientalivecountmax|passwordauthentication|kbdinteractiveauthentication|pubkeyauthentication' || true
}

apply_hosts() {
  need_root
  write_hosts_block "$BASE/templates/hosts/reseau_hosts.block"
  echo "OK: /etc/hosts updated"
}

apply_sshd_safe() {
  need_root
  local dst="/etc/ssh/sshd_config.d/99-reseau_ssh_safe.conf"
  mkdir -p /etc/ssh/sshd_config.d
  backup_file "$dst"
  cp -a "$BASE/templates/sshd_config.d/99-reseau_ssh_safe.conf" "$dst"
  restart_ssh
  echo "OK: sshd SAFE drop-in installed + service restarted"
}

apply_sshd_lockdown() {
  need_root
  local host user ak
  host="$(hostname -s)"
  case "$host" in
    admin-trading|db-layer) user="ghost" ;;
    student) user="student" ;;
    *) user="$(logname 2>/dev/null || echo ghost)" ;;
  esac
  ak="/home/$user/.ssh/authorized_keys"
  if ! nonempty_file "$ak"; then
    echo "ERROR: authorized_keys missing or empty: $ak" >&2
    echo "Refusing to enable LOCKDOWN (would risk lockout)." >&2
    exit 2
  fi
  local dst="/etc/ssh/sshd_config.d/99-reseau_ssh_lockdown.conf"
  mkdir -p /etc/ssh/sshd_config.d
  backup_file "$dst"
  cp -a "$BASE/templates/sshd_config.d/99-reseau_ssh_lockdown.conf" "$dst"
  restart_ssh
  echo "OK: sshd LOCKDOWN enabled (PasswordAuthentication no)"
}

apply_ufw_baseline() {
  need_root
  local host
  host="$(hostname -s)"

  # defaults (safe)
  ufw default deny incoming >/dev/null 2>&1 || true
  ufw default allow outgoing >/dev/null 2>&1 || true

  # SSH from LAN + WG mgmt
  ufw_allow_rule allow from "$LAN_CIDR" to any port 22 proto tcp
  ufw_allow_rule allow from "$WG_MGMT_CIDR" to any port 22 proto tcp

  if [[ "$host" == "admin-trading" ]]; then
    # WG servers on admin-trading
    ufw_allow_rule allow from "$LAN_CIDR" to any port 51820 proto udp
    ufw_allow_rule allow from "$LAN_CIDR" to any port 51821 proto udp
    # allow mgmt-subnet access to WG ports too (useful for internal testing)
    ufw_allow_rule allow from "$WG_MGMT_CIDR" to any port 51820 proto udp
    ufw_allow_rule allow from "$WG_MGMT_CIDR" to any port 51821 proto udp
  else
    # client machines: OPTIONAL cleanup of stray open wg port
    ufw_delete_if_present delete allow 51820/udp
    ufw_delete_if_present delete allow 51821/udp
  fi

  ufw --force enable >/dev/null 2>&1 || true
  echo "OK: UFW baseline applied + enabled"
}

disable_dblayer_wg0() {
  need_root
  local host
  host="$(hostname -s)"
  if [[ "$host" != "db-layer" ]]; then
    echo "ERROR: this action is intended for db-layer only" >&2
    exit 2
  fi
  systemctl disable --now wg-quick@wg0 >/dev/null 2>&1 || true
  ip link show wg0 >/dev/null 2>&1 && echo "WARN: wg0 still present (may be managed differently)" || echo "OK: wg0 stopped/disabled (if it existed)"
}

apply_safe() {
  apply_hosts
  apply_sshd_safe
  apply_ufw_baseline
  echo "OK: SAFE baseline done"
}

main() {
  local cmd="${1:-}"; shift || true
  case "$cmd" in
    status) status ;;
    apply-safe) apply_safe ;;
    apply-lockdown) apply_sshd_lockdown ;;
    disable-dblayer-wg0) disable_dblayer_wg0 ;;
    ""|-h|--help|help) usage ;;
    *) echo "ERROR: unknown command: $cmd" >&2; usage; exit 1 ;;
  esac
}
main "$@"
