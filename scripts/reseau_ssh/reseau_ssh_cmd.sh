#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/scripts/reseau_ssh"
# shellcheck source=/dev/null
source "$BASE/lib/common.sh"

usage() {
  cat <<'USAGE'
cmd-reseau_ssh <command> [args]

Commands:
  sanity
  bootstrap                 # install packages + enable ufw + fail2ban (safe rules)
  ssh-hardening-safe        # adds a drop-in config WITHOUT disabling password auth
  ssh-lockdown              # disables password auth (requires existing authorized_keys)
  wg-server-init [wg_ip]    # default wg_ip=10.66.66.1/24
  wg-client-init <server_lan_ip> <client_wg_ip>  # writes /etc/wireguard/wg0.conf and prints it
  wg-add-peer <peer_name> <peer_pubkey> <peer_wg_ip_cidr>
  wg-up | wg-down | wg-show
USAGE
}

ensure_pkgs() {
  if ! is_debian_like; then
    log "WARN: non-debian detected; continuing anyway."
  fi
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y
  apt-get install -y openssh-server ufw fail2ban wireguard wireguard-tools
}

cmd_sanity() {
  "$BASE/sanity_reseau_ssh.sh"
}

cmd_bootstrap() {
  need_root
  ensure_pkgs

  systemctl enable --now ssh >/dev/null 2>&1 || systemctl enable --now sshd >/dev/null 2>&1 || true

  # Fail2Ban: systemd backend for sshd
  mkdir -p /etc/fail2ban/jail.d
  cat > /etc/fail2ban/jail.d/sshd.local <<'EOF'
[sshd]
enabled = true
backend = systemd
EOF
  systemctl enable --now fail2ban >/dev/null 2>&1 || true

  # UFW: safe defaults
  ufw --force reset >/dev/null
  ufw default deny incoming >/dev/null
  ufw default allow outgoing >/dev/null
  local lan
  lan="$(detect_lan_cidr)"
  # allow SSH from LAN
  ufw_allow_from_cidr "$lan" 22 tcp
  # allow WireGuard from LAN
  ufw_allow_from_cidr "$lan" 51820 udp
  ufw --force enable >/dev/null

  log "OK: bootstrap complete (UFW+Fail2Ban+SSH). LAN=$lan"
}

cmd_ssh_hardening_safe() {
  need_root
  mkdir -p /etc/ssh/sshd_config.d
  backup_file /etc/ssh/sshd_config

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
  log "OK: ssh hardening SAFE applied (/etc/ssh/sshd_config.d/99-reseau_ssh_safe.conf)"
}

cmd_ssh_lockdown() {
  need_root
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
  log "OK: ssh lockdown applied (password auth disabled)"
}

wg_write_sysctl() {
  need_root
  mkdir -p /etc/sysctl.d
  cat > /etc/sysctl.d/99-reseau_ssh_wg.conf <<'EOF'
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
EOF
  sysctl --system >/dev/null 2>&1 || true
}

wg_server_init() {
  need_root
  local wg_ip="${1:-10.66.66.1/24}"
  mkdir -p /etc/wireguard
  umask 077
  if [[ ! -f /etc/wireguard/server.key ]]; then
    wg genkey | tee /etc/wireguard/server.key | wg pubkey > /etc/wireguard/server.pub
  fi
  local priv pub
  priv="$(cat /etc/wireguard/server.key)"
  pub="$(cat /etc/wireguard/server.pub)"

  cat > /etc/wireguard/wg0.conf <<EOF
[Interface]
Address = $wg_ip
ListenPort = 51820
PrivateKey = $priv

# Peers added via: cmd-reseau_ssh wg-add-peer ...
EOF

  wg_write_sysctl
  systemctl enable --now wg-quick@wg0 >/dev/null 2>&1 || true
  log "OK: WG server init. Server pubkey:"
  echo "$pub"
  log "TIP: add peers with: cmd-reseau_ssh wg-add-peer <name> <pubkey> <10.66.66.x/32>"
}

wg_client_init() {
  need_root
  local server_lan_ip="${1:-}"
  local client_wg_ip="${2:-}"
  if [[ -z "$server_lan_ip" || -z "$client_wg_ip" ]]; then
    echo "ERROR: usage: cmd-reseau_ssh wg-client-init <server_lan_ip> <client_wg_ip>" >&2
    exit 2
  fi

  mkdir -p /etc/wireguard
  umask 077
  if [[ ! -f /etc/wireguard/client.key ]]; then
    wg genkey | tee /etc/wireguard/client.key | wg pubkey > /etc/wireguard/client.pub
  fi
  local priv pub
  priv="$(cat /etc/wireguard/client.key)"
  pub="$(cat /etc/wireguard/client.pub)"

  cat > /etc/wireguard/wg0.conf <<EOF
[Interface]
Address = $client_wg_ip
PrivateKey = $priv
DNS = 1.1.1.1

[Peer]
# TODO: set to the SERVER public key (printed by wg-server-init)
PublicKey = REPLACE_WITH_SERVER_PUBKEY
AllowedIPs = 10.66.66.0/24
Endpoint = ${server_lan_ip}:51820
PersistentKeepalive = 25
EOF

  wg_write_sysctl
  systemctl enable --now wg-quick@wg0 >/dev/null 2>&1 || true

  log "OK: WG client init."
  log "Client pubkey (copy to server):"
  echo "$pub"
  log "Client config written: /etc/wireguard/wg0.conf (replace server pubkey)"
}

wg_add_peer() {
  need_root
  local name="${1:-}"
  local pub="${2:-}"
  local ip="${3:-}"
  if [[ -z "$name" || -z "$pub" || -z "$ip" ]]; then
    echo "ERROR: usage: cmd-reseau_ssh wg-add-peer <peer_name> <peer_pubkey> <peer_wg_ip_cidr>" >&2
    exit 2
  fi
  if [[ ! -f /etc/wireguard/wg0.conf ]]; then
    echo "ERROR: /etc/wireguard/wg0.conf not found. Run wg-server-init first." >&2
    exit 2
  fi
  backup_file /etc/wireguard/wg0.conf
  cat >> /etc/wireguard/wg0.conf <<EOF

# $name
[Peer]
PublicKey = $pub
AllowedIPs = $ip
EOF
  systemctl restart wg-quick@wg0 >/dev/null 2>&1 || true
  log "OK: peer added: $name ($ip)"
}

wg_up()   { need_root; systemctl start wg-quick@wg0; }
wg_down() { need_root; systemctl stop wg-quick@wg0; }
wg_show() { wg show 2>/dev/null || true; ip a show wg0 2>/dev/null || true; }

main() {
  local cmd="${1:-}"; shift || true
  case "$cmd" in
    sanity) cmd_sanity ;;
    bootstrap) cmd_bootstrap ;;
    ssh-hardening-safe) cmd_ssh_hardening_safe ;;
    ssh-lockdown) cmd_ssh_lockdown ;;
    wg-server-init) wg_server_init "$@" ;;
    wg-client-init) wg_client_init "$@" ;;
    wg-add-peer) wg_add_peer "$@" ;;
    wg-up) wg_up ;;
    wg-down) wg_down ;;
    wg-show) wg_show ;;
    ""|-h|--help|help) usage ;;
    *) echo "ERROR: unknown command: $cmd" >&2; usage; exit 1 ;;
  esac
}
main "$@"
