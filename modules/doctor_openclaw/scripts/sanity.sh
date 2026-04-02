#!/usr/bin/env bash
set -euo pipefail
command -v openclaw >/dev/null 2>&1 || { echo "FAIL: openclaw non trouve" >&2; exit 1; }
echo "PASS: doctor_openclaw sanity OK"
