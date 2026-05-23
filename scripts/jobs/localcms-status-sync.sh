#!/bin/bash
set -euo pipefail
cd /opt/trading
python3 scripts/ai/workers/localcms_automation_status_sync.py 2>&1 || echo "LOCALCMS_SYNC_FAIL"
