#!/usr/bin/env bash
set -euo pipefail
echo "--- sftp users ---"
getent passwd | awk -F: '$1 ~ /^sftp_/ {printf "%-16s home=%s shell=%s\n",$1,$6,$7}'
