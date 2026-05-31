# bot_vision orchestrator runner — called by systemd timer
# Installed at: /opt/trading/modules/bot_vision/headless_capture/scripts/run_orchestrator.sh

REPO_DIR="/opt/trading"
VENV_PYTHON="${REPO_DIR}/venv/bin/python3"
SCRIPT="${REPO_DIR}/modules/bot_vision/headless_capture/scripts/schedule_orchestrator.py"

# Fallback to system python if venv not available
PYTHON="${VENV_PYTHON}"
if [ ! -x "${PYTHON}" ]; then
    PYTHON="python3"
fi

cd "${REPO_DIR}" || exit 1

export BOT_VISION_MARKET_HOURS="${BOT_VISION_MARKET_HOURS:-1}"
export BOT_VISION_TMP="${BOT_VISION_TMP:-/tmp/bot_vision_headless}"
export BOT_VISION_OUT="${BOT_VISION_OUT:-/srv/sftp/shared_files/shared/vision_inbox}"

exec "${PYTHON}" "${SCRIPT}" "$@"
