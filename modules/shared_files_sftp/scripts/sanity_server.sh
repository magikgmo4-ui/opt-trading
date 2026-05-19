#!/usr/bin/env bash
set -euo pipefail
DROP="/etc/ssh/sshd_config.d/shared_files_sftp.conf"

echo "HOST=$(hostname)"
echo "OK: drop-in exists? $(test -f "$DROP" && echo yes || echo no)"
echo "OK: sshd -t ..."
sudo sshd -t && echo "OK: sshd config valid"

echo "--- ForceCommand line ---"
grep -nE 'ForceCommand' "$DROP" || true

echo "--- directories ---"
sudo test -d /srv/sftp/shared_files/shared && echo "OK: shared dir exists"
sudo test -d /srv/sftp/shared_files/upload && echo "OK: upload dir exists"

echo "--- perms ---"
sudo ls -ld /srv/sftp/shared_files/shared /srv/sftp/shared_files/upload 2>/dev/null || true

echo "PASS: server sanity"
