#!/usr/bin/env bash
set -euo pipefail

RESEAU_SSH_WIREGUARD_DIR="${RESEAU_SSH_MODULE_DIR}/wireguard"
RESEAU_SSH_WG_INVENTORY="${RESEAU_SSH_WIREGUARD_DIR}/inventory.yaml"
RESEAU_SSH_WG_TEMPLATES_DIR="${RESEAU_SSH_WIREGUARD_DIR}/templates"
RESEAU_SSH_WG_WINDOWS_DIR="${RESEAU_SSH_WIREGUARD_DIR}/windows"

RESEAU_SSH_WG_DATA_DIR="/opt/trading/data/reseau_ssh/wireguard"
RESEAU_SSH_WG_KEYS_DIR="${RESEAU_SSH_WG_DATA_DIR}/keys"
RESEAU_SSH_WG_PEERS_DIR="${RESEAU_SSH_WG_DATA_DIR}/peers"
RESEAU_SSH_WG_HUB_DIR="${RESEAU_SSH_WG_DATA_DIR}/hub"
RESEAU_SSH_WG_WIN_DIR="${RESEAU_SSH_WG_DATA_DIR}/windows"

reseau_ssh_wireguard_ts() { date -Iseconds; }
reseau_ssh_wireguard_die() { echo "ERROR: $*" >&2; exit 1; }

reseau_ssh_wireguard_need_cmd() {
  command -v "$1" >/dev/null 2>&1 || reseau_ssh_wireguard_die "missing command: $1"
}

reseau_ssh_wireguard_host_short() {
  hostname | tr -d '\r\n'
}

reseau_ssh_wireguard_iface() {
  local iface="${RESEAU_SSH_WG_IFACE:-wg-mgmt}"
  if [ -f "$RESEAU_SSH_WG_INVENTORY" ]; then
    iface="$(python3 - "$RESEAU_SSH_WG_INVENTORY" "$iface" <<'PY'
import sys, yaml
inv, fallback = sys.argv[1], sys.argv[2]
try:
    with open(inv, 'r', encoding='utf-8') as f:
        d = yaml.safe_load(f) or {}
    value = (d.get('policy', {}) or {}).get('wg_interface')
    print(value or fallback)
except Exception:
    print(fallback)
PY
)"
  fi
  printf '%s\n' "$iface"
}

reseau_ssh_wireguard_load_inventory_json() {
  python3 - "$RESEAU_SSH_WG_INVENTORY" <<'PY'
import sys, yaml, json
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f) or {}
print(json.dumps(data))
PY
}

reseau_ssh_wireguard_json_get() {
  python3 - "$1" "$2" <<'PY'
import sys, json
obj = json.loads(sys.argv[1])
path = sys.argv[2].split(".")
cur = obj
for key in path:
    cur = cur[key]
print(cur)
PY
}

reseau_ssh_wireguard_ensure_dirs() {
  sudo mkdir -p "$RESEAU_SSH_WG_DATA_DIR" "$RESEAU_SSH_WG_KEYS_DIR" "$RESEAU_SSH_WG_PEERS_DIR" "$RESEAU_SSH_WG_HUB_DIR" "$RESEAU_SSH_WG_WIN_DIR"
  sudo chown -R "$USER":"$USER" "$RESEAU_SSH_WG_DATA_DIR"
  chmod 700 "$RESEAU_SSH_WG_KEYS_DIR" "$RESEAU_SSH_WG_HUB_DIR" 2>/dev/null || true
}

reseau_ssh_wireguard_install() {
  echo "=== reseau_ssh wireguard install ==="
  if command -v wg >/dev/null 2>&1; then
    echo "OK: wireguard tools already installed"
    return 0
  fi
  echo "Installing wireguard packages (Debian/Ubuntu)..."
  sudo apt-get update
  sudo apt-get install -y wireguard wireguard-tools
  echo "OK: installed"
}

reseau_ssh_wireguard_genkeys() {
  reseau_ssh_wireguard_ensure_dirs
  local host
  host="$(reseau_ssh_wireguard_host_short)"
  local priv="${RESEAU_SSH_WG_KEYS_DIR}/${host}.key"
  local pub="${RESEAU_SSH_WG_KEYS_DIR}/${host}.pub"

  if [ -f "$priv" ] && [ -f "$pub" ]; then
    echo "OK: keys already exist: $priv $pub"
    return 0
  fi

  reseau_ssh_wireguard_need_cmd wg
  umask 077
  wg genkey | tee "$priv" | wg pubkey > "$pub"
  chmod 600 "$priv" "$pub"
  echo "OK: generated keys:"
  echo "  private: $priv"
  echo "  public : $pub"
}

reseau_ssh_wireguard_showpub() {
  reseau_ssh_wireguard_ensure_dirs
  local host pub
  host="$(reseau_ssh_wireguard_host_short)"
  pub="${RESEAU_SSH_WG_KEYS_DIR}/${host}.pub"
  [ -f "$pub" ] || reseau_ssh_wireguard_die "missing pubkey: run wg-genkeys first ($pub)"
  echo "HOST: $host"
  echo -n "PUBLIC KEY: "
  cat "$pub"
}

reseau_ssh_wireguard_render_server() {
  local inv_json hub_ip hub_port hub_name
  inv_json="$(reseau_ssh_wireguard_load_inventory_json)"
  hub_name="admin-trading"
  hub_ip="$(reseau_ssh_wireguard_json_get "$inv_json" "hosts.${hub_name}.wg_ip")"
  hub_port="$(reseau_ssh_wireguard_json_get "$inv_json" "hosts.${hub_name}.wg_listen_port")"

  local priv="${RESEAU_SSH_WG_KEYS_DIR}/${hub_name}.key"
  [ -f "$priv" ] || reseau_ssh_wireguard_die "hub private key missing: $priv (run wg-genkeys on admin-trading)"

  local peers_block=""
  local peer
  for peer in db-layer student cursor-ai; do
    local peer_pub="${RESEAU_SSH_WG_PEERS_DIR}/${peer}.pub"
    if [ -f "$peer_pub" ]; then
      local peer_ip
      peer_ip="$(reseau_ssh_wireguard_json_get "$inv_json" "hosts.${peer}.wg_ip")"
      peers_block+=$'\n'"[Peer]"$'\n'
      peers_block+="PublicKey = $(cat "$peer_pub")"$'\n'
      peers_block+="AllowedIPs = ${peer_ip}"$'\n'
    fi
  done

  local tpl="${RESEAU_SSH_WG_TEMPLATES_DIR}/wg0.server.template"
  local out="${RESEAU_SSH_WG_DATA_DIR}/wg0.admin-trading.conf"

  python3 - "$tpl" "$out" "$hub_ip" "$hub_port" "$priv" "$peers_block" <<'PY'
import sys
tpl, out, ip, port, priv, peers = sys.argv[1:7]
text = open(tpl, 'r', encoding='utf-8').read()
text = text.replace("{{WG_IP}}", ip)
text = text.replace("{{WG_PORT}}", port)
text = text.replace("{{PRIVATE_KEY}}", open(priv, 'r', encoding='utf-8').read().strip())
text = text.replace("{{PEERS}}", peers.strip() + "\n" if peers.strip() else "# (no peers yet) add pubkeys into /opt/trading/data/reseau_ssh/wireguard/peers/\n")
open(out, 'w', encoding='utf-8').write(text)
print(out)
PY
  echo "OK: rendered hub config: $out"
}

reseau_ssh_wireguard_render_client() {
  local inv_json host wg_ip keepalive hub_lan hub_port hub_endpoint wg_net
  inv_json="$(reseau_ssh_wireguard_load_inventory_json)"
  host="$(reseau_ssh_wireguard_host_short)"
  wg_ip="$(reseau_ssh_wireguard_json_get "$inv_json" "hosts.${host}.wg_ip")"
  keepalive="$(reseau_ssh_wireguard_json_get "$inv_json" "policy.wg_persistent_keepalive")"
  hub_lan="$(reseau_ssh_wireguard_json_get "$inv_json" "hosts.admin-trading.lan_ip")"
  hub_port="$(reseau_ssh_wireguard_json_get "$inv_json" "hosts.admin-trading.wg_listen_port")"
  hub_endpoint="${hub_lan}:${hub_port}"
  wg_net="$(reseau_ssh_wireguard_json_get "$inv_json" "policy.allowed_wg_cidr")"

  local priv="${RESEAU_SSH_WG_KEYS_DIR}/${host}.key"
  [ -f "$priv" ] || reseau_ssh_wireguard_die "private key missing: $priv (run wg-genkeys on this host)"

  local hub_pub="${RESEAU_SSH_WG_HUB_DIR}/admin-trading.pub"
  [ -f "$hub_pub" ] || reseau_ssh_wireguard_die "hub pubkey missing: $hub_pub (copy from admin-trading: ${RESEAU_SSH_WG_KEYS_DIR}/admin-trading.pub)"

  local tpl="${RESEAU_SSH_WG_TEMPLATES_DIR}/wg0.client.template"
  local out="${RESEAU_SSH_WG_DATA_DIR}/wg0.${host}.conf"

  python3 - "$tpl" "$out" "$wg_ip" "$priv" "$hub_pub" "$hub_endpoint" "$wg_net" "$keepalive" <<'PY'
import sys
tpl, out, ip, priv, hubpub, endpoint, wgnet, keep = sys.argv[1:9]
text = open(tpl, 'r', encoding='utf-8').read()
text = text.replace("{{WG_IP}}", ip)
text = text.replace("{{PRIVATE_KEY}}", open(priv, 'r', encoding='utf-8').read().strip())
text = text.replace("{{HUB_PUBLIC_KEY}}", open(hubpub, 'r', encoding='utf-8').read().strip())
text = text.replace("{{HUB_ENDPOINT}}", endpoint)
text = text.replace("{{WG_NET}}", wgnet)
text = text.replace("{{KEEPALIVE}}", keep)
open(out, 'w', encoding='utf-8').write(text)
print(out)
PY
  echo "OK: rendered client config: $out"
}

reseau_ssh_wireguard_render_windows() {
  reseau_ssh_wireguard_ensure_dirs
  local inv_json host wg_ip keepalive hub_lan hub_port hub_endpoint wg_net
  inv_json="$(reseau_ssh_wireguard_load_inventory_json)"
  host="cursor-ai"
  wg_ip="$(reseau_ssh_wireguard_json_get "$inv_json" "hosts.${host}.wg_ip")"
  keepalive="$(reseau_ssh_wireguard_json_get "$inv_json" "policy.wg_persistent_keepalive")"
  hub_lan="$(reseau_ssh_wireguard_json_get "$inv_json" "hosts.admin-trading.lan_ip")"
  hub_port="$(reseau_ssh_wireguard_json_get "$inv_json" "hosts.admin-trading.wg_listen_port")"
  hub_endpoint="${hub_lan}:${hub_port}"
  wg_net="$(reseau_ssh_wireguard_json_get "$inv_json" "policy.allowed_wg_cidr")"

  local priv="${RESEAU_SSH_WG_KEYS_DIR}/${host}.key"
  [ -f "$priv" ] || reseau_ssh_wireguard_die "windows private key not present here: $priv. Create on Windows using WireGuard app OR generate here then securely copy."
  local hub_pub="${RESEAU_SSH_WG_HUB_DIR}/admin-trading.pub"
  [ -f "$hub_pub" ] || reseau_ssh_wireguard_die "hub pubkey missing: $hub_pub"

  local tpl="${RESEAU_SSH_WG_TEMPLATES_DIR}/wg0.windows.template"
  local out="${RESEAU_SSH_WG_WIN_DIR}/${host}_$(reseau_ssh_wireguard_iface).conf"

  python3 - "$tpl" "$out" "$wg_ip" "$priv" "$hub_pub" "$hub_endpoint" "$wg_net" "$keepalive" <<'PY'
import sys
tpl, out, ip, priv, hubpub, endpoint, wgnet, keep = sys.argv[1:9]
text = open(tpl, 'r', encoding='utf-8').read()
text = text.replace("{{WG_IP}}", ip)
text = text.replace("{{PRIVATE_KEY}}", open(priv, 'r', encoding='utf-8').read().strip())
text = text.replace("{{HUB_PUBLIC_KEY}}", open(hubpub, 'r', encoding='utf-8').read().strip())
text = text.replace("{{HUB_ENDPOINT}}", endpoint)
text = text.replace("{{WG_NET}}", wgnet)
text = text.replace("{{KEEPALIVE}}", keep)
open(out, 'w', encoding='utf-8').write(text)
print(out)
PY
  echo "OK: rendered Windows config: $out"
}

reseau_ssh_wireguard_render() {
  reseau_ssh_wireguard_ensure_dirs
  if [ "$(reseau_ssh_wireguard_host_short)" = "admin-trading" ]; then
    reseau_ssh_wireguard_render_server
  else
    reseau_ssh_wireguard_render_client
  fi
}

reseau_ssh_wireguard_apply() {
  reseau_ssh_wireguard_ensure_dirs
  local host iface src dst
  host="$(reseau_ssh_wireguard_host_short)"
  iface="$(reseau_ssh_wireguard_iface)"
  if [ "$host" = "admin-trading" ]; then
    src="${RESEAU_SSH_WG_DATA_DIR}/wg0.admin-trading.conf"
    [ -f "$src" ] || reseau_ssh_wireguard_die "missing rendered hub config: $src (run wg-render on admin-trading)"
  else
    src="${RESEAU_SSH_WG_DATA_DIR}/wg0.${host}.conf"
    [ -f "$src" ] || reseau_ssh_wireguard_die "missing rendered client config: $src (run wg-render)"
  fi
  sudo mkdir -p /etc/wireguard
  dst="/etc/wireguard/${iface}.conf"
  if [ -f "$dst" ]; then
    sudo cp -a "$dst" "${dst}.bak.$(date +%F_%H%M%S)"
  fi
  sudo cp -a "$src" "$dst"
  sudo chmod 600 "$dst"
  echo "OK: wrote $dst"
}

reseau_ssh_wireguard_up() {
  local iface
  iface="$(reseau_ssh_wireguard_iface)"
  sudo systemctl enable --now "wg-quick@${iface}"
  echo "OK: wg up"
}

reseau_ssh_wireguard_down() {
  local iface
  iface="$(reseau_ssh_wireguard_iface)"
  sudo systemctl disable --now "wg-quick@${iface}" || true
  echo "OK: wg down"
}

reseau_ssh_wireguard_status() {
  local iface
  iface="$(reseau_ssh_wireguard_iface)"
  echo "=== wg status ==="
  sudo systemctl --no-pager status "wg-quick@${iface}" | sed -n '1,25p' || true
  echo
  sudo wg show "${iface}" 2>/dev/null || true
  echo
  ip -4 addr show "${iface}" 2>/dev/null || true
}

reseau_ssh_wireguard_fw_dry_run() {
  local inv_json allowed_lan allowed_wg hub_port
  inv_json="$(reseau_ssh_wireguard_load_inventory_json)"
  allowed_lan="$(reseau_ssh_wireguard_json_get "$inv_json" "policy.allowed_lan_cidr")"
  allowed_wg="$(reseau_ssh_wireguard_json_get "$inv_json" "policy.allowed_wg_cidr")"
  hub_port="$(reseau_ssh_wireguard_json_get "$inv_json" "hosts.admin-trading.wg_listen_port")"
  echo "=== UFW plan (dry-run) ==="
  echo "  ufw allow from ${allowed_lan} to any port 22 proto tcp"
  echo "  ufw allow from ${allowed_wg}  to any port 22 proto tcp"
  if [ "$(reseau_ssh_wireguard_host_short)" = "admin-trading" ]; then
    echo "  ufw allow from ${allowed_lan} to any port ${hub_port} proto udp  # WireGuard hub"
  fi
}

reseau_ssh_wireguard_fw_apply() {
  reseau_ssh_wireguard_need_cmd ufw
  local inv_json allowed_lan allowed_wg hub_port
  inv_json="$(reseau_ssh_wireguard_load_inventory_json)"
  allowed_lan="$(reseau_ssh_wireguard_json_get "$inv_json" "policy.allowed_lan_cidr")"
  allowed_wg="$(reseau_ssh_wireguard_json_get "$inv_json" "policy.allowed_wg_cidr")"
  hub_port="$(reseau_ssh_wireguard_json_get "$inv_json" "hosts.admin-trading.wg_listen_port")"

  echo "=== UFW apply ==="
  sudo ufw allow from "${allowed_lan}" to any port 22 proto tcp
  sudo ufw allow from "${allowed_wg}" to any port 22 proto tcp
  if [ "$(reseau_ssh_wireguard_host_short)" = "admin-trading" ]; then
    sudo ufw allow from "${allowed_lan}" to any port "${hub_port}" proto udp
  fi
  sudo ufw status verbose || true
}

reseau_ssh_wireguard_sanity() {
  local iface
  iface="$(reseau_ssh_wireguard_iface)"
  echo "=== reseau_ssh wireguard sanity ==="
  echo "$(reseau_ssh_wireguard_ts)"
  echo "[host] $USER @ $(reseau_ssh_wireguard_host_short)"
  echo

  echo "[ssh aliases]"
  local host
  for host in admin-trading db-layer student cursor-ai; do
    if ssh -o BatchMode=yes -o ConnectTimeout=2 "$host" 'hostname' >/dev/null 2>&1; then
      echo "OK ssh $host"
    else
      echo "WARN ssh $host"
    fi
  done
  echo

  echo "[wireguard tools]"
  if command -v wg >/dev/null 2>&1; then
    echo "OK wg installed"
  else
    echo "WARN: wg not installed"
  fi
  echo

  if [ -f "/etc/wireguard/${iface}.conf" ]; then
    echo "OK /etc/wireguard/${iface}.conf exists"
  else
    echo "WARN /etc/wireguard/${iface}.conf missing (expected after wg-apply)"
  fi
  echo

  if ip link show "${iface}" >/dev/null 2>&1; then
    echo "OK interface ${iface} exists"
    ip -4 addr show "${iface}" | sed -n '1,5p'
  else
    echo "WARN interface ${iface} not up (run wg-up)"
  fi
  echo
  echo "OK: sanity finished"
}

reseau_ssh_wireguard_menu() {
  local cmd="$RESEAU_SSH_TOP_CMD"
  while true; do
    echo "=== reseau_ssh WireGuard Menu ==="
    echo "1) Sanity"
    echo "2) Install WireGuard tools"
    echo "3) Generate keys (local)"
    echo "4) Show local public key"
    echo "5) Render config"
    echo "6) Apply config (/etc/wireguard/<iface>.conf)"
    echo "7) Bring interface up"
    echo "8) WireGuard status"
    echo "9) Bring interface down"
    echo "10) Firewall dry-run (UFW)"
    echo "11) Firewall apply (UFW)"
    echo "q) Quit"
    read -r -p "> " choice
    case "$choice" in
      1) bash "$cmd" wireguard-sanity ;;
      2) bash "$cmd" wg-install ;;
      3) bash "$cmd" wg-genkeys ;;
      4) bash "$cmd" wg-showpub ;;
      5) bash "$cmd" wg-render ;;
      6) bash "$cmd" wg-apply ;;
      7) bash "$cmd" wg-up ;;
      8) bash "$cmd" wg-status ;;
      9) bash "$cmd" wg-down ;;
      10) bash "$cmd" fw-dry-run ;;
      11) bash "$cmd" fw-apply ;;
      q|Q) exit 0 ;;
      *) echo "Invalid choice" ;;
    esac
    echo
  done
}

reseau_ssh_wireguard_dispatch() {
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    wg-install) reseau_ssh_wireguard_install "$@" ;;
    wg-genkeys) reseau_ssh_wireguard_genkeys "$@" ;;
    wg-showpub) reseau_ssh_wireguard_showpub "$@" ;;
    wg-render) reseau_ssh_wireguard_render "$@" ;;
    wg-render-windows) reseau_ssh_wireguard_render_windows "$@" ;;
    wg-apply) reseau_ssh_wireguard_apply "$@" ;;
    wg-up) reseau_ssh_wireguard_up "$@" ;;
    wg-down) reseau_ssh_wireguard_down "$@" ;;
    wg-status) reseau_ssh_wireguard_status "$@" ;;
    fw-dry-run) reseau_ssh_wireguard_fw_dry_run "$@" ;;
    fw-apply) reseau_ssh_wireguard_fw_apply "$@" ;;
    wireguard-sanity) reseau_ssh_wireguard_sanity "$@" ;;
    wireguard-menu) reseau_ssh_wireguard_menu "$@" ;;
    *) reseau_ssh_wireguard_die "unknown wireguard command: $cmd" ;;
  esac
}
