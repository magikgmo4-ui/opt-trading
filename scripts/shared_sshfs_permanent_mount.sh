#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="/etc/opt-trading/shared_sshfs_permanent.env"
[[ -f "$ENV_FILE" ]] || { echo "missing $ENV_FILE"; exit 1; }
# shellcheck disable=SC1090
source "$ENV_FILE"

REMOTE_HOST="${REMOTE_HOST:-admin-trading}"
REMOTE_USER="${REMOTE_USER:-ghost}"
REMOTE_PATH="${REMOTE_PATH:-/srv/sftp/shared_files/shared}"
MOUNT_POINT="${MOUNT_POINT:-/shared}"
SSH_PORT="${SSH_PORT:-22}"
LOCAL_USER="${LOCAL_USER:-$(id -un)}"
LOCAL_GROUP="${LOCAL_GROUP:-$(id -gn)}"

uid="$(id -u "$LOCAL_USER" 2>/dev/null || id -u)"
gid="$(getent group "$LOCAL_GROUP" >/dev/null 2>&1 && getent group "$LOCAL_GROUP" | awk -F: '{print $3}' || id -g)"

if [[ -z "${IDENTITY_FILE:-}" ]]; then
  IDENTITY_FILE="/home/${LOCAL_USER}/.ssh/id_ed25519"
fi

# Ensure mountpoint
mkdir -p "$MOUNT_POINT"

# If already mounted, do nothing
if mountpoint -q "$MOUNT_POINT"; then
  echo "already mounted: $MOUNT_POINT"
  exit 0
fi

# Build options
# Note: allow_other requires /etc/fuse.conf with user_allow_other
BASE_OPTS=(
  "reconnect"
  "ServerAliveInterval=15"
  "ServerAliveCountMax=3"
  "StrictHostKeyChecking=accept-new"
  "UserKnownHostsFile=/home/${LOCAL_USER}/.ssh/known_hosts"
  "IdentityFile=${IDENTITY_FILE}"
  "allow_other"
  "default_permissions"
  "idmap=user"
  "uid=${uid}"
  "gid=${gid}"
)

# Allow override/extra opts
EXTRA="${SSHFS_OPTS:-}"
echo "Mounting SSHFS: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH} -> ${MOUNT_POINT}"
echo "Local user/group: ${LOCAL_USER}:${LOCAL_GROUP} (uid=${uid} gid=${gid})"
echo "Key: ${IDENTITY_FILE}  Port: ${SSH_PORT}"
echo "Extra opts: ${EXTRA}"

# Convert opts to -o form
opts_args=()
for o in "${BASE_OPTS[@]}"; do
  opts_args+=("-o" "$o")
done

# sshfs in foreground for systemd Type=simple
exec /usr/bin/sshfs -f -p "$SSH_PORT" "${opts_args[@]}" ${EXTRA:+-o "$EXTRA"} \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}" "$MOUNT_POINT"
