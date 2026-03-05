#!/usr/bin/env bash
set -euo pipefail

# install_module - command helper for /shared zips + sync/validate workflow.
# This script is meant to be reachable via /usr/local/bin/cmd-install_module

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MOD_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"              # /opt/trading/modules/install_module
ROOT_DIR="$(cd "${MOD_DIR}/../.." && pwd)"            # /opt/trading

SHARED_DIR_DEFAULT="/srv/sftp/shared_files/shared"

usage() {
  cat <<'USAGE'
cmd-install_module — helpers for installing zips from /shared and syncing machines.

Usage:
  cmd-install_module help
  cmd-install_module shared_list [--dir DIR]
  cmd-install_module install_zip <zip_name_or_path> [--dir DIR]
    - Unzips into /opt/trading and runs ./INSTALL.sh if present.

  cmd-install_module apply_patch_zip <zip_name_or_path> [--dir DIR]
    - Unzips into /tmp and runs APPLY_PATCH.sh / APPLY_FIX.sh if present.
      (Use this for patch zips that contain their own apply script.)

  cmd-install_module sync_validate --hosts "student db-layer" [--auto-commit] [--commit "msg"] [--allow-dirty]
    - On this machine: optionally auto-commit+push, then pulls on remote hosts.

Examples:
  cmd-install_module shared_list
  cmd-install_module install_zip ops_super_menu_step0.zip
  cmd-install_module apply_patch_zip ops_super_menu_numbered_patch.zip
  cmd-install_module sync_validate --hosts "student db-layer" --auto-commit --commit "sync: update modules"
USAGE
}

die() { echo "ERROR: $*" >&2; exit 1; }
log() { echo "$*"; }

shared_list() {
  local dir="$SHARED_DIR_DEFAULT"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) dir="${2:-}"; shift 2;;
      *) die "unknown arg: $1";;
    esac
  done
  [[ -d "$dir" ]] || die "shared dir not found: $dir"
  ls -lah "$dir" | sed -n '1,200p'
}

resolve_zip() {
  local arg="$1"
  local dir="$2"
  if [[ -f "$arg" ]]; then
    echo "$arg"
  elif [[ -f "${dir}/${arg}" ]]; then
    echo "${dir}/${arg}"
  else
    die "zip not found: $arg (also checked ${dir}/${arg})"
  fi
}

install_zip() {
  local arg="${1:-}"; shift || true
  [[ -n "$arg" ]] || die "install_zip requires zip name/path"
  local dir="$SHARED_DIR_DEFAULT"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) dir="${2:-}"; shift 2;;
      *) die "unknown arg: $1";;
    esac
  done

  local zip_path
  zip_path="$(resolve_zip "$arg" "$dir")"
  log "Using zip: $zip_path"
  cd "$ROOT_DIR" || exit 1
  unzip -o "$zip_path"
  if [[ -f "$ROOT_DIR/INSTALL.sh" ]]; then
    bash "$ROOT_DIR/INSTALL.sh"
  elif [[ -f "$ROOT_DIR/modules/$(basename "$zip_path" .zip)/INSTALL.sh" ]]; then
    bash "$ROOT_DIR/modules/$(basename "$zip_path" .zip)/INSTALL.sh"
  fi
  log "OK: install_zip done."
}

apply_patch_zip() {
  local arg="${1:-}"; shift || true
  [[ -n "$arg" ]] || die "apply_patch_zip requires zip name/path"
  local dir="$SHARED_DIR_DEFAULT"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) dir="${2:-}"; shift 2;;
      *) die "unknown arg: $1";;
    esac
  done

  local zip_path
  zip_path="$(resolve_zip "$arg" "$dir")"
  log "Using patch zip: $zip_path"

  local tmp="/tmp/install_module_patch_$(date +%Y%m%d_%H%M%S)"
  mkdir -p "$tmp"
  unzip -o "$zip_path" -d "$tmp"

  if [[ -f "$tmp/APPLY_PATCH.sh" ]]; then
    bash "$tmp/APPLY_PATCH.sh"
  elif [[ -f "$tmp/APPLY_FIX.sh" ]]; then
    bash "$tmp/APPLY_FIX.sh"
  else
    die "No APPLY_PATCH.sh or APPLY_FIX.sh found in $zip_path"
  fi
  log "OK: apply_patch_zip done."
}

sync_validate() {
  local hosts=""
  local auto_commit=0
  local allow_dirty=0
  local commit_msg="sync: update modules"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --hosts) hosts="${2:-}"; shift 2;;
      --auto-commit) auto_commit=1; shift;;
      --allow-dirty) allow_dirty=1; shift;;
      --commit) commit_msg="${2:-}"; shift 2;;
      *) die "unknown arg: $1";;
    esac
  done

  [[ -n "$hosts" ]] || die "sync_validate requires --hosts "student db-layer""

  cd "$ROOT_DIR" || exit 1

  if [[ $auto_commit -eq 1 ]]; then
    if [[ $allow_dirty -eq 0 ]]; then
      git diff --quiet || die "Working tree dirty. Use --allow-dirty or commit manually."
    fi
    git add -A
    git commit -m "$commit_msg" || true
    git push
  fi

  for h in $hosts; do
    log "---- remote: $h ----"
    ssh "$h" "cd /opt/trading && git pull --ff-only && echo OK:$h"
  done
  log "OK: sync_validate done."
}

cmd="${1:-help}"; shift || true
case "$cmd" in
  help|-h|--help) usage;;
  shared_list) shared_list "$@";;
  install_zip) install_zip "$@";;
  apply_patch_zip) apply_patch_zip "$@";;
  sync_validate) sync_validate "$@";;
  *) die "unknown command: $cmd (try: cmd-install_module help)";;
esac
