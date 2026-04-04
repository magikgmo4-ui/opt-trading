#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$BASE/../.." && pwd)"
DEFAULT_VENV=".venv-dev-validation"
CMD="${1:-help}"
ARG2="${2:-}"

ensure_repo() {
  git -C "$REPO_ROOT" rev-parse --show-toplevel >/dev/null 2>&1
}

venv_dir() {
  local name="${1:-$DEFAULT_VENV}"
  printf '%s/%s' "$REPO_ROOT" "$name"
}

venv_python() {
  local name="${1:-$DEFAULT_VENV}"
  printf '%s/bin/python' "$(venv_dir "$name")"
}

cmd_status() {
  echo "REPO_ROOT=$REPO_ROOT"
  echo "BRANCH=$(git -C "$REPO_ROOT" branch --show-current)"
  echo "PYTHON3=$(command -v python3 || true)"
  python3 --version || true
  echo
  git -C "$REPO_ROOT" status --short --branch
  echo
  echo "VENV_CANDIDATES:"
  find "$REPO_ROOT" -maxdepth 1 -type d -name '.venv*' -printf '  %f\n' | sort || true
}

cmd_pre_pr() {
  echo "== STATUS =="
  git -C "$REPO_ROOT" status --short --branch
  echo
  echo "== LAST 5 COMMITS =="
  git -C "$REPO_ROOT" log --oneline -5
  echo
  if git -C "$REPO_ROOT" rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1; then
    echo "== AHEAD/BEHIND =="
    git -C "$REPO_ROOT" rev-list --left-right --count HEAD...@{u}
  else
    echo "No upstream configured for current branch."
  fi
}

cmd_ensure_venv() {
  local name="${ARG2:-$DEFAULT_VENV}"
  local dir
  dir="$(venv_dir "$name")"
  if [ -d "$dir" ]; then
    echo "Venv already exists: $dir"
  else
    python3 -m venv "$dir"
    echo "Venv created: $dir"
  fi
  echo "Activate with: source $dir/bin/activate"
}

cmd_install_http_test_deps() {
  local name="${ARG2:-$DEFAULT_VENV}"
  local py
  py="$(venv_python "$name")"
  if [ ! -x "$py" ]; then
    echo "Missing venv python: $py"
    echo "Run: bash modules/dev_validation_hub/scripts/cmd.sh ensure-venv ${name}"
    exit 1
  fi
  "$py" -m pip install --upgrade pip
  "$py" -m pip install pytest fastapi httpx uvicorn
}

cmd_run_memory_bricks_http_tests() {
  local name="${ARG2:-$DEFAULT_VENV}"
  local py
  py="$(venv_python "$name")"
  if [ ! -x "$py" ]; then
    echo "Missing venv python: $py"
    echo "Run: bash modules/dev_validation_hub/scripts/cmd.sh ensure-venv ${name}"
    exit 1
  fi
  "$py" -m pytest "$REPO_ROOT/modules/memory_bricks/tests/test_api_v2_http.py"
}

cmd_trading_lab_status() {
  bash "$REPO_ROOT/modules/trading_lab_v1/scripts/cmd.sh" status
}

cmd_help() {
  cat <<'EOF'
Usage: bash modules/dev_validation_hub/scripts/cmd.sh <command> [arg]

Commands:
  sanity                         Run module sanity
  status                         Show repo / branch / python / venv candidates
  pre-pr                         Show short pre-PR Git state
  ensure-venv [name]             Create local venv (default: .venv-dev-validation)
  install-http-test-deps [name]  Install pytest/fastapi/httpx/uvicorn in venv
  run-memory-bricks-http-tests   Run isolated memory_bricks HTTP tests in venv
  trading-lab-status             Show trading_lab_v1 status
EOF
}

ensure_repo || { echo "Not inside opt-trading repo"; exit 1; }

case "$CMD" in
  sanity) bash "$BASE/scripts/sanity.sh" ;;
  status) cmd_status ;;
  pre-pr) cmd_pre_pr ;;
  ensure-venv) cmd_ensure_venv ;;
  install-http-test-deps) cmd_install_http_test_deps ;;
  run-memory-bricks-http-tests) cmd_run_memory_bricks_http_tests ;;
  trading-lab-status) cmd_trading_lab_status ;;
  help|*) cmd_help ;;
esac
