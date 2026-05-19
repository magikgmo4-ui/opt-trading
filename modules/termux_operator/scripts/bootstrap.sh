#!/usr/bin/env bash
# Termux bootstrap — opt-trading mobile operator setup
# Run ONCE in Termux after fresh install
# Source: https://f-droid.org/en/packages/com.termux/
set -euo pipefail

echo "=== Termux Bootstrap — opt-trading mobile operator ==="

# ── 1. Packages essentiels ────────────────────────────────────────────────
echo "--- [1/5] packages ---"
pkg update -y && pkg upgrade -y
pkg install -y openssh tmux git python nano jq coreutils

# ── 2. Répertoires operator ───────────────────────────────────────────────
echo "--- [2/5] directories ---"
mkdir -p ~/.termux/tasker ~/operator ~/.ssh
chmod 700 ~/.termux ~/.termux/tasker ~/operator ~/.ssh
echo "  ~/.termux/tasker  (Tasker scripts)"
echo "  ~/operator        (notes et scripts locaux)"
echo "  ~/.ssh            (clés SSH)"

# ── 3. Clé SSH mobile ─────────────────────────────────────────────────────
echo "--- [3/5] SSH key ---"

KEY="$HOME/.ssh/id_ed25519_termux"
if [ -f "$KEY" ]; then
    echo "  KEY EXISTS: $KEY"
else
    ssh-keygen -t ed25519 -f "$KEY" -N "" -C "termux_$(date +%Y%m%d)"
    echo "  KEY CREATED: $KEY"
fi
echo "  Public key:"
cat "${KEY}.pub"

# ── 4. SSH config ─────────────────────────────────────────────────────────
echo "--- [4/5] SSH config ---"
cat > ~/.ssh/config <<'EOF'
Host *
  ServerAliveInterval 30
  ServerAliveCountMax 3
  TCPKeepAlive yes
  IdentitiesOnly yes
  IdentityFile ~/.ssh/id_ed25519_termux
  StrictHostKeyChecking accept-new

Host db-layer
  HostName 192.168.0.100
  User ghost
  Port 22

Host admin-trading
  HostName 192.168.0.111
  User ghost
  Port 22

Host fantome
  HostName 192.168.0.191
  User fantome
  Port 22

Host student
  HostName 192.168.0.142
  User student
  Port 22
EOF
chmod 600 ~/.ssh/config
echo "  SSH config written"

# ── 5. Aliases shell ──────────────────────────────────────────────────────
echo "--- [5/5] aliases ---"
BASHRC="$HOME/.bashrc"
if ! grep -q "opt-trading-mobile" "$BASHRC" 2>/dev/null; then
    cat >> "$BASHRC" <<'ALIASES'

# opt-trading mobile operator
alias fleet='ssh db-layer "cd /opt/trading && bash modules/openclaw_tmux_operator/scripts/cmd.sh fleet-status"'
alias health='ssh db-layer "cd /opt/trading && bash modules/openclaw_tmux_operator/scripts/cmd.sh health-all"'
alias sessions-db='ssh db-layer "tmux ls 2>/dev/null || echo no sessions"'
alias sessions-at='ssh admin-trading "tmux ls 2>/dev/null || echo no sessions"'
alias attach-db() { ssh db-layer -t "tmux attach -t ${1:-openclaw-core} || tmux ls"; }
alias attach-at() { ssh admin-trading -t "tmux attach -t ${1:-desk-pro} || tmux ls"; }
alias matrix='ssh db-layer "cd /opt/trading && bash scripts/reseau_ssh/ssh_matrix_test.sh"'
ALIASES
    echo "  Aliases added to $BASHRC"
else
    echo "  Aliases already present"
fi

# ── 6. Readiness checks ───────────────────────────────────────────────────
echo ""
echo "--- readiness ---"
ssh -V 2>&1 | head -1 && echo "  ssh OK"
tmux -V 2>&1 | head -1 && echo "  tmux OK"
jq --version 2>&1 | head -1 && echo "  jq OK"
ls -ld ~/.termux/tasker && echo "  tasker dir OK"
ls -ld ~/operator && echo "  operator dir OK"

# ── 7. Afficher clé publique à copier ─────────────────────────────────────
echo ""
echo "--- ACTION REQUIRED ---"
echo ""
echo "Copier cette clé publique sur db-layer :"
echo ""
cat "${KEY}.pub"
echo ""
echo "Commande à exécuter sur db-layer :"
echo "  echo '$(cat ${KEY}.pub)' >> ~/.ssh/authorized_keys"
echo "  echo '$(cat ${KEY}.pub)' >> ~/.ssh/authorized_keys  # admin-trading"
echo ""
echo "=== Bootstrap terminé. Relancer : source ~/.bashrc ==="
