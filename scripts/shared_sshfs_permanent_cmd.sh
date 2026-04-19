#!/usr/bin/env bash
set -euo pipefail

MODULE="shared_sshfs_permanent"
ENV_FILE="/etc/opt-trading/shared_sshfs_permanent.env"
SERVICE="shared-sshfs.service"
MOUNT_SCRIPT="/opt/trading/scripts/shared_sshfs_permanent_mount.sh"
UMOUNT_SCRIPT="/opt/trading/scripts/shared_sshfs_permanent_umount.sh"

die(){ echo "ERROR: $*" >&2; exit 1; }

need_root_for() {
  local action="$1"
  if [[ $EUID -ne 0 ]]; then
    die "Command '$action' needs sudo. Example: sudo cmd-${MODULE} ${action}"
  fi
}

load_env() {
  if [[ -f "$ENV_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$ENV_FILE"
  fi
}

usage() {
  cat <<EOF
cmd-${MODULE} <action>

Actions:
  status          Show systemd status + mount status
  mount           Start (enable) the systemd service
  umount          Stop the systemd service + unmount
  restart         Restart the systemd service
  logs            Show last 200 lines of service logs
  test-ssh        Test SSH connectivity to remote
  ls              List top of mountpoint
  edit-config     Edit ${ENV_FILE}
  print-config    Print parsed config
EOF
}

action="${1:-}"
[[ -z "$action" ]] && { usage; exit 0; }

case "$action" in
  status)
    load_env
    echo "Service: $SERVICE"
    systemctl status "$SERVICE" --no-pager || true
    echo
    if mountpoint -q "${MOUNT_POINT:-/shared}"; then
      echo "OK: mounted at ${MOUNT_POINT:-/shared}"
      df -hT "${MOUNT_POINT:-/shared}" || true
    else
      echo "WARN: not mounted at ${MOUNT_POINT:-/shared}"
    fi
    ;;
  mount)
    need_root_for "mount"
    systemctl enable --now "$SERVICE"
    systemctl status "$SERVICE" --no-pager || true
    ;;
  umount)
    need_root_for "umount"
    systemctl stop "$SERVICE" || true
    bash "$UMOUNT_SCRIPT" || true
    ;;
  restart)
    need_root_for "restart"
    systemctl restart "$SERVICE"
    systemctl status "$SERVICE" --no-pager || true
    ;;
  logs)
    journalctl -u "$SERVICE" -n 200 --no-pager || true
    ;;
  test-ssh)
    load_env
    local_user="${LOCAL_USER:-$(id -un)}"
    id_file="${IDENTITY_FILE:-/home/${local_user}/.ssh/id_ed25519}"
    host="${REMOTE_HOST:-admin-trading}"
    ruser="${REMOTE_USER:-ghost}"
    port="${SSH_PORT:-22}"
    echo "Testing SSH: ${ruser}@${host} (port ${port}) using key ${id_file}"
    ssh -p "$port" -i "$id_file" -o BatchMode=yes -o ConnectTimeout=7 -o StrictHostKeyChecking=accept-new "${ruser}@${host}" "echo OK && hostname && id" 
    ;;
  ls)
    load_env
    mp="${MOUNT_POINT:-/shared}"
    ls -lah "$mp" | head -n 80
    ;;
  edit-config)
    need_root_for "edit-config"
    ${EDITOR:-nano} "$ENV_FILE"
    ;;
  print-config)
    load_env
    echo "ENV_FILE=$ENV_FILE"
    echo "REMOTE_HOST=${REMOTE_HOST:-admin-trading}"
    echo "REMOTE_USER=${REMOTE_USER:-ghost}"
    echo "REMOTE_PATH=${REMOTE_PATH:-/srv/sftp/shared_files/shared}"
    echo "MOUNT_POINT=${MOUNT_POINT:-/shared}"
    echo "LOCAL_USER=${LOCAL_USER:-$(id -un)}"
    echo "LOCAL_GROUP=${LOCAL_GROUP:-$(id -gn)}"
    echo "SSH_PORT=${SSH_PORT:-22}"
    echo "IDENTITY_FILE=${IDENTITY_FILE:-}"
    echo "SSHFS_OPTS=${SSHFS_OPTS:-}"
    ;;
  *)
    usage
    exit 2
    ;;
esac
