#!/bin/bash
set -euo pipefail
cd /opt/trading
python3 scripts/ai/workers/health_status.py 2>&1 || echo "HEALTH_STATUS_FAIL"
