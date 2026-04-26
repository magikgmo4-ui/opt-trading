#!/usr/bin/env bash
set -euo pipefail

reseau_ssh_transition_ts() { date -Is; }

reseau_ssh_transition_log() { echo "[$(reseau_ssh_transition_ts)] $*"; }

reseau_ssh_transition_need_root() {
  if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
    echo "ERROR: run as root (sudo)." >&2
    exit 1
  fi
}

reseau_ssh_transition_backup_file() {
  local f="$1"
  if [[ -f "$f" ]]; then
    mkdir -p /var/backups/reseau_ssh
    local b="/var/backups/reseau_ssh/$(basename "$f").$(date +%Y%m%d_%H%M%S).bak"
    cp -a "$f" "$b"
    reseau_ssh_transition_log "backup: $f -> $b"
  fi
}

reseau_ssh_transition_detect_lan_cidr() {
  local ip
  ip="$(ip -4 -o addr show scope global | awk '{print $4}' | head -n1 || true)"
  if [[ -n "$ip" ]]; then
    echo "$ip" | awk -F'/' '{print $1"/"$2}'
  else
    echo "192.168.16.0/24"
  fi
}

reseau_ssh_transition_ufw_allow_from_cidr() {
  local cidr="$1"
  local port="$2"
  local proto="${3:-tcp}"
  ufw allow from "$cidr" to any port "$port" proto "$proto" >/dev/null
}

reseau_ssh_transition_is_debian_like() {
  [[ -f /etc/debian_version ]]
}

reseau_ssh_transition_ensure_pkgs() {
  if ! reseau_ssh_transition_is_debian_like; then
    reseau_ssh_transition_log "WARN: non-debian detected; continuing anyway."
  fi
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y
  apt-get install -y openssh-server ufw fail2ban wireguard wireguard-tools
}

reseau_ssh_transition_bootstrap() {
  reseau_ssh_transition_need_root
  reseau_ssh_transition_ensure_pkgs

  systemctl enable --now ssh >/dev/null 2>&1 || systemctl enable --now sshd >/dev/null 2>&1 || true

  mkdir -p /etc/fail2ban/jail.d
  cat > /etc/fail2ban/jail.d/sshd.local <<'EOF'
[sshd]
enabled = true
backend = systemd
EOF
  systemctl enable --now fail2ban >/dev/null 2>&1 || true

  ufw --force reset >/dev/null
  ufw default deny incoming >/dev/null
  ufw default allow outgoing >/dev/null
  local lan
  lan="$(reseau_ssh_transition_detect_lan_cidr)"
  reseau_ssh_transition_ufw_allow_from_cidr "$lan" 22 tcp
  reseau_ssh_transition_ufw_allow_from_cidr "$lan" 51820 udp
  ufw --force enable >/dev/null

  reseau_ssh_transition_log "OK: bootstrap complete (UFW+Fail2Ban+SSH). LAN=$lan"
}

reseau_ssh_transition_ssh_hardening_safe() {
  reseau_ssh_transition_need_root
  mkdir -p /etc/ssh/sshd_config.d
  reseau_ssh_transition_backup_file /etc/ssh/sshd_config

  cat > /etc/ssh/sshd_config.d/99-reseau_ssh_safe.conf <<'EOF'
# reseau_ssh SAFE hardening (does NOT disable password auth)
Protocol 2
PermitRootLogin no
X11Forwarding no
AllowTcpForwarding no
ClientAliveInterval 60
ClientAliveCountMax 2
MaxAuthTries 4
LoginGraceTime 30
EOF

  systemctl reload ssh >/dev/null 2>&1 || systemctl reload sshd >/dev/null 2>&1 || true
  reseau_ssh_transition_log "OK: ssh hardening SAFE applied (/etc/ssh/sshd_config.d/99-reseau_ssh_safe.conf)"
}

reseau_ssh_transition_ssh_lockdown() {
  reseau_ssh_transition_need_root
  local home_dir="${SUDO_USER:+/home/$SUDO_USER}"
  if [[ -z "${home_dir:-}" || ! -d "$home_dir" ]]; then
    home_dir="$HOME"
  fi

  local ak="$home_dir/.ssh/authorized_keys"
  if [[ ! -s "$ak" ]]; then
    echo "ERROR: $ak missing/empty. Refusing to disable password auth." >&2
    exit 2
  fi

  mkdir -p /etc/ssh/sshd_config.d
  cat > /etc/ssh/sshd_config.d/99-reseau_ssh_lockdown.conf <<'EOF'
# reseau_ssh LOCKDOWN (requires working authorized_keys)
PasswordAuthentication no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
PubkeyAuthentication yes
EOF

  systemctl reload ssh >/dev/null 2>&1 || systemctl reload sshd >/dev/null 2>&1 || true
  reseau_ssh_transition_log "OK: ssh lockdown applied (password auth disabled)"
}
