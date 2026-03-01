#!/usr/bin/env bash
set -euo pipefail
test -d /opt/trading || { echo "FAIL: /opt/trading missing"; exit 1; }
echo "PASS"
