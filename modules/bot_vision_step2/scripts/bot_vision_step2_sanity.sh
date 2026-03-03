#!/usr/bin/env bash
set -euo pipefail
echo "=== bot_vision_step2 sanity ==="
date -Is || true

PY="/opt/trading/.venvs/bot_vision_step2/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "WARN: venv not found ($PY). This is OK before install_service."
  PY="/usr/bin/python3"
fi
$PY /opt/trading/modules/bot_vision_step2/app/bot_vision_step2.py sanity
