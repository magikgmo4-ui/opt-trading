#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-$HOME/reseau_ssh_keys_bundle.pub}"
: > "$OUT"
echo "=== make_keys_bundle_admin ==="
echo "Output: $OUT"

add_keyfile() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  cat "$f" >> "$OUT"
  echo >> "$OUT"
  echo "OK added: $f"
}

add_keyfile "$HOME/.ssh/id_ed25519.pub"
add_keyfile "$HOME/.ssh/id_ed25519_fantome.pub"

for host in db-layer student; do
  for pub in ".ssh/id_ed25519.pub" ".ssh/id_ed25519_fantome.pub"; do
    if ssh -o BatchMode=yes -o ConnectTimeout=3 "$host" "test -f ~/$pub" 2>/dev/null; then
      ssh "$host" "cat ~/$pub" >> "$OUT" && echo >> "$OUT"
      echo "OK pulled: $host ~/$pub"
    else
      echo "WARN could not pull: $host ~/$pub"
    fi
  done
done

echo "Done."
wc -l "$OUT" || true
