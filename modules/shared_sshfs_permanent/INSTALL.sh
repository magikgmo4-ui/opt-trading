#!/usr/bin/env bash
set -euo pipefail

MODULE="shared_sshfs_permanent"
BASE="/opt/trading"
MOD_DIR="${BASE}/modules/${MODULE}"
SCRIPTS_DIR="${BASE}/scripts"
ENV_DIR="/etc/opt-trading"
ENV_FILE="${ENV_DIR}/shared_sshfs_permanent.env"
UNIT_FILE="/etc/systemd/system/shared-sshfs.service"
TEMPLATE="${MOD_DIR}/systemd/shared-sshfs.service.template"

die(){ echo "ERROR: $*" >&2; exit 1; }
need_root(){ [[ $EUID -eq 0 ]] || die "Run with sudo: sudo bash ${MOD_DIR}/INSTALL.sh"; }

need_root

# Determine local user/group (prefer sudo user)
LOCAL_USER="${SUDO_USER:-}"
if [[ -z "$LOCAL_USER" || "$LOCAL_USER" == "root" ]]; then
  LOCAL_USER="$(logname 2>/dev/null || true)"
fi
if [[ -z "$LOCAL_USER" || "$LOCAL_USER" == "root" ]]; then
  # last resort
  LOCAL_USER="$(id -un)"
fi

# If group sftp_shared_files exists, use it; else use user's primary group
if getent group sftp_shared_files >/dev/null 2>&1; then
  LOCAL_GROUP="sftp_shared_files"
else
  LOCAL_GROUP="$(id -gn "$LOCAL_USER" 2>/dev/null || id -gn)"
fi

echo "== Installing $MODULE =="
echo "Local user/group: ${LOCAL_USER}:${LOCAL_GROUP}"

# deps
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y sshfs fuse3

# allow_other
if [[ -f /etc/fuse.conf ]]; then
  grep -qE '^\s*user_allow_other\s*$' /etc/fuse.conf || echo "user_allow_other" >> /etc/fuse.conf
fi

# dirs
mkdir -p "$SCRIPTS_DIR" "$ENV_DIR" /shared

# permissions on mountpoint
chown "${LOCAL_USER}:${LOCAL_GROUP}" /shared
chmod 2775 /shared

# copy scripts to /opt/trading/scripts
install -m 0755 "${MOD_DIR}/scripts/shared_sshfs_permanent_menu.sh" "${SCRIPTS_DIR}/shared_sshfs_permanent_menu.sh"
install -m 0755 "${MOD_DIR}/scripts/shared_sshfs_permanent_cmd.sh"  "${SCRIPTS_DIR}/shared_sshfs_permanent_cmd.sh"
install -m 0755 "${MOD_DIR}/scripts/shared_sshfs_permanent_sanity.sh" "${SCRIPTS_DIR}/shared_sshfs_permanent_sanity.sh"
install -m 0755 "${MOD_DIR}/scripts/shared_sshfs_permanent_mount.sh" "${SCRIPTS_DIR}/shared_sshfs_permanent_mount.sh"
install -m 0755 "${MOD_DIR}/scripts/shared_sshfs_permanent_umount.sh" "${SCRIPTS_DIR}/shared_sshfs_permanent_umount.sh"

# wrappers
ln -sf "${SCRIPTS_DIR}/shared_sshfs_permanent_menu.sh"  /usr/local/bin/menu-shared_sshfs_permanent
ln -sf "${SCRIPTS_DIR}/shared_sshfs_permanent_cmd.sh"   /usr/local/bin/cmd-shared_sshfs_permanent
ln -sf "${SCRIPTS_DIR}/shared_sshfs_permanent_sanity.sh" /usr/local/bin/sanity-shared_sshfs_permanent

# env defaults (only create if missing)
if [[ ! -f "$ENV_FILE" ]]; then
  cat > "$ENV_FILE" <<EOF
# shared_sshfs_permanent.env
# Remote share hosted on admin-trading
REMOTE_HOST=admin-trading
REMOTE_USER=ghost
REMOTE_PATH=/srv/sftp/shared_files/shared

# Local mount
MOUNT_POINT=/shared
LOCAL_USER=${LOCAL_USER}
LOCAL_GROUP=${LOCAL_GROUP}

# SSH
SSH_PORT=22
IDENTITY_FILE=/home/${LOCAL_USER}/.ssh/id_ed25519

# Extra sshfs opts (optional): comma-separated list WITHOUT spaces
# Example: SSHFS_OPTS="cache=yes,kernel_cache"
SSHFS_OPTS=
EOF
  chmod 0644 "$ENV_FILE"
  echo "Wrote $ENV_FILE"
else
  echo "Keeping existing config: $ENV_FILE"
fi

# unit from template with concrete user/group
[[ -f "$TEMPLATE" ]] || die "missing template: $TEMPLATE"
sed -e "s/{{LOCAL_USER}}/${LOCAL_USER}/g" -e "s/{{LOCAL_GROUP}}/${LOCAL_GROUP}/g" "$TEMPLATE" > "$UNIT_FILE"

systemctl daemon-reload
systemctl enable "$UNIT_FILE" >/dev/null 2>&1 || true

echo
echo "OK: installed wrappers:"
echo "  menu-shared_sshfs_permanent"
echo "  cmd-shared_sshfs_permanent"
echo "  sanity-shared_sshfs_permanent"
echo
echo "Next:"
echo "  sanity-shared_sshfs_permanent || true"
echo "  sudo cmd-shared_sshfs_permanent mount"
