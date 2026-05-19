#!/usr/bin/env bash
set -euo pipefail
DROP="/etc/ssh/sshd_config.d/shared_files_sftp.conf"
echo "--- drop-in ---"
sudo sed -n '1,120p' "$DROP" || true
echo
echo "--- dirs ---"
sudo ls -ld /srv/sftp/shared_files /srv/sftp/shared_files/shared /srv/sftp/shared_files/upload 2>/dev/null || true
echo
echo "--- sample files (upload) ---"
sudo ls -lah /srv/sftp/shared_files/upload | tail -n 20 || true
echo
echo "--- downloads link (ghost) ---"
for d in "/home/ghost/Téléchargements" "/home/ghost/Downloads"; do
  [[ -e "$d" ]] && ls -lah "$d/SHARED" 2>/dev/null || true
done
