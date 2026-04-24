#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
cmd-perm_fix_student

Usage:
  cmd-perm_fix_student fix_runtime     # fix perms for state/tmp/_student_archive runtime paths
  cmd-perm_fix_student fix_journal     # legacy alias of fix_runtime
  cmd-perm_fix_student fix_all         # (optional) fix perms for entire /opt/trading (more intrusive)
  cmd-perm_fix_student ollama_test     # test ollama CLI + local API (127.0.0.1:11434)
  cmd-perm_fix_student status          # quick status/diagnostic
  cmd-perm_fix_student help
USAGE
}

need_sudo() {
  if [[ "${EUID}" -ne 0 ]]; then
    echo "ERROR: run with sudo for this action."
    exit 1
  fi
}

owner_user() {
  if [[ -n "${SUDO_USER:-}" ]]; then
    echo "${SUDO_USER}"
  else
    id -un
  fi
}

fix_paths() {
  local user group
  user="$(owner_user)"
  group="$(id -gn "$user" 2>/dev/null || echo "$user")"

  local -a paths=(
    "/opt/trading/state"
    "/opt/trading/_student_archive"
    "/opt/trading/tmp"
    "/opt/trading/tmp/logs"
  )

  echo "== fixing permissions for runtime-related paths"
  echo "User:Group => ${user}:${group}"
  for p in "${paths[@]}"; do
    if [[ -e "$p" ]]; then
      echo " - $p"
      chown -R "${user}:${group}" "$p"
      chmod -R u+rwX,g+rwX,o-rwx "$p"
      if [[ -d "$p" ]]; then
        find "$p" -type d -exec chmod g+s {} + || true
      fi
    else
      echo " - (skip missing) $p"
    fi
  done

  echo "OK: runtime permissions fixed."
}

fix_all_opt() {
  local user group
  user="$(owner_user)"
  group="$(id -gn "$user" 2>/dev/null || echo "$user")"

  echo "== fixing permissions for /opt/trading (OPTIONAL / more intrusive)"
  echo "User:Group => ${user}:${group}"
  chown -R "${user}:${group}" /opt/trading
  chmod -R u+rwX,g+rwX,o-rwx /opt/trading
  find /opt/trading -type d -exec chmod g+s {} + || true
  echo "OK: /opt/trading permissions fixed."
}

ollama_test() {
  echo "== ollama test"
  if ! command -v ollama >/dev/null 2>&1; then
    echo "ERROR: 'ollama' not found. Install/start Ollama first."
    exit 1
  fi

  echo "-- version"
  ollama --version || true

  echo "-- list"
  ollama list || true

  echo "-- API tags (http://127.0.0.1:11434/api/tags)"
  if command -v curl >/dev/null 2>&1; then
    if curl -sf --max-time 2 "http://127.0.0.1:11434/api/tags" >/tmp/ollama_tags.json; then
      head -c 800 /tmp/ollama_tags.json; echo
    else
      echo "WARN: cannot reach Ollama API on 127.0.0.1:11434 (is 'ollama serve' running?)"
      exit 2
    fi
  else
    echo "ERROR: curl not found."
    exit 1
  fi

  local model
  model="$(ollama list 2>/dev/null | awk 'NR==2{print $1}' || true)"
  if [[ -z "${model}" || "${model}" == "NAME" ]]; then
    echo "INFO: No models found. Pull one, e.g.: ollama pull llama3.2:1b"
    exit 0
  fi

  echo "-- API generate test (model=${model})"
  curl -sf --max-time 10 "http://127.0.0.1:11434/api/generate" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"${model}\",\"prompt\":\"ping\",\"stream\":false}" \
    | head -c 1200; echo

  echo "OK: Ollama API responds."
}

status() {
  echo "== status"
  echo "-- whoami / id"
  whoami
  id
  echo "-- runtime unreadable files (if any)"
  local found=0
  for p in /opt/trading/state /opt/trading/tmp /opt/trading/_student_archive; do
    if [[ -d "$p" ]]; then
      found=1
      find "$p" -type f ! -readable -printf '%m %u:%g %p\n' | head -n 200 || true
    fi
  done
  if [[ "$found" -eq 0 ]]; then
    echo "(runtime dirs missing)"
  fi
}

main() {
  local cmd="${1:-help}"
  case "$cmd" in
    fix_runtime|fix_journal|"")
      need_sudo
      fix_paths
      ;;
    fix_all)
      need_sudo
      fix_all_opt
      ;;
    ollama_test|ollama)
      ollama_test
      ;;
    status)
      status
      ;;
    help|-h|--help)
      usage
      ;;
    *)
      echo "Unknown command: $cmd"
      usage
      exit 1
      ;;
  esac
}

main "$@"
