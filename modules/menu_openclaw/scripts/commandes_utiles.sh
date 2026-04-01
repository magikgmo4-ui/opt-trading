#!/usr/bin/env bash
set -euo pipefail

run_direct() {
  case "${1:-list}" in
    list)
      cat <<'EOF'
Actions disponibles:
  list
  validate
  health
  probe
  audit
  agents
  doctor
  logs
  status
EOF
      ;;
    validate)
      openclaw config validate
      ;;
    health)
      openclaw gateway health
      ;;
    probe)
      openclaw gateway probe
      ;;
    audit)
      openclaw security audit --deep
      ;;
    agents)
      openclaw agents list
      ;;
    doctor)
      openclaw doctor
      ;;
    logs)
      tail -n 80 "/tmp/openclaw/openclaw-$(date +%F).log" 2>/dev/null || ls -lah /tmp/openclaw
      ;;
    status)
      echo "USER=$(whoami)"
      echo "HOME=$HOME"
      echo "PATH=$PATH"
      echo "CONFIG=$HOME/.openclaw/openclaw.json"
      echo
      command -v openclaw || true
      echo
      ls -lah "$HOME/.openclaw" || true
      echo
      ls -lah "$HOME/.openclaw/config.d" || true
      ;;
    *)
      echo "Action inconnue: $1" >&2
      exit 1
      ;;
  esac
}

ACTION="${1:-list}"

if [ "$ACTION" = "list" ]; then
  run_direct list
  exit 0
fi

if [ "$(whoami)" = "openclaw" ]; then
  run_direct "$ACTION"
  exit 0
fi

if ! command -v sudo >/dev/null 2>&1; then
  echo "FAIL: sudo indisponible pour basculer vers openclaw" >&2
  exit 1
fi

echo "[run-as-openclaw] action=$ACTION"
HOST_OPENCLAW_BIN="$(command -v openclaw || true)"

sudo -iu openclaw env ACTION="$ACTION" HOST_OPENCLAW_BIN="$HOST_OPENCLAW_BIN" bash <<'EOS'
set -euo pipefail

[ -f "$HOME/.profile" ] && . "$HOME/.profile" || true
[ -f "$HOME/.bashrc" ] && . "$HOME/.bashrc" || true
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

if command -v openclaw >/dev/null 2>&1; then
  :
elif [ -n "${HOST_OPENCLAW_BIN:-}" ] && [ -x "${HOST_OPENCLAW_BIN:-}" ]; then
  export PATH="$(dirname "$HOST_OPENCLAW_BIN"):$PATH"
else
  echo "FAIL: openclaw introuvable dans le contexte openclaw" >&2
  exit 127
fi

case "${ACTION:-}" in
  validate)
    openclaw config validate
    ;;
  health)
    openclaw gateway health
    ;;
  probe)
    openclaw gateway probe
    ;;
  audit)
    openclaw security audit --deep
    ;;
  agents)
    openclaw agents list
    ;;
  doctor)
    openclaw doctor
    ;;
  logs)
    tail -n 80 "/tmp/openclaw/openclaw-$(date +%F).log" 2>/dev/null || ls -lah /tmp/openclaw
    ;;
  status)
    echo "USER=$(whoami)"
    echo "HOME=$HOME"
    echo "PATH=$PATH"
    echo "CONFIG=$HOME/.openclaw/openclaw.json"
    echo
    command -v openclaw || true
    echo
    ls -lah "$HOME/.openclaw" || true
    echo
    ls -lah "$HOME/.openclaw/config.d" || true
    ;;
  *)
    echo "FAIL: action inconnue: ${ACTION:-}" >&2
    exit 1
    ;;
esac
EOS
