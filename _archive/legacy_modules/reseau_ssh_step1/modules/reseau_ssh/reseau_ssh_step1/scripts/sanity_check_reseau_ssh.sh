#!/usr/bin/env bash
set -euo pipefail

echo "=== reseau_ssh sanity check (Step 1) ==="
date -Is

echo "[host]"
hostnamectl 2>/dev/null | sed -n '1,8p' || hostname

echo "[ssh]"
command -v ssh >/dev/null && ssh -V || echo "ssh not found"

echo "[inventory]"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INV="$ROOT_DIR/hosts.yaml"
test -f "$INV" && echo "OK inventory: $INV" || (echo "Missing hosts.yaml" && exit 1)

echo "OK: sanity passed"
