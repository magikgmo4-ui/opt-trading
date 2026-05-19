#!/usr/bin/env bash
set -euo pipefail
echo "=== UI_DEBUG Sanity Check ==="
date --iso-8601=seconds || date
echo

need() { command -v "$1" >/dev/null 2>&1 || { echo "MISSING: $1"; exit 2; }; }

need bash
need ss
need ps
need systemctl
need journalctl
need grep
need find
need tar
need curl

echo "OK: base tools present"
echo
echo "[host]"
hostnamectl || true
echo
echo "[network]"
ip -br a || true
echo
echo "PASS: ui_debug sanity OK"
