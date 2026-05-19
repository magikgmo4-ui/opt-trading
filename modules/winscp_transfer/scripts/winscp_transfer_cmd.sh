#!/usr/bin/env bash
set -euo pipefail

BASE="/opt/trading/modules/winscp_transfer"
SHARE_BASE="${SHARE_BASE:-/srv/sftp/shared_files/shared}"
INBOX="${SHARE_BASE}/inbox"
OUTBOX="${SHARE_BASE}/outbox"
MODULES="${SHARE_BASE}/modules"
LOGS="${SHARE_BASE}/_logs"

DEFAULT_GROUP="${SFTP_GROUP:-sftp_shared_files}"

# Host defaults (override via env)
STUDENT_HOST_DEFAULT="student"
STUDENT_USER_DEFAULT="student"

ts() { date +"%Y-%m-%d %H:%M:%S"; }

usage() {
  cat <<'USAGE'
cmd-winscp_transfer

Usage:
  cmd-winscp_transfer init
  cmd-winscp_transfer ls [inbox|outbox|modules|logs]
  cmd-winscp_transfer send student <filename_or_path> [remote_dir]
  cmd-winscp_transfer deploy student <zipfile_in_inbox_or_path>
  cmd-winscp_transfer fetch student <remote_path> [outbox_subdir]
  cmd-winscp_transfer status
  cmd-winscp_transfer help

Env overrides:
  SHARE_BASE=/srv/sftp/shared_files/shared
  SFTP_GROUP=sftp_shared_files
  STUDENT_HOST=student
  STUDENT_USER=student
USAGE
}

need_sudo() {
  if [[ "${EUID}" -ne 0 ]]; then
    echo "ERROR: run with sudo for this action."
    exit 1
  fi
}

host_student() { echo "${STUDENT_HOST:-$STUDENT_HOST_DEFAULT}"; }
user_student() { echo "${STUDENT_USER:-$STUDENT_USER_DEFAULT}"; }

dir_for() {
  local which="${1:-inbox}"
  case "$which" in
    inbox) echo "$INBOX" ;;
    outbox) echo "$OUTBOX" ;;
    modules) echo "$MODULES" ;;
    logs) echo "$LOGS" ;;
    *) echo "" ;;
  esac
}

init_dirs() {
  need_sudo
  echo "[$(ts)] init: creating shared dirs under: $SHARE_BASE"
  mkdir -p "$INBOX" "$OUTBOX" "$MODULES" "$LOGS"

  # perms: group-writable + setgid on dirs
  for d in "$INBOX" "$OUTBOX" "$MODULES" "$LOGS"; do
    chgrp -R "$DEFAULT_GROUP" "$d" 2>/dev/null || true
    chmod 2775 "$d" || true
    find "$d" -type d -exec chmod 2775 {} + || true
    find "$d" -type f -exec chmod 0664 {} + || true
  done

  echo "OK: dirs ready."
  echo " - inbox  : $INBOX"
  echo " - outbox : $OUTBOX"
  echo " - modules: $MODULES"
  echo " - logs   : $LOGS"
}

ls_dir() {
  local which="${1:-inbox}"
  local d
  d="$(dir_for "$which")"
  if [[ -z "$d" ]]; then
    echo "ERROR: unknown dir '$which' (use inbox|outbox|modules|logs)"
    exit 1
  fi
  if [[ ! -d "$d" ]]; then
    echo "ERROR: missing dir: $d (run: sudo cmd-winscp_transfer init)"
    exit 1
  fi
  echo "[$(ts)] listing: $d"
  ls -lah --time-style=long-iso "$d" | sed -n '1,200p'
}

resolve_local_file() {
  local arg="${1:-}"
  if [[ -z "$arg" ]]; then
    echo ""
    return
  fi
  if [[ -f "$arg" ]]; then
    echo "$arg"
    return
  fi
  if [[ -f "$INBOX/$arg" ]]; then
    echo "$INBOX/$arg"
    return
  fi
  if [[ -f "$MODULES/$arg" ]]; then
    echo "$MODULES/$arg"
    return
  fi
  echo ""
}

send_student() {
  local file_arg="${1:-}"
  local remote_dir="${2:-/tmp}"
  local f
  f="$(resolve_local_file "$file_arg")"
  if [[ -z "$f" ]]; then
    echo "ERROR: file not found: '$file_arg' (try: inbox/<file>)"
    exit 1
  fi

  local host user
  host="$(host_student)"
  user="$(user_student)"

  echo "[$(ts)] sending to student: $f -> ${user}@${host}:${remote_dir}/"
  scp "$f" "${user}@${host}:${remote_dir}/"
  echo "OK: sent."
}

deploy_student_zip() {
  local zip_arg="${1:-}"
  local host user
  host="$(host_student)"
  user="$(user_student)"

  local z
  z="$(resolve_local_file "$zip_arg")"
  if [[ -z "$z" ]]; then
    echo "ERROR: zip not found: '$zip_arg'"
    exit 1
  fi

  local zname
  zname="$(basename "$z")"

  echo "[$(ts)] deploy: copying $zname to student:/tmp/"
  scp "$z" "${user}@${host}:/tmp/${zname}"

  echo "[$(ts)] deploy: running remote install (/tmp/<zip> -> /tmp/wst_push -> APPLY.sh)"
  # remote: unzip to /tmp/wst_push (unique folder) then run APPLY.sh if present
  ssh -t "${user}@${host}" bash -lc "set -euo pipefail; \
    d=/tmp/wst_push_\$(date +%Y%m%d_%H%M%S); mkdir -p \"\$d\"; \
    unzip -o \"/tmp/${zname}\" -d \"\$d\" >/dev/null; \
    if [[ -f \"\$d/APPLY.sh\" ]]; then sudo bash \"\$d/APPLY.sh\"; \
    else echo 'ERROR: APPLY.sh not found in zip root'; exit 2; fi"
  echo "OK: deployed."
}

fetch_student() {
  local remote_path="${1:-}"
  local outbox_sub="${2:-}"
  if [[ -z "$remote_path" ]]; then
    echo "ERROR: remote_path required (ex: /opt/trading/state/events.jsonl)"
    exit 1
  fi

  local host user
  host="$(host_student)"
  user="$(user_student)"

  local dest="$OUTBOX"
  if [[ -n "$outbox_sub" ]]; then
    dest="$OUTBOX/$outbox_sub"
    mkdir -p "$dest"
    chmod 2775 "$dest" || true
    chgrp "$DEFAULT_GROUP" "$dest" 2>/dev/null || true
  fi

  echo "[$(ts)] fetching from student: ${user}@${host}:${remote_path} -> ${dest}/"
  scp "${user}@${host}:${remote_path}" "$dest/"
  echo "OK: fetched. Check outbox."
}

status() {
  echo "== winscp_transfer status"
  echo "-- share base: $SHARE_BASE"
  echo "-- dirs:"
  for d in "$INBOX" "$OUTBOX" "$MODULES" "$LOGS"; do
    if [[ -d "$d" ]]; then
      echo "OK: $d"
    else
      echo "MISSING: $d"
    fi
  done
  echo "-- group: $DEFAULT_GROUP"
  echo "-- student host/user: $(host_student) / $(user_student)"
}

main() {
  local cmd="${1:-help}"
  shift || true
  case "$cmd" in
    init) init_dirs ;;
    ls) ls_dir "${1:-inbox}" ;;
    send)
      local target="${1:-}"
      shift || true
      if [[ "$target" != "student" ]]; then
        echo "ERROR: only 'student' target supported for now."
        exit 1
      fi
      send_student "${1:-}" "${2:-/tmp}"
      ;;
    deploy)
      local target="${1:-}"
      shift || true
      if [[ "$target" != "student" ]]; then
        echo "ERROR: only 'student' target supported for now."
        exit 1
      fi
      deploy_student_zip "${1:-}"
      ;;
    fetch)
      local target="${1:-}"
      shift || true
      if [[ "$target" != "student" ]]; then
        echo "ERROR: only 'student' target supported for now."
        exit 1
      fi
      fetch_student "${1:-}" "${2:-}"
      ;;
    status) status ;;
    help|-h|--help) usage ;;
    *)
      echo "Unknown command: $cmd"
      usage
      exit 1
      ;;
  esac
}

main "$@"
