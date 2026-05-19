#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/opt/trading}"
MODS="$ROOT/modules"
BIN="/usr/local/bin"

host="$(hostname)"
ts="$(date +%Y%m%d_%H%M%S)"

say() { printf "%s\n" "$*"; }

# Marker we embed inside wrapper menu.sh
WRAP_MARKER="=== MODULE MENU (wrapper) ==="

is_wrapper_module() {
  local m="$1"
  [ -f "$MODS/$m/scripts/menu.sh" ] || return 1
  grep -qF "$WRAP_MARKER" "$MODS/$m/scripts/menu.sh" 2>/dev/null
}

has_menu_shortcut() {
  local m="$1"
  [ -e "$BIN/menu-$m" ]
}

# Modules that need wrapper generation:
# - in /modules
# - not __pycache__
# - no scripts/menu.sh (standard menu) AND no /usr/local/bin/menu-<m>
is_needs_wrapper() {
  local m="$1"
  [[ "$m" == "__pycache__" ]] && return 1
  [ -d "$MODS/$m" ] || return 1
  [ -f "$MODS/$m/scripts/menu.sh" ] && return 1
  has_menu_shortcut "$m" && return 1
  return 0
}

list_needs_wrapper() {
  [ -d "$MODS" ] || { say "ERROR: missing $MODS"; return 2; }
  local d m
  for d in "$MODS"/*; do
    [ -d "$d" ] || continue
    m="$(basename "$d")"
    if is_needs_wrapper "$m"; then
      echo "$m"
    fi
  done | sort
}

# Wrapper modules missing shortcuts
list_wrappers_missing_shortcuts() {
  [ -d "$MODS" ] || return 2
  local d m
  for d in "$MODS"/*; do
    [ -d "$d" ] || continue
    m="$(basename "$d")"
    if is_wrapper_module "$m" && ! has_menu_shortcut "$m"; then
      echo "$m"
    fi
  done | sort
}

list_wrappers_all() {
  [ -d "$MODS" ] || return 2
  local d m
  for d in "$MODS"/*; do
    [ -d "$d" ] || continue
    m="$(basename "$d")"
    if is_wrapper_module "$m"; then
      echo "$m"
    fi
  done | sort
}

write_wrapper_files() {
  local m="$1"
  local dir="$MODS/$m"
  local sdir="$dir/scripts"
  mkdir -p "$sdir"

  local menu="$sdir/menu.sh"
  local cmd="$sdir/cmd.sh"
  local sanity="$sdir/sanity_check.sh"
  local install="$sdir/install_shortcuts.sh"

  if [ ! -f "$menu" ]; then
    cat >"$menu" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
MOD="${0%/*}/.."
MOD="$(cd "$MOD" && pwd -P)"
NAME="$(basename "$MOD")"

# WRAPPER MARKER (used by ops_wrappers)
echo
echo "=== MODULE MENU (wrapper) ==="
echo "name=$NAME"
echo "path=$MOD"
echo

readme=""
for f in "$MOD/README.md" "$MOD/README.txt" "$MOD/README"; do
  [ -f "$f" ] && readme="$f" && break
done

while true; do
  echo "1) Show README"
  echo "2) List files (maxdepth=2)"
  echo "3) Grep entrypoints (python __main__/click/typer/argparse)"
  echo "4) Git status (module only)"
  echo "5) Open a shell in module dir"
  echo "q) Quit"
  read -r -p "> " ans
  case "$ans" in
    1)
      if [ -n "$readme" ]; then
        sed -n '1,220p' "$readme" || true
      else
        echo "(no README found)"
      fi
      ;;
    2)
      (cd "$MOD" && find . -maxdepth 2 -type f | sed 's#^\./##' | sort) | sed -n '1,200p'
      ;;
    3)
      (cd "$MOD" && \
        grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ -E "if __name__ == '__main__'|typer|click|argparse" . \
        | head -n 120) || true
      ;;
    4)
      ROOT="/opt/trading"
      if [ -d "$ROOT/.git" ]; then
        (cd "$ROOT" && git status -sb -- "$MOD" 2>/dev/null) || true
      else
        echo "(no git repo at $ROOT)"
      fi
      ;;
    5)
      echo "Entering: $MOD"
      cd "$MOD"
      exec bash
      ;;
    q|Q) exit 0;;
    *) echo "?";;
  esac
done
SH
    chmod +x "$menu"
  fi

  if [ ! -f "$cmd" ]; then
    cat >"$cmd" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
MOD="${0%/*}/.."
MOD="$(cd "$MOD" && pwd -P)"
NAME="$(basename "$MOD")"

cmd="${1:-help}"
case "$cmd" in
  info) echo "name=$NAME"; echo "path=$MOD";;
  readme)
    for f in "$MOD/README.md" "$MOD/README.txt" "$MOD/README"; do
      [ -f "$f" ] && sed -n '1,220p' "$f" && exit 0
    done
    echo "(no README found)"
    ;;
  ls)
    (cd "$MOD" && find . -maxdepth 2 -type f | sed 's#^\./##' | sort) | sed -n '1,200p'
    ;;
  grep)
    (cd "$MOD" && \
      grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ -E "if __name__ == '__main__'|typer|click|argparse" . \
      | head -n 120) || true
    ;;
  menu) exec bash "$MOD/scripts/menu.sh";;
  *)
    echo "Usage: cmd-$NAME info|readme|ls|grep|menu"
    exit 1
    ;;
esac
SH
    chmod +x "$cmd"
  fi

  if [ ! -f "$sanity" ]; then
    cat >"$sanity" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
MOD="${0%/*}/.."
MOD="$(cd "$MOD" && pwd -P)"
NAME="$(basename "$MOD")"
echo "=== sanity (wrapper) ==="
echo "name=$NAME"
echo "path=$MOD"
[ -d "$MOD" ] || { echo "FAIL: module missing"; exit 2; }
[ -d "$MOD/scripts" ] || { echo "FAIL: scripts missing"; exit 2; }
[ -x "$MOD/scripts/menu.sh" ] || { echo "FAIL: menu.sh not executable"; exit 2; }
[ -x "$MOD/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh not executable"; exit 2; }
echo "PASS: wrapper sanity OK"
SH
    chmod +x "$sanity"
  fi

  if [ ! -f "$install" ]; then
    cat >"$install" <<SH
#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/trading"
BIN="/usr/local/bin"
sudo ln -sf "\$ROOT/modules/$m/scripts/menu.sh" "\$BIN/menu-$m"
sudo ln -sf "\$ROOT/modules/$m/scripts/cmd.sh" "\$BIN/cmd-$m"
sudo ln -sf "\$ROOT/modules/$m/scripts/sanity_check.sh" "\$BIN/sanity-$m"
echo "OK: installed shortcuts for $m"
ls -l "\$BIN/menu-$m" "\$BIN/cmd-$m" "\$BIN/sanity-$m"
SH
    chmod +x "$install"
  fi
}

generate_wrappers() {
  local created=0
  local m
  while IFS= read -r m; do
    [ -z "$m" ] && continue
    write_wrapper_files "$m"
    created=$((created+1))
  done < <(list_needs_wrapper)
  say "OK: wrappers ensured for modules needing wrappers (count=$created)"
}

install_shortcuts_for_wrappers() {
  local m count=0
  while IFS= read -r m; do
    [ -z "$m" ] && continue
    sudo ln -sf "$ROOT/modules/$m/scripts/menu.sh" "$BIN/menu-$m"
    sudo ln -sf "$ROOT/modules/$m/scripts/cmd.sh" "$BIN/cmd-$m"
    sudo ln -sf "$ROOT/modules/$m/scripts/sanity_check.sh" "$BIN/sanity-$m"
    count=$((count+1))
  done < <(list_wrappers_missing_shortcuts)
  say "OK: shortcuts installed for wrapper modules missing shortcuts (count=$count)"
}

cmd="${1:-menu}"
case "$cmd" in
  scan)
    echo "host=$host ts=$ts"
    echo "--- modules needing wrappers (no scripts/menu.sh and no menu-<m>) ---"
    list_needs_wrapper | nl -w2 -s') '
    echo
    echo "--- wrappers missing shortcuts (have wrapper menu.sh but no menu-<m>) ---"
    list_wrappers_missing_shortcuts | nl -w2 -s') '
    ;;
  generate) generate_wrappers;;
  install_shortcuts) install_shortcuts_for_wrappers;;
  generate_and_install) generate_wrappers; install_shortcuts_for_wrappers;;
  run_by_number)
    n="${2:-}"
    [ -n "$n" ] || { echo "ERROR: need a number (1..N)"; exit 2; }
    [ "$n" -ge 1 ] 2>/dev/null || { echo "ERROR: invalid number (use 1..N)"; exit 2; }
    m="$(list_wrappers_all | sed -n "${n}p" || true)"
    [ -n "$m" ] || { echo "ERROR: invalid number"; exit 2; }
    exec bash "$ROOT/modules/$m/scripts/menu.sh"
    ;;
  menu)
    while true; do
      echo
      echo "=== OPS WRAPPERS ==="
      echo "host=$host ts=$ts"
      echo "1) Scan (needs wrappers + wrappers missing shortcuts)"
      echo "2) Generate wrappers (no sudo)"
      echo "3) Install shortcuts for wrappers missing shortcuts (sudo)"
      echo "4) Generate + install (sudo)"
      echo "5) Run wrapper menu by number (from ALL wrappers)"
      echo "q) Quit"
      read -r -p "> " ans
      case "$ans" in
        1) "$0" scan;;
        2) "$0" generate;;
        3) "$0" install_shortcuts;;
        4) "$0" generate_and_install;;
        5)
          echo "--- wrappers (ALL) ---"
          list_wrappers_all | nl -w2 -s') '
          read -r -p "Numéro (1..N): " n
          [ -n "$n" ] || continue
          "$0" run_by_number "$n"
          ;;
        q|Q) exit 0;;
        *) echo "?";;
      esac
    done
    ;;
  *)
    echo "Usage: ops_wrappers.sh scan|generate|install_shortcuts|generate_and_install|run_by_number N|menu"
    exit 1
    ;;
esac
