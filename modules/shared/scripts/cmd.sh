#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT_PATH="$(readlink -f "$SCRIPT_PATH" 2>/dev/null || echo "$SCRIPT_PATH")"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"

ts() { date +"%Y-%m-%d %H:%M:%S"; }

die() { echo "ERROR: $*" >&2; exit 1; }

usage() {
  cat <<'USAGE'
cmd-shared

Usage:
  cmd-shared ls [<relpath>]
  cmd-shared get [--dry-run] [--force] <relpath> [<dest>]
  cmd-shared put [--dry-run] [--force] <src> [<relpath|dir>]
  cmd-shared cat <relpath>
  cmd-shared status
  cmd-shared path
  cmd-shared help

Notes:
  - relpath is relative to shared root (no leading "/"; no "..").
  - Default shared root is /shared if present; else /srv/sftp/shared_files/shared.
USAGE
}

default_share_base() {
  if [[ -n "${SHARE_BASE:-}" ]]; then
    echo "$SHARE_BASE"
    return
  fi
  if [[ -d "/shared" ]]; then
    echo "/shared"
    return
  fi
  if [[ -d "/srv/sftp/shared_files/shared" ]]; then
    echo "/srv/sftp/shared_files/shared"
    return
  fi
  echo ""
}

require_share_base() {
  local b
  b="$(default_share_base)"
  [[ -z "$b" ]] && die "shared root not found (set SHARE_BASE or ensure /shared exists)."
  [[ -d "$b" ]] || die "shared root is not a directory: $b"
  echo "$b"
}

normalize_relpath() {
  local p="${1:-}"
  [[ -z "$p" ]] && die "path required"
  p="${p#./}"
  [[ "$p" == /* ]] && die "relpath must not start with '/': $p"
  [[ "$p" == *".."* ]] && die "relpath must not contain '..': $p"
  echo "$p"
}

cp_file() {
  local force="${1:-0}"; shift || true
  local src="${1:-}"; shift || true
  local dst="${1:-}"; shift || true
  if [[ "$force" -eq 1 ]]; then
    cp -f -- "$src" "$dst"
  else
    cp -n -- "$src" "$dst"
  fi
}

cmd_path() {
  local b
  b="$(require_share_base)"
  echo "share_base=$b"
  if command -v hostname >/dev/null 2>&1; then
    echo "host=$(hostname)"
  fi
  if command -v whoami >/dev/null 2>&1; then
    echo "user=$(whoami)"
  fi
}

cmd_ls() {
  local b rel target
  b="$(require_share_base)"
  rel="${1:-}"
  if [[ -z "$rel" ]]; then
    target="$b"
  else
    rel="$(normalize_relpath "$rel")"
    target="$b/$rel"
  fi

  echo "[$(ts)] ls: $target"
  if [[ -d "$target" ]]; then
    ls -lah --time-style=long-iso "$target" | sed -n '1,220p'
    return
  fi
  if [[ -f "$target" ]]; then
    ls -lah --time-style=long-iso "$target"
    return
  fi
  die "not found: $target"
}

cmd_cat() {
  local b rel p
  b="$(require_share_base)"
  rel="$(normalize_relpath "${1:-}")"
  p="$b/$rel"
  [[ -f "$p" ]] || die "not a file: $p"
  sed -n '1,260p' "$p"
}

cmd_get() {
  local dry=0 force=0
  while [[ "${1:-}" == --* ]]; do
    case "${1:-}" in
      --dry-run) dry=1; shift ;;
      --force) force=1; shift ;;
      *) die "unknown flag: ${1:-}" ;;
    esac
  done

  local rel dest b src base out
  rel="$(normalize_relpath "${1:-}")"
  dest="${2:-.}"
  b="$(require_share_base)"
  src="$b/$rel"
  [[ -f "$src" ]] || die "not a file: $src"

  if [[ -d "$dest" || "$dest" == */ ]]; then
    base="$(basename "$rel")"
    out="${dest%/}/$base"
  else
    out="$dest"
  fi

  echo "[$(ts)] get: $src -> $out"
  if [[ "$dry" -eq 1 ]]; then
    echo "DRY_RUN=1"
    return
  fi

  mkdir -p "$(dirname "$out")"
  cp_file "$force" "$src" "$out"
  echo "OK"
}

cmd_put() {
  local dry=0 force=0
  while [[ "${1:-}" == --* ]]; do
    case "${1:-}" in
      --dry-run) dry=1; shift ;;
      --force) force=1; shift ;;
      *) die "unknown flag: ${1:-}" ;;
    esac
  done

  local src_arg="${1:-}"
  [[ -n "$src_arg" ]] || die "src required"
  [[ -f "$src_arg" ]] || die "src not found: $src_arg"

  local dst_rel="${2:-}"
  local b dst
  b="$(require_share_base)"

  if [[ -z "$dst_rel" ]]; then
    dst="$b/$(basename "$src_arg")"
  else
    dst_rel="${dst_rel#./}"
    [[ "$dst_rel" == *".."* ]] && die "destination relpath must not contain '..': $dst_rel"
    if [[ "$dst_rel" == /* ]]; then
      die "destination must be relative to shared root (no leading '/'): $dst_rel"
    fi
    if [[ "$dst_rel" == */ ]]; then
      dst="$b/${dst_rel%/}/$(basename "$src_arg")"
    else
      dst="$b/$dst_rel"
      if [[ -d "$dst" ]]; then
        dst="$dst/$(basename "$src_arg")"
      fi
    fi
  fi

  echo "[$(ts)] put: $src_arg -> $dst"
  if [[ "$dry" -eq 1 ]]; then
    echo "DRY_RUN=1"
    return
  fi

  mkdir -p "$(dirname "$dst")"
  cp_file "$force" "$src_arg" "$dst"
  echo "OK"
}

cmd_status() {
  local b
  b="$(require_share_base)"
  echo "== shared status"
  echo "-- share_base: $b"
  echo "-- subdirs:"
  for d in _bundles _ops _refs _archives inbox outbox modules _logs vision_inbox vision_outbox vision_processed desk_pro documents windows _git_archives; do
    if [[ -d "$b/$d" ]]; then
      echo "OK: $d"
    else
      echo "MISSING: $d"
    fi
  done
  echo "-- root files:"
  find "$b" -maxdepth 1 -mindepth 1 -type f -printf "%f\n" | sort | sed -n '1,220p'
}

CMD="${1:-}"
shift || true

case "$CMD" in
  ls) cmd_ls "${1:-}" ;;
  get) cmd_get "$@" ;;
  put) cmd_put "$@" ;;
  cat) cmd_cat "${1:-}" ;;
  status) cmd_status ;;
  path) cmd_path ;;
  help|-h|--help|"") usage ;;
  *) echo "Unknown: $CMD" >&2; usage; exit 2 ;;
esac

