#!/usr/bin/env bash
set -euo pipefail

RESEAU_SSH_BASELINE_DIR="$RESEAU_SSH_MODULE_DIR/baseline"
RESEAU_SSH_BASELINE_HOSTS_BLOCK="$RESEAU_SSH_BASELINE_DIR/hosts.block"
RESEAU_SSH_BASELINE_SSH_CONFIG="$RESEAU_SSH_BASELINE_DIR/ssh_config.linux"

reseau_ssh_baseline_ts() { date -Is; }

reseau_ssh_baseline_apply_linux() {
  local apply="${1:-}"

  mkdir -p "$HOME/.ssh"
  chmod 700 "$HOME/.ssh"

  echo "=== reseau_ssh baseline apply_linux ==="
  echo "$(reseau_ssh_baseline_ts)"
  echo "[whoami] $(whoami) @ $(hostname)"
  echo "[mode] ${apply:-dry-run}"
  echo

  if [[ "$apply" != "--apply" ]]; then
    echo "DRY-RUN ONLY."
    echo "Would install: $RESEAU_SSH_BASELINE_SSH_CONFIG -> $HOME/.ssh/config"
    echo "Would update:  /etc/hosts (managed block from $RESEAU_SSH_BASELINE_HOSTS_BLOCK)"
    echo "Run with --apply to make changes."
    return 0
  fi

  local cfg="$HOME/.ssh/config"
  if [[ -f "$cfg" ]]; then
    cp -a "$cfg" "$cfg.bak.$(date +%F_%H%M%S)"
  fi
  cp -a "$RESEAU_SSH_BASELINE_SSH_CONFIG" "$cfg"
  chmod 600 "$cfg"

  local tmp
  tmp="$(mktemp)"
  sudo cp -a /etc/hosts "/etc/hosts.bak.reseau_ssh.$(date +%F_%H%M%S)"

  sudo awk '
    BEGIN{inblk=0}
    /^# === reseau_ssh BEGIN ===/{inblk=1; next}
    /^# === reseau_ssh END ===/{inblk=0; next}
    { if(!inblk) print $0 }
  ' /etc/hosts > "$tmp"

  printf "\n" >> "$tmp"
  cat "$RESEAU_SSH_BASELINE_HOSTS_BLOCK" >> "$tmp"
  sudo cp "$tmp" /etc/hosts
  rm -f "$tmp"

  echo "OK: applied ~/.ssh/config and /etc/hosts"
}

reseau_ssh_baseline_apply_hostname() {
  local target="${1:-}"
  if [[ -z "$target" ]]; then
    echo "Usage: baseline-hostname <target-hostname>" >&2
    exit 1
  fi

  echo "=== reseau_ssh baseline hostname apply ==="
  echo "Current: $(hostname)"
  echo "Target : $target"

  if [[ "$(hostname)" == "$target" ]]; then
    echo "OK: already set"
    return 0
  fi

  sudo hostnamectl set-hostname "$target"
  echo "OK: now $(hostname)"
}

reseau_ssh_baseline_sanity() {
  echo "=== reseau_ssh baseline sanity ==="
  echo "$(reseau_ssh_baseline_ts)"
  echo "[host] $(whoami) @ $(hostname)"
  echo

  echo "[/etc/hosts block]"
  if grep -q "# === reseau_ssh BEGIN ===" /etc/hosts; then
    awk '
      /^# === reseau_ssh BEGIN ===/{p=1}
      p{print}
      /^# === reseau_ssh END ===/{p=0}
    ' /etc/hosts
  else
    echo "WARN: reseau_ssh block missing in /etc/hosts"
  fi
  echo

  echo "[ssh config]"
  local cfg="$HOME/.ssh/config"
  if [[ -f "$cfg" ]]; then
    echo "OK: $cfg"
    grep -nE '^Host (admin-trading|db-layer|student|cursor-ai)$' "$cfg" || echo "WARN: missing Host entries"
  else
    echo "WARN: missing $cfg"
  fi
  echo

  echo "[connectivity (BatchMode best-effort)]"
  local h
  for h in admin-trading db-layer student cursor-ai; do
    echo "--- $h ---"
    timeout 6 ssh -o BatchMode=yes -o ConnectTimeout=3 "$h" 'echo OK $(hostname); exit 0' 2>/dev/null \
      && echo "OK $h" || echo "WARN $h (key missing / not reachable / windows ssh not enabled)"
  done

  echo
  echo "OK: sanity finished"
}

reseau_ssh_baseline_show_hosts() {
  sed -n '1,120p' "$RESEAU_SSH_BASELINE_HOSTS_BLOCK"
}

reseau_ssh_baseline_show_ssh() {
  sed -n '1,220p' "$RESEAU_SSH_BASELINE_SSH_CONFIG"
}
