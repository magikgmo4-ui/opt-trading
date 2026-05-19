#!/usr/bin/env bash
# Authorize a Termux public key on all Linux fleet machines
# Run from db-layer after copying the Termux public key
# Usage: bash authorize_termux_key.sh "<ssh-ed25519 AAAA... termux_YYYYMMDD>"
set -euo pipefail

TERMUX_KEY="${1:-}"
if [ -z "$TERMUX_KEY" ]; then
    echo "usage: $0 '<public-key-content>'" >&2
    echo "  Get your key with: cat ~/.ssh/id_ed25519_termux.pub  (on Android)" >&2
    exit 2
fi

MACHINES=(db-layer admin-trading fantome student)
PASS=0; FAIL=0

ok()   { echo "  OK  $*"; ((PASS++)) || true; }
fail() { echo "  FAIL $*" >&2; ((FAIL++)) || true; }

echo "=== Authorizing Termux key on fleet ==="
echo "  Key: ${TERMUX_KEY:0:40}..."

for machine in "${MACHINES[@]}"; do
    if [ "$machine" = "$(hostname)" ]; then
        # Local
        if grep -qF "$TERMUX_KEY" ~/.ssh/authorized_keys 2>/dev/null; then
            ok "$machine: already authorized"
        else
            echo "$TERMUX_KEY" >> ~/.ssh/authorized_keys
            ok "$machine: authorized"
        fi
    else
        result=$(ssh -o BatchMode=yes -o ConnectTimeout=5 "$machine" "
            grep -qF '$TERMUX_KEY' ~/.ssh/authorized_keys 2>/dev/null && echo ALREADY || {
                echo '$TERMUX_KEY' >> ~/.ssh/authorized_keys && echo ADDED
            }
        " 2>&1)
        rc=$?
        [ $rc -eq 0 ] && ok "$machine: $result" || fail "$machine: $result"
    fi
done

echo ""
echo "=== $PASS/${#MACHINES[@]} machines authorized ==="
echo ""
echo "Test depuis Termux :"
echo "  ssh db-layer 'hostname'"
