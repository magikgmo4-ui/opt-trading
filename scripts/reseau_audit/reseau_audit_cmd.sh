#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/scripts/reseau_audit"
# shellcheck source=/dev/null
source "$BASE/lib/common.sh"

usage() {
  cat <<'USAGE'
cmd-reseau_audit <command>

Commands:
  collect        Collecte un bundle complet (root) et produit un .tgz
  sanity         Alias de collect
USAGE
}

collect() {
  need_root
  local host tsdir root outdir tgz bn
  host="$(hostname -s 2>/dev/null || hostname)"
  tsdir="$(date +%Y%m%d_%H%M%S)"
  root="/opt/trading/_reseau_audit"
  outdir="$root/$host/$tsdir"
  tgz="$root/${host}_${tsdir}.tgz"

  mkdir -p "$outdir"

  {
    echo "reseau_audit v1.3"
    echo "host=$host"
    echo "time=$(date -Is)"
    echo "user=$(logname 2>/dev/null || echo unknown)"
    echo
  } > "$outdir/summary.txt"

  run_to_file "$outdir/00_host.txt" "hostname; hostnamectl 2>/dev/null | sed -n '1,25p' || true"
  run_to_file "$outdir/01_os.txt" "cat /etc/os-release 2>/dev/null || true; uname -a"
  run_to_file "$outdir/02_time.txt" "date -Is; timedatectl 2>/dev/null || true; chronyc tracking 2>/dev/null || true"

  run_to_file "$outdir/10_ip_addr.txt" "ip -br addr; ip -4 -o addr show scope global; ip -6 -o addr show scope global || true"
  run_to_file "$outdir/11_routes.txt" "ip route; ip -6 route || true; ip rule || true"
  run_to_file "$outdir/12_dns.txt" "resolvectl status 2>/dev/null || true; cat /etc/resolv.conf 2>/dev/null || true"
  run_to_file "$outdir/13_services_net.txt" "systemctl --no-pager status networking 2>/dev/null | sed -n '1,80p' || true; systemctl --no-pager status NetworkManager 2>/dev/null | sed -n '1,80p' || true; systemctl --no-pager status systemd-networkd 2>/dev/null | sed -n '1,80p' || true"
  run_to_file "$outdir/14_nmcli.txt" "nmcli dev show 2>/dev/null || true; nmcli con show 2>/dev/null || true"
  run_to_file "$outdir/15_hosts_file.txt" "ls -la /etc/hosts; sed -n '1,220p' /etc/hosts"

  run_to_file "$outdir/20_ssh_status.txt" "systemctl is-enabled ssh 2>/dev/null || systemctl is-enabled sshd 2>/dev/null || true; systemctl --no-pager status ssh 2>/dev/null | sed -n '1,120p' || systemctl --no-pager status sshd 2>/dev/null | sed -n '1,120p' || true; ss -ltnp | grep -E ':(22)\\s' || true"
  run_to_file "$outdir/21_sshd_config.txt" "ls -la /etc/ssh/sshd_config /etc/ssh/sshd_config.d 2>/dev/null || true; sed -n '1,220p' /etc/ssh/sshd_config 2>/dev/null || true"
  run_to_file "$outdir/22_sshd_dropins.txt" 'ls -la /etc/ssh/sshd_config.d 2>/dev/null || true; for f in /etc/ssh/sshd_config.d/*.conf; do echo "---" "$f"; sed -n "1,220p" "$f"; done 2>/dev/null || true'
  run_to_file "$outdir/23_sshd_effective.txt" "sshd -T 2>/dev/null | egrep -i 'port|listenaddress|passwordauthentication|kbdinteractiveauthentication|pubkeyauthentication|permitrootlogin|allowusers|allowgroups|maxauthtries|clientaliveinterval|clientalivecountmax' || true"

  run_to_file "$outdir/30_fail2ban_status.txt" "systemctl --no-pager status fail2ban 2>/dev/null | sed -n '1,120p' || true; fail2ban-client ping 2>/dev/null || true; fail2ban-client status sshd 2>/dev/null || true"
  run_to_file "$outdir/31_fail2ban_conf.txt" 'ls -la /etc/fail2ban 2>/dev/null || true; ls -la /etc/fail2ban/jail.d 2>/dev/null || true; for f in /etc/fail2ban/jail.conf /etc/fail2ban/jail.local /etc/fail2ban/jail.d/*.conf /etc/fail2ban/jail.d/*.local; do [[ -f "$f" ]] && echo "---" "$f" && sed -n "1,260p" "$f"; done'
  run_to_file "$outdir/32_fail2ban_logs.txt" "journalctl -u fail2ban --no-pager -n 250 2>/dev/null || true"

  run_to_file "$outdir/40_ufw.txt" "ufw status verbose 2>/dev/null || true; ufw show raw 2>/dev/null || true"
  run_to_file "$outdir/41_nft_iptables.txt" "nft list ruleset 2>/dev/null | sed -n '1,260p' || true; iptables -S 2>/dev/null || true"
  run_to_file "$outdir/42_sysctl_forward.txt" "sysctl net.ipv4.ip_forward 2>/dev/null || true; sysctl net.ipv6.conf.all.forwarding 2>/dev/null || true; sysctl -a 2>/dev/null | egrep 'net.ipv4.conf.all.rp_filter|net.ipv4.conf.default.rp_filter' || true"

  run_to_file "$outdir/50_wg_show.txt" "wg show 2>/dev/null || true; ip -4 a show wg0 2>/dev/null || true; ip -4 a show wg-mgmt 2>/dev/null || true"
  run_to_file "$outdir/51_wg_services.txt" "systemctl --no-pager status wg-quick@wg0 2>/dev/null | sed -n '1,120p' || true; systemctl --no-pager status wg-quick@wg-mgmt 2>/dev/null | sed -n '1,120p' || true"
  mkdir -p "$outdir/wireguard"
  if [[ -d /etc/wireguard ]]; then
    for f in /etc/wireguard/*.conf; do
      [[ -f "$f" ]] || continue
      bn="$(basename "$f")"
      sanitize_wg_conf "$f" "$outdir/wireguard/$bn.sanitized"
    done
    run_to_file "$outdir/52_wireguard_dir.txt" "ls -la /etc/wireguard 2>/dev/null || true"
  fi

  run_to_file "$outdir/60_authlog_tail.txt" "tail -n 250 /var/log/auth.log 2>/dev/null || true"
  run_to_file "$outdir/61_journal_sshd.txt" "journalctl -u ssh -u sshd --no-pager -n 250 2>/dev/null || true"
  run_to_file "$outdir/62_journal_ufw.txt" "journalctl -u ufw --no-pager -n 200 2>/dev/null || true"

  {
    echo "=== QUICK FACTS ==="
    echo "ip4_global: $(ip -4 -o addr show scope global | awk '{print $2"="$4}' | paste -sd ' ' -)"
    echo "routes: $(ip route | head -n 5 | tr '\n' '; ' )"
    echo "ssh_listen: $(ss -ltn 2>/dev/null | awk '$4 ~ /:22$/{print $4}' | paste -sd ',' -)"
    echo "ufw_active: $(ufw status 2>/dev/null | head -n1 || true)"
    echo "wg_ifaces: $(wg show interfaces 2>/dev/null || true)"
    echo "wg_mgmt_addr: $(ip -4 -o addr show dev wg-mgmt 2>/dev/null | awk '{print $4}' || true)"
  } >> "$outdir/summary.txt"

  mkdir -p "$root"
  tar czf "$tgz" -C "$root/$host" "$tsdir"

  echo "OK: archive: $tgz"
}

main() {
  local cmd="${1:-}"; shift || true
  case "$cmd" in
    collect|sanity) collect ;;
    ""|-h|--help|help) usage ;;
    *) echo "ERROR: unknown command: $cmd" >&2; usage; exit 1 ;;
  esac
}
main "$@"
