#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="$(cd "$HERE/.." && pwd)"

INV="$BASE/inventory.yaml"
DATA_DIR="/opt/trading/data/reseau_ssh/wireguard"
KEYS_DIR="$DATA_DIR/keys"
PEERS_DIR="$DATA_DIR/peers"
HUB_DIR="$DATA_DIR/hub"
WIN_DIR="$DATA_DIR/windows"

WG_IF_FALLBACK="wg-mgmt"
WG_IF="${RESEAU_SSH_WG_IFACE:-$WG_IF_FALLBACK}"
# If inventory specifies policy.wg_interface, it overrides the default.
if [ -f "$INV" ]; then
  WG_IF="$(python3 - "$INV" "$WG_IF" <<'PY'
import sys, yaml
inv, fallback = sys.argv[1], sys.argv[2]
try:
    with open(inv,'r',encoding='utf-8') as f:
        d=yaml.safe_load(f) or {}
    v=(d.get('policy',{}) or {}).get('wg_interface')
    print(v or fallback)
except Exception:
    print(fallback)
PY
)"
fi
ts() { date -Iseconds; }
die() { echo "ERROR: $*" >&2; exit 1; }

need_cmd() { command -v "$1" >/dev/null 2>&1 || die "missing command: $1"; }

host_short() { hostname | tr -d '\r\n'; }

load_inventory_py() {
  python3 - "$INV" <<'PY'
import sys, yaml, json
p=sys.argv[1]
with open(p,'r',encoding='utf-8') as f:
    d=yaml.safe_load(f)
print(json.dumps(d))
PY
}

json_get() {
  python3 - "$1" "$2" <<'PY'
import sys, json
obj=json.loads(sys.argv[1])
path=sys.argv[2].split(".")
cur=obj
for k in path:
    cur=cur[k]
print(cur)
PY
}

ensure_dirs() {
  sudo mkdir -p "$DATA_DIR" "$KEYS_DIR" "$PEERS_DIR" "$HUB_DIR" "$WIN_DIR"
  sudo chown -R "$USER":"$USER" "$DATA_DIR"
  chmod 700 "$KEYS_DIR" "$HUB_DIR" 2>/dev/null || true
}

wg_install() {
  echo "=== reseau_ssh_step2 wg-install ==="
  if command -v wg >/dev/null 2>&1; then
    echo "OK: wireguard tools already installed"
    return 0
  fi
  echo "Installing wireguard packages (Debian/Ubuntu)..."
  sudo apt-get update
  sudo apt-get install -y wireguard wireguard-tools
  echo "OK: installed"
}

wg_genkeys() {
  ensure_dirs
  local h
  h="$(host_short)"
  local priv="$KEYS_DIR/${h}.key"
  local pub="$KEYS_DIR/${h}.pub"

  if [ -f "$priv" ] && [ -f "$pub" ]; then
    echo "OK: keys already exist: $priv $pub"
    return 0
  fi

  need_cmd wg
  umask 077
  wg genkey | tee "$priv" | wg pubkey > "$pub"
  chmod 600 "$priv" "$pub"
  echo "OK: generated keys:"
  echo "  private: $priv"
  echo "  public : $pub"
}

wg_showpub() {
  ensure_dirs
  local h pub
  h="$(host_short)"
  pub="$KEYS_DIR/${h}.pub"
  [ -f "$pub" ] || die "missing pubkey: run wg-genkeys first ($pub)"
  echo "HOST: $h"
  echo -n "PUBLIC KEY: "
  cat "$pub"
}

render_server() {
  local inv_json hub_ip hub_port wg_mtu
  inv_json="$(load_inventory_py)"
  local hub_name="admin-trading"
  wg_mtu="$(json_get "$inv_json" "policy.wg_mtu")"
  hub_ip="$(json_get "$inv_json" "hosts.${hub_name}.wg_ip")"
  hub_port="$(json_get "$inv_json" "hosts.${hub_name}.wg_listen_port")"

  local priv="$KEYS_DIR/${hub_name}.key"
  [ -f "$priv" ] || die "hub private key missing: $priv (run wg-genkeys on admin-trading)"

  local peers_block=""
  for peer in db-layer student cursor-ai; do
    local peer_pub="$PEERS_DIR/${peer}.pub"
    if [ -f "$peer_pub" ]; then
      local peer_ip
      peer_ip="$(json_get "$inv_json" "hosts.${peer}.wg_ip")"
      peers_block+=$'\n'"[Peer]"$'\n'
      peers_block+="PublicKey = $(cat "$peer_pub")"$'\n'
      peers_block+="AllowedIPs = ${peer_ip}"$'\n'
    fi
  done

  local tpl="$BASE/templates/wg0.server.template"
  local out="$DATA_DIR/wg0.admin-trading.conf"

  python3 - "$tpl" "$out" "$hub_ip" "$hub_port" "$priv" "$peers_block" <<'PY'
import sys
tpl,out,ip,port,priv,peers=sys.argv[1:7]
t=open(tpl,'r',encoding='utf-8').read()
t=t.replace("{{WG_IP}}", ip)
t=t.replace("{{WG_PORT}}", port)
t=t.replace("{{PRIVATE_KEY}}", open(priv,'r',encoding='utf-8').read().strip())
t=t.replace("{{PEERS}}", peers.strip()+"\n" if peers.strip() else "# (no peers yet) add pubkeys into /opt/trading/data/reseau_ssh/wireguard/peers/\n")
open(out,'w',encoding='utf-8').write(t)
print(out)
PY
  echo "OK: rendered hub config: $out"
}

render_client() {
  local inv_json host wg_ip keepalive hub_lan hub_port hub_endpoint wg_net
  inv_json="$(load_inventory_py)"
  host="$(host_short)"
  wg_ip="$(json_get "$inv_json" "hosts.${host}.wg_ip")"
  keepalive="$(json_get "$inv_json" "policy.wg_persistent_keepalive")"
  hub_lan="$(json_get "$inv_json" "hosts.admin-trading.lan_ip")"
  hub_port="$(json_get "$inv_json" "hosts.admin-trading.wg_listen_port")"
  hub_endpoint="${hub_lan}:${hub_port}"
  wg_net="$(json_get "$inv_json" "policy.allowed_wg_cidr")"

  local priv="$KEYS_DIR/${host}.key"
  [ -f "$priv" ] || die "private key missing: $priv (run wg-genkeys on this host)"

  local hub_pub="$HUB_DIR/admin-trading.pub"
  [ -f "$hub_pub" ] || die "hub pubkey missing: $hub_pub (copy from admin-trading: $KEYS_DIR/admin-trading.pub)"

  local tpl="$BASE/templates/wg0.client.template"
  local out="$DATA_DIR/wg0.${host}.conf"

  python3 - "$tpl" "$out" "$wg_ip" "$priv" "$hub_pub" "$hub_endpoint" "$wg_net" "$keepalive" <<'PY'
import sys
tpl,out,ip,priv,hubpub,endpoint,wgnet,keep=sys.argv[1:9]
t=open(tpl,'r',encoding='utf-8').read()
t=t.replace("{{WG_IP}}", ip)
t=t.replace("{{PRIVATE_KEY}}", open(priv,'r',encoding='utf-8').read().strip())
t=t.replace("{{HUB_PUBLIC_KEY}}", open(hubpub,'r',encoding='utf-8').read().strip())
t=t.replace("{{HUB_ENDPOINT}}", endpoint)
t=t.replace("{{WG_NET}}", wgnet)
t=t.replace("{{KEEPALIVE}}", keep)
open(out,'w',encoding='utf-8').write(t)
print(out)
PY
  echo "OK: rendered client config: $out"
}

wg_render_windows() {
  ensure_dirs
  local inv_json host wg_ip keepalive hub_lan hub_port hub_endpoint wg_net
  inv_json="$(load_inventory_py)"
  host="cursor-ai"
  wg_ip="$(json_get "$inv_json" "hosts.${host}.wg_ip")"
  keepalive="$(json_get "$inv_json" "policy.wg_persistent_keepalive")"
  hub_lan="$(json_get "$inv_json" "hosts.admin-trading.lan_ip")"
  hub_port="$(json_get "$inv_json" "hosts.admin-trading.wg_listen_port")"
  hub_endpoint="${hub_lan}:${hub_port}"
  wg_net="$(json_get "$inv_json" "policy.allowed_wg_cidr")"

  local priv="$KEYS_DIR/${host}.key"
  [ -f "$priv" ] || die "windows private key not present here: $priv. Create on Windows using WireGuard app OR generate here then securely copy."
  local hub_pub="$HUB_DIR/admin-trading.pub"
  [ -f "$hub_pub" ] || die "hub pubkey missing: $hub_pub"

  local tpl="$BASE/templates/wg0.windows.template"
  local out="$WIN_DIR/${host}_${WG_IF}.conf"
  python3 - "$tpl" "$out" "$wg_ip" "$priv" "$hub_pub" "$hub_endpoint" "$wg_net" "$keepalive" <<'PY'
import sys
tpl,out,ip,priv,hubpub,endpoint,wgnet,keep=sys.argv[1:9]
t=open(tpl,'r',encoding='utf-8').read()
t=t.replace("{{WG_IP}}", ip)
t=t.replace("{{PRIVATE_KEY}}", open(priv,'r',encoding='utf-8').read().strip())
t=t.replace("{{HUB_PUBLIC_KEY}}", open(hubpub,'r',encoding='utf-8').read().strip())
t=t.replace("{{HUB_ENDPOINT}}", endpoint)
t=t.replace("{{WG_NET}}", wgnet)
t=t.replace("{{KEEPALIVE}}", keep)
open(out,'w',encoding='utf-8').write(t)
print(out)
PY
  echo "OK: rendered Windows config: $out"
}

wg_apply() {
  ensure_dirs
  local h
  h="$(host_short)"
  local src=""
  if [ "$h" = "admin-trading" ]; then
    src="$DATA_DIR/wg0.admin-trading.conf"
    [ -f "$src" ] || die "missing rendered hub config: $src (run wg-render on admin-trading)"
  else
    src="$DATA_DIR/wg0.${h}.conf"
    [ -f "$src" ] || die "missing rendered client config: $src (run wg-render)"
  fi
  sudo mkdir -p /etc/wireguard
  local dst="/etc/wireguard/${WG_IF}.conf"
  if [ -f "$dst" ]; then
    sudo cp -a "$dst" "${dst}.bak.$(date +%F_%H%M%S)"
  fi
  sudo cp -a "$src" "$dst"
  sudo chmod 600 "$dst"
  echo "OK: wrote $dst"
}

wg_up() {
  sudo systemctl enable --now "wg-quick@${WG_IF}"
  echo "OK: wg up"
}

wg_down() {
  sudo systemctl disable --now "wg-quick@${WG_IF}" || true
  echo "OK: wg down"
}

wg_status() {
  echo "=== wg status ==="
  sudo systemctl --no-pager status "wg-quick@${WG_IF}" | sed -n '1,25p' || true
  echo
  sudo wg show "${WG_IF}" 2>/dev/null || true
  echo
  ip -4 addr show "${WG_IF}" 2>/dev/null || true
}

fw_dry_run() {
  local inv_json allowed_lan allowed_wg hub_port
  inv_json="$(load_inventory_py)"
  allowed_lan="$(json_get "$inv_json" "policy.allowed_lan_cidr")"
  allowed_wg="$(json_get "$inv_json" "policy.allowed_wg_cidr")"
  hub_port="$(json_get "$inv_json" "hosts.admin-trading.wg_listen_port")"
  echo "=== UFW plan (dry-run) ==="
  echo "  ufw allow from ${allowed_lan} to any port 22 proto tcp"
  echo "  ufw allow from ${allowed_wg}  to any port 22 proto tcp"
  if [ "$(host_short)" = "admin-trading" ]; then
    echo "  ufw allow from ${allowed_lan} to any port ${hub_port} proto udp  # WireGuard hub"
  fi
}

fw_apply() {
  need_cmd ufw
  local inv_json allowed_lan allowed_wg hub_port
  inv_json="$(load_inventory_py)"
  allowed_lan="$(json_get "$inv_json" "policy.allowed_lan_cidr")"
  allowed_wg="$(json_get "$inv_json" "policy.allowed_wg_cidr")"
  hub_port="$(json_get "$inv_json" "hosts.admin-trading.wg_listen_port")"

  echo "=== UFW apply ==="
  sudo ufw allow from "${allowed_lan}" to any port 22 proto tcp
  sudo ufw allow from "${allowed_wg}"  to any port 22 proto tcp
  if [ "$(host_short)" = "admin-trading" ]; then
    sudo ufw allow from "${allowed_lan}" to any port "${hub_port}" proto udp
  fi
  sudo ufw status verbose || true
}

sanity() {
  echo "=== reseau_ssh sanity (Step 2) ==="
  echo "$(ts)"
  echo "[host] $USER @ $(host_short)"
  echo
  echo "[ssh aliases]"
  for h in admin-trading db-layer student cursor-ai; do
    if ssh -o BatchMode=yes -o ConnectTimeout=2 "$h" 'hostname' >/dev/null 2>&1; then
      echo "OK ssh $h"
    else
      echo "WARN ssh $h"
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
  if [ -f /etc/wireguard/${WG_IF}.conf ]; then
    echo "OK /etc/wireguard/${WG_IF}.conf exists"
  else
    echo "WARN /etc/wireguard/${WG_IF}.conf missing (expected after wg-apply)"
  fi
  echo
  if ip link show "${WG_IF}" >/dev/null 2>&1; then
    echo "OK interface ${WG_IF} exists"
    ip -4 addr show "${WG_IF}" | sed -n '1,5p'
  else
    echo "WARN interface ${WG_IF} not up (run wg-up)"
  fi
  echo
  echo "OK: sanity finished"
}

usage() {
  cat <<EOF
Usage: $0 <command>

WireGuard:
  wg-install         Install wireguard tools (Debian/Ubuntu)
  wg-genkeys         Generate local keypair into ${KEYS_DIR}/<host>.{key,pub}
  wg-showpub         Print local public key (copy to hub)
  wg-render          Render config (hub on admin-trading, client elsewhere)
  wg-render-windows  Render Windows tunnel config (requires cursor-ai key present locally)
  wg-apply           Write /etc/wireguard/${WG_IF}.conf (backup first)
  wg-up              Enable + start wg-quick@${WG_IF}
  wg-down            Stop + disable wg-quick@${WG_IF}
  wg-status          Show wg + systemd status

Firewall (optional):
  fw-dry-run         Print UFW plan
  fw-apply           Apply UFW rules (no enable/disable)

General:
  sanity             Best-effort checks
EOF
}

main() {
  local cmd="${1:-}"
  case "$cmd" in
    wg-install) wg_install ;;
    wg-genkeys) wg_genkeys ;;
    wg-showpub) wg_showpub ;;
    wg-render)
      ensure_dirs
      if [ "$(host_short)" = "admin-trading" ]; then
        render_server
      else
        render_client
      fi
      ;;
    wg-render-windows) wg_render_windows ;;
    wg-apply) wg_apply ;;
    wg-up) wg_up ;;
    wg-down) wg_down ;;
    wg-status) wg_status ;;
    fw-dry-run) fw_dry_run ;;
    fw-apply) fw_apply ;;
    sanity) sanity ;;
    -h|--help|"") usage ;;
    *) die "unknown command: $cmd" ;;
  esac
}

main "$@"
