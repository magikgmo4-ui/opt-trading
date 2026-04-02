#!/usr/bin/env bash
set -euo pipefail
command -v openclaw >/dev/null 2>&1 || { echo "FAIL: openclaw non trouvé" >&2; exit 1; }
openclaw config file >/dev/null 2>&1 || { echo "FAIL: config file introuvable" >&2; exit 1; }
echo "PASS: configure_openclaw sanity OK"
