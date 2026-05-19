#!/usr/bin/env bash
set -euo pipefail

TS="$(date -Iseconds)"
echo "=== install_module sanity ==="
echo "$TS"

need() { command -v "$1" >/dev/null 2>&1 || { echo "FAIL: missing '$1'"; exit 1; }; }

need bash
need unzip
need sed
need awk
need find
need date

ROOT="${ROOT:-/opt/trading}"
SHARED_DIR="${SHARED_DIR:-/srv/sftp/shared_files/shared}"

if [[ ! -d "$ROOT" ]]; then
  echo "FAIL: ROOT not found: $ROOT"
  exit 1
fi

if [[ ! -d "$SHARED_DIR" ]]; then
  echo "WARN: SHARED_DIR not found: $SHARED_DIR"
  echo "      (If you're on a machine without /srv/sftp, set SHARED_DIR=... or use git-sync workflow.)"
else
  echo "OK: SHARED_DIR=$SHARED_DIR"
fi

echo "OK: ROOT=$ROOT"
echo "PASS: sanity OK"
