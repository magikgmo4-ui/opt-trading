\
#!/usr/bin/env bash
set -euo pipefail

echo "=== reseau_ssh sanity (Step 1b) ==="
date -Is
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
CFG="$HOME/.ssh/config"
if [[ -f "$CFG" ]]; then
  echo "OK: $CFG"
  grep -nE '^Host (admin-trading|db-layer|student|cursor-ai)$' "$CFG" || echo "WARN: missing Host entries"
else
  echo "WARN: missing $CFG"
fi
echo

echo "[connectivity (BatchMode best-effort)]"
for h in admin-trading db-layer student cursor-ai; do
  echo "--- $h ---"
  timeout 6 ssh -o BatchMode=yes -o ConnectTimeout=3 "$h" 'echo OK $(hostname); exit 0' 2>/dev/null \
    && echo "OK $h" || echo "WARN $h (key missing / not reachable / windows ssh not enabled)"
done

echo
echo "OK: sanity finished"
