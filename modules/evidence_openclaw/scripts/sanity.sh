#!/usr/bin/env bash
set -euo pipefail
[ "$(whoami)" = "openclaw" ] || { echo "FAIL: exécuter ce module sous l'utilisateur openclaw" >&2; exit 1; }
command -v openclaw >/dev/null 2>&1 || { echo "FAIL: openclaw non trouvé" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "FAIL: python3 non trouvé" >&2; exit 1; }
echo "PASS: evidence_openclaw sanity OK"
