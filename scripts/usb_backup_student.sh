\
#!/usr/bin/env bash
set -euo pipefail
MNT="/mnt/usb"
BASE="/opt/trading"
TS="$(date +%Y%m%d_%H%M%S)"
DEST="$MNT/student_backup_$TS"

if ! mountpoint -q "$MNT"; then
  echo "ERROR: $MNT is not mounted. Mount your USB first."
  echo "Hint: lsblk -f ; then sudo mount /dev/sdX1 $MNT"
  exit 1
fi

sudo mkdir -p "$DEST"
sudo chown -R "$USER":"$USER" "$DEST"

echo "Backing up to: $DEST"

# Copy core data
rsync -a --delete "$BASE/journal/" "$DEST/journal/"
rsync -a --delete "$BASE/archive/" "$DEST/archive/" || true
rsync -a --delete "$BASE/ingest/" "$DEST/ingest/" || true

# Exclude venv to keep backup small (can be recreated)
rm -rf "$DEST/ingest/venv" 2>/dev/null || true

# System snapshots
mkdir -p "$DEST/system"
uname -a > "$DEST/system/uname.txt"
date -Is > "$DEST/system/backup_time.txt"
hostnamectl > "$DEST/system/hostnamectl.txt" 2>/dev/null || true
ip -br a > "$DEST/system/ip.txt"
df -h > "$DEST/system/df.txt"
lsblk > "$DEST/system/lsblk.txt"
sudo vgs > "$DEST/system/vgs.txt"
sudo lvs > "$DEST/system/lvs.txt"
sudo ufw status verbose > "$DEST/system/ufw_status.txt" 2>/dev/null || true
systemctl status student-watchdrop --no-pager > "$DEST/system/watchdrop_status.txt" 2>/dev/null || true
systemctl status student-ingest --no-pager > "$DEST/system/ingest_status.txt" 2>/dev/null || true

# Manifest
( cd "$DEST" && find . -type f -maxdepth 3 -print0 | xargs -0 sha256sum ) > "$DEST/manifest.sha256"

echo "OK: Backup complete."
echo "Manifest: $DEST/manifest.sha256"
