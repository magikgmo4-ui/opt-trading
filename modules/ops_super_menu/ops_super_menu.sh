#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/opt/trading}"
MODS="$ROOT/modules"
SCRIPTS="$ROOT/scripts"
BIN="/usr/local/bin"

host="$(hostname)"
role="unknown"
case "$host" in
  admin-trading) role="admin-trading (headless)";;
  student) role="student (headless)";;
  db-layer) role="db-layer (MSI Ubuntu GUI)";;
  cursor-ai) role="cursor-ai (Windows dev box)";;
esac

ts="$(date +%Y%m%d_%H%M%S)"

list_shortcuts() {
  local g="$1"
  shopt -s nullglob
  local arr=($BIN/$g)
  shopt -u nullglob
  if [ ${#arr[@]} -eq 0 ]; then
    echo "(none)"
    return 0
  fi
  for p in "${arr[@]}"; do
    local name; name="$(basename "$p")"
    local link target
    link="$(readlink "$p" 2>/dev/null || true)"
    target="$(readlink -f "$p" 2>/dev/null || true)"
    if [ -z "$link" ]; then
      echo "FILE:   $name"
    elif [ -z "$target" ] || [ ! -e "$target" ]; then
      echo "BROKEN: $name -> $link"
    else
      echo "OK:     $name -> $target"
    fi
  done | sort
}

has_menu_shortcut_for_module() {
  local m="$1"
  [ -e "$BIN/menu-$m" ]
}

discover_module_entry() {
  local m="$1"
  local base="$MODS/$m"
  local scripts="$base/scripts"
  if [ -f "$scripts/menu.sh" ]; then
    echo "standard|$scripts/menu.sh"; return 0
  fi
  local legacy=""
  legacy="$(ls -1 "$scripts"/*_menu.sh 2>/dev/null | head -n 1 || true)"
  if [ -n "$legacy" ]; then
    echo "legacy|$legacy"; return 0
  fi
  legacy="$(ls -1 "$scripts"/menu_*.sh 2>/dev/null | head -n 1 || true)"
  if [ -n "$legacy" ]; then
    echo "legacy|$legacy"; return 0
  fi
  echo "none|"
}

list_modules() {
  if [ ! -d "$MODS" ]; then
    echo "ERROR: missing $MODS"
    return 2
  fi
  for d in "$MODS"/*; do
    [ -d "$d" ] || continue
    local m; m="$(basename "$d")"
    [[ "$m" == "__pycache__" ]] && continue

    local out typ entry
    out="$(discover_module_entry "$m")"
    typ="${out%%|*}"
    entry="${out#*|}"
    local shc="no"
    if has_menu_shortcut_for_module "$m"; then shc="yes"; fi

    if [ "$typ" = "standard" ]; then
      echo "STD   $m  shortcut=$shc  entry=$entry"
    elif [ "$typ" = "legacy" ]; then
      echo "LEG   $m  shortcut=$shc  entry=$entry"
    else
      echo "NONE  $m  shortcut=$shc"
    fi
  done | sort
}

list_modules_none() {
  list_modules | awk '$1=="NONE"{print}'
}

list_modules_none_actionable() {
  list_modules | awk '$1=="NONE" && $3=="shortcut=no"{print}'
}

list_script_menus() {
  if [ ! -d "$SCRIPTS" ]; then
    echo "(no /opt/trading/scripts)"
    return 0
  fi
  find "$SCRIPTS" -maxdepth 3 -type f \( -name "*_menu.sh" -o -name "*_menu*.sh" \) 2>/dev/null \
    | sed "s#^$ROOT/##" | sort
}

build_menu_list() {
  shopt -s nullglob
  local arr=($BIN/menu-*)
  shopt -u nullglob
  printf "%s\n" "${arr[@]}" | sed 's#.*/##' | sort -u
}

list_menus_numbered() {
  local i=1
  local name
  echo "--- MENUS (shortcuts menu-*) ---"
  while IFS= read -r name; do
    [ -z "$name" ] && continue
    printf "%2d) %s\n" "$i" "$name"
    i=$((i+1))
  done < <(build_menu_list)
  echo "count=$((i-1))"
}

menu_name_from_index() {
  local idx="$1"
  local i=1
  local name
  while IFS= read -r name; do
    [ -z "$name" ] && continue
    if [ "$i" -eq "$idx" ]; then
      echo "$name"
      return 0
    fi
    i=$((i+1))
  done < <(build_menu_list)
  return 1
}

run_menu_by_name() {
  local name="$1"
  if [[ "$name" == menu-* ]]; then
    if [ -x "$BIN/$name" ] || [ -L "$BIN/$name" ]; then
      exec "$BIN/$name"
    fi
    echo "ERROR: shortcut not found: $BIN/$name"
    return 2
  fi

  local out typ entry
  out="$(discover_module_entry "$name")"
  typ="${out%%|*}"
  entry="${out#*|}"
  if [ "$typ" = "standard" ] || [ "$typ" = "legacy" ]; then
    exec bash "$entry"
  fi
  echo "ERROR: module has no menu entry: $name"
  return 2
}

cleanup_broken_symlinks() {
  local g="$1"
  shopt -s nullglob
  local arr=($BIN/$g)
  shopt -u nullglob
  local removed=0
  for p in "${arr[@]}"; do
    [ -L "$p" ] || continue
    local target; target="$(readlink -f "$p" 2>/dev/null || true)"
    if [ -z "$target" ] || [ ! -e "$target" ]; then
      rm -f "$p"
      echo "RM: $(basename "$p")"
      removed=$((removed+1))
    fi
  done
  echo "removed=$removed"
}

cmd="${1:-menu}"

case "$cmd" in
  menu)
    while true; do
      echo
      echo "=== OPS SUPER MENU ==="
      echo "host=$host role=$role ts=$ts"
      echo "1) Menus (numérotés)  -> exécuter par numéro"
      echo "2) Shortcuts (menu/cmd/sanity) + BROKEN"
      echo "3) Modules (/opt/trading/modules) status (STD/LEG/NONE)"
      echo "4) Modules SANS menu (NONE) (tous)"
      echo "5) Modules SANS menu (NONE) + SANS shortcut (actionable)"
      echo "6) Script-menus (/opt/trading/scripts)"
      echo "7) Cleanup BROKEN symlinks (rm)  [DANGEREUX]"
      echo "q) Quit"
      read -r -p "> " ans
      case "$ans" in
        1)
          list_menus_numbered
          read -r -p "Numéro du menu à ouvrir (ENTER=retour): " n
          [ -z "${n:-}" ] && continue
          if ! [[ "$n" =~ ^[0-9]+$ ]]; then
            echo "ERROR: numéro invalide"
            continue
          fi
          mn="$(menu_name_from_index "$n" || true)"
          if [ -z "${mn:-}" ]; then
            echo "ERROR: numéro hors liste"
            continue
          fi
          run_menu_by_name "$mn"
          ;;
        2)
          echo "--- menu-* ---"; list_shortcuts "menu-*"; echo
          echo "--- cmd-* ---"; list_shortcuts "cmd-*"; echo
          echo "--- sanity-* ---"; list_shortcuts "sanity-*";;
        3) list_modules;;
        4) list_modules_none;;
        5) list_modules_none_actionable;;
        6) list_script_menus;;
        7)
          echo "Cleaning BROKEN symlinks under $BIN ..."
          cleanup_broken_symlinks "menu-*"
          cleanup_broken_symlinks "cmd-*"
          cleanup_broken_symlinks "sanity-*"
          ;;
        q|Q) exit 0;;
        *) echo "?";;
      esac
    done
    ;;
  list_menus) list_menus_numbered;;
  list_shortcuts)
    echo "--- menu-* ---"; list_shortcuts "menu-*"; echo
    echo "--- cmd-* ---"; list_shortcuts "cmd-*"; echo
    echo "--- sanity-* ---"; list_shortcuts "sanity-*";;
  list_modules) list_modules;;
  list_none) list_modules_none;;
  list_none_actionable) list_modules_none_actionable;;
  list_scripts) list_script_menus;;
  run) run_menu_by_name "${2:-}";;
  broken)
    list_shortcuts "menu-*" | grep '^BROKEN' || true
    list_shortcuts "cmd-*" | grep '^BROKEN' || true
    list_shortcuts "sanity-*" | grep '^BROKEN' || true
    ;;
  cleanup_broken)
    cleanup_broken_symlinks "menu-*"
    cleanup_broken_symlinks "cmd-*"
    cleanup_broken_symlinks "sanity-*"
    ;;
  *)
    echo "Usage:"
    echo "  ops_super_menu.sh menu"
    echo "  ops_super_menu.sh list_menus"
    echo "  ops_super_menu.sh list_shortcuts"
    echo "  ops_super_menu.sh list_modules"
    echo "  ops_super_menu.sh list_none"
    echo "  ops_super_menu.sh list_none_actionable"
    echo "  ops_super_menu.sh list_scripts"
    echo "  ops_super_menu.sh run <menu-xxx|module>"
    echo "  ops_super_menu.sh broken"
    echo "  ops_super_menu.sh cleanup_broken"
    exit 1
    ;;
esac
