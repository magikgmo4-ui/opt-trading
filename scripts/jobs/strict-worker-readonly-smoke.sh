#!/bin/bash
set -euo pipefail
cd /opt/trading
python3 scripts/ai/tests/g05_strict_worker_e2e_readonly.py 2>&1 || echo "STRICT_WORKER_SMOKE_FAIL"
