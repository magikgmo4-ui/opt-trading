#!/bin/bash
set -euo pipefail
cd /opt/trading
echo "=== Bridge Contract Validation ==="
python3 -c "
import json
contract = json.load(open('scripts/ai/workers/orchestration/external_apps_orchestration_contract.json'))
apps = contract['input']['requested_app']['enum']
modes = contract['input']['mode']['enum']
print(f'Contract v{contract.get(\"contract_version\",\"unknown\")}')
print(f'Target apps ({len(apps)}): {apps}')
print(f'Modes: {modes}')
print('OK: contract parseable and valid')
" 2>&1
echo "{\"job\":\"bridge-contract-validation\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\"}" >> data/runtime_health/job_logs/ledger.jsonl
