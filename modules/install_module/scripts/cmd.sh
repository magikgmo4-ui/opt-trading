#!/usr/bin/env bash
set -euo pipefail

# install_module: install zip/tgz packages from a shared folder and (optionally) sync/validate git + shortcuts.

ROOT="${ROOT:-/opt/trading}"
# Prefer /shared if present (nice shortcut). Otherwise default to SFTP shared path.
if [[ -z "${SHARED_DIR:-}" ]]; then
  if [[ -d "/shared" ]]; then
    SHARED_DIR="/shared"
  else
    SHARED_DIR="/srv/sftp/shared_files/shared"
  fi
else
  SHARED_DIR="$SHARED_DIR"
fi
LOGDIR="${LOGDIR:-$ROOT/journal/tmp}"
mkdir -p "$LOGDIR" || true

ts() { date +"%Y%m%d_%H%M%S"; }
logfile() { echo "$LOGDIR/install_module_$(ts).log"; }

die() { echo "ERROR: $*" >&2; exit 1; }

usage() {
  cat <<'USAGE'
Usage:
  cmd-install_module list
  cmd-install_module list_packages        # alias of list
  cmd-install_module install <num|file> [--sudo]
  cmd-install_module apply   <num|file> [--sudo]     # force patch mode (APPLY_*.sh)

  cmd-install_module sync_validate        # local: git pull + sanity + bootstrap shortcuts
  cmd-install_module sync_all             # admin-trading: git push + pull on student/db-layer + bootstrap

  cmd-install_module paths
  cmd-install_module help

Env overrides:
  ROOT=/opt/trading
  SHARED_DIR=/shared   (or /srv/sftp/shared_files/shared)
  LOGDIR=/opt/trading/journal/tmp
USAGE
}

pkg_candidates() {
  [[ -d "$SHARED_DIR" ]] || die "SHARED_DIR not found: $SHARED_DIR"
  find "$SHARED_DIR" -maxdepth 1 -type f \( -iname "*.zip" -o -iname "*.tgz" -o -iname "*.tar.gz" \) -printf "%T@ %p\n" \
    | sort -nr | awk '{ $1=""; sub(/^ /,""); print }'
}

list_pkgs() {
  local i=0
  while IFS= read -r f; do
    [[ -n "$f" ]] || continue
    i=$((i+1))
    printf "%2d) %s\n" "$i" "$(basename "$f")"
  done < <(pkg_candidates)
  echo "count=$i"
}

resolve_pkg() {
  local sel="${1:-}"
  [[ -n "$sel" ]] || die "missing package selector (num|filename)"

  if [[ "$sel" =~ ^[0-9]+$ ]]; then
    local n="$sel"
    [[ "$n" -ge 1 ]] || die "invalid number (use 1..N)"
    local f
    f="$(pkg_candidates | sed -n "${n}p")"
    [[ -n "${f:-}" ]] || die "no package at index $n"
    echo "$f"
    return 0
  fi

  if [[ -f "$sel" ]]; then echo "$sel"; return 0; fi
  if [[ -f "$SHARED_DIR/$sel" ]]; then echo "$SHARED_DIR/$sel"; return 0; fi

  die "package not found: $sel (in $SHARED_DIR)"
}

zip_list() { unzip -Z1 "$1" 2>/dev/null || true; }

detect_patch_script() {
  local lst s
  lst="$(zip_list "$1")"
  s="$(printf "%s\n" "$lst" | grep -E '(^|/)(APPLY_PATCH\.sh|APPLY_FIX\.sh|APPLY_.*\.sh)$' | head -n 1 || true)"
  [[ -n "$s" ]] && echo "$s" || return 1
}

is_patch_pkg() { detect_patch_script "$1" >/dev/null 2>&1; }

unpack_to_tmp() {
  local pkg="$1"
  local out="/tmp/install_module_$(ts)_$RANDOM"
  mkdir -p "$out"
  if [[ "$pkg" =~ \.zip$ ]]; then
    unzip -o "$pkg" -d "$out" >/dev/null
  else
    tar -xzf "$pkg" -C "$out"
  fi
  echo "$out"
}

run_patch() {
  local pkg="$1"; local tmp rel script
  tmp="$(unpack_to_tmp "$pkg")"
  rel="$(detect_patch_script "$pkg" || true)"
  [[ -n "$rel" ]] || die "could not find APPLY_*.sh in package"
  script="$tmp/$rel"
  [[ -f "$script" ]] || die "patch script missing after unpack: $script"
  echo "=== patch mode ==="
  echo "tmp=$tmp"
  echo "script=$script"
  ( cd "$ROOT" && bash "$script" )
  echo "OK: patch applied"
}

run_install_like_you_do() {
  local pkg="$1"; local do_sudo="${2:-0}"
  echo "=== install mode (classic) ==="
  echo "ROOT=$ROOT"
  echo "PKG=$pkg"
  [[ -d "$ROOT" ]] || die "ROOT not found: $ROOT"

  ( cd "$ROOT" && unzip -o "$pkg" >/dev/null )
  if [[ -f "$ROOT/INSTALL.sh" ]]; then
    ( cd "$ROOT" && bash "$ROOT/INSTALL.sh" )
  else
    echo "WARN: INSTALL.sh not found at $ROOT/INSTALL.sh (package may be patch-like or structured differently)."
  fi

  local lst modules
  lst="$(zip_list "$pkg")"
  modules="$(printf "%s\n" "$lst" | sed -n 's|^modules/\([^/]\+\)/.*|\1|p' | sort -u || true)"

  if [[ -n "${modules:-}" ]]; then
    echo "Detected modules in package:"
    printf "%s\n" "$modules" | sed 's/^/ - /'
    while IFS= read -r m; do
      [[ -n "$m" ]] || continue
      if [[ -x "$ROOT/modules/$m/scripts/sanity_check.sh" ]]; then
        echo "--- sanity: $m ---"
        "$ROOT/modules/$m/scripts/sanity_check.sh" || true
      fi
      if [[ "$do_sudo" == "1" && -x "$ROOT/modules/$m/scripts/install_shortcuts.sh" ]]; then
        echo "--- shortcuts (sudo): $m ---"
        sudo "$ROOT/modules/$m/scripts/install_shortcuts.sh" || true
      fi
    done <<< "$modules"
  else
    echo "NOTE: no modules/ detected in package list."
  fi

  echo "OK: install flow finished"
}

run_sanity_if_exists() {
  local p="$1"; shift || true
  [[ -x "$p" ]] || return 0
  echo "--- sanity: $(basename "$(dirname "$(dirname "$p")")") ---"
  "$p" "$@" || true
}

bootstrap_shortcuts() {
  # Ensure ops hub shortcuts exist, then create standard shortcuts for modules with scripts/
  if [[ -x "$ROOT/modules/ops_menu_hub/scripts/install_shortcuts.sh" ]]; then
    sudo "$ROOT/modules/ops_menu_hub/scripts/install_shortcuts.sh" || true
  fi
  if [[ -x "$ROOT/modules/ops_menu_hub/scripts/cmd.sh" ]]; then
    sudo "$ROOT/modules/ops_menu_hub/scripts/cmd.sh" bootstrap_shortcuts || true
  else
    echo "WARN: ops_menu_hub not present; cannot bootstrap shortcuts automatically."
  fi
}

sync_validate_local() {
  echo "=== sync_validate (local) ==="
  ( cd "$ROOT" && git pull --ff-only )

  run_sanity_if_exists "$ROOT/modules/ops_super_menu/scripts/sanity_check.sh"
  run_sanity_if_exists "$ROOT/modules/ops_wrappers/scripts/sanity_check.sh"
  run_sanity_if_exists "$ROOT/modules/install_module/scripts/sanity_check.sh"

  bootstrap_shortcuts
  echo "OK: sync_validate done"
}

ssh_try() {
  local host="$1"; shift || true
  ssh -o BatchMode=yes -o ConnectTimeout=3 "$host" "$@" 2>/dev/null
}

sync_all_admin() {
  echo "=== sync_all (admin-trading) ==="
  ( cd "$ROOT" && git push )

  local targets=("student" "db-layer")
  for h in "${targets[@]}"; do
    if ssh_try "$h" "true"; then
      echo "--- $h: git pull + bootstrap ---"
      ssh "$h" "cd /opt/trading && git pull --ff-only" || true
      ssh "$h" "sudo /opt/trading/modules/ops_menu_hub/scripts/install_shortcuts.sh" || true
      ssh "$h" "sudo /opt/trading/modules/ops_menu_hub/scripts/cmd.sh bootstrap_shortcuts" || true
    else
      echo "WARN: cannot SSH to $h (skipping)."
    fi
  done

  echo "OK: sync_all done"
}

main() {
  local sub="${1:-help}"; shift || true
  case "$sub" in
    help|-h|--help) usage ;;
    paths)
      echo "ROOT=$ROOT"
      echo "SHARED_DIR=$SHARED_DIR"
      echo "LOGDIR=$LOGDIR"
      ;;
    list|list_packages) list_pkgs ;;
    install|apply)
      local sel="${1:-}"; shift || true
      local do_sudo=0
      if [[ "${1:-}" == "--sudo" ]]; then do_sudo=1; fi
      local pkg; pkg="$(resolve_pkg "$sel")"
      local lf; lf="$(logfile)"
      echo "LOG=$lf"
      {
        echo "host=$(hostname) ts=$(date -Iseconds)"
        echo "cmd=$sub sel=$sel pkg=$pkg sudo=$do_sudo"
        echo
        if [[ "$sub" == "apply" ]]; then
          run_patch "$pkg"
        else
          if is_patch_pkg "$pkg"; then run_patch "$pkg"; else run_install_like_you_do "$pkg" "$do_sudo"; fi
        fi
      } 2>&1 | tee "$lf"
      ;;
    sync_validate) sync_validate_local ;;
    sync_all) sync_all_admin ;;
    *) usage; die "unknown subcommand: $sub" ;;
  esac
}

main "$@"
