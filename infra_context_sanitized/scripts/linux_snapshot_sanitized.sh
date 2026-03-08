#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-snapshot}"
mkdir -p "$OUT_DIR"

ts="$(date -Iseconds | tr ':' '-')"
OUT="$OUT_DIR/snapshot_${ts}.txt"

{
  echo "=== SANITIZED MACHINE SNAPSHOT (LINUX) ==="
  date -Iseconds
  echo

  echo "[host]"
  hostnamectl 2>/dev/null || true
  echo

  echo "[os-release]"
  cat /etc/os-release 2>/dev/null || true
  echo

  echo "[kernel]"
  uname -a || true
  echo

  echo "[cpu]"
  (command -v lscpu >/dev/null && lscpu) || true
  echo

  echo "[memory]"
  free -h || true
  echo

  echo "[disks df]"
  df -hT || true
  echo

  echo "[disks lsblk]"
  lsblk -f || true
  echo

  echo "[network ip]"
  ip -br a || true
  echo

  echo "[network routes]"
  ip r || true
  echo

  echo "[dns]"
  (command -v resolvectl >/dev/null && resolvectl status) || (cat /etc/resolv.conf || true)
  echo

  echo "[listening ports (top)]"
  ss -tulpn 2>/dev/null | head -n 120 || true
  echo

  echo "[firewall ufw]"
  (command -v ufw >/dev/null && sudo ufw status verbose) || echo "ufw not installed"
  echo

  echo "[fail2ban sshd]"
  (command -v fail2ban-client >/dev/null && sudo fail2ban-client status sshd) || echo "fail2ban/sshd jail not available"
  echo

  echo "[running services sample]"
  systemctl --type=service --state=running 2>/dev/null | head -n 140 || true
  echo

  echo "[docker]"
  (command -v docker >/dev/null && docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null) || echo "docker not installed / not running"
  echo

  echo "[paths check]"
  for p in /opt/trading /opt/trading/scripts /opt/trading/modules /usr/local/bin; do
    echo "--- $p"
    ls -la "$p" 2>/dev/null | head -n 80 || echo "missing"
  done
  echo

  echo "[REDACTION NOTE]"
  echo "Always scan this snapshot for tokens/URLs before sharing."
} | tee "$OUT"

echo
echo "Wrote: $OUT"
