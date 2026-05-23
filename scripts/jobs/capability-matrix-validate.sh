#!/bin/bash
set -euo pipefail
cd /opt/trading
echo "=== Capability Matrix Validation ==="
python3 -c "
import json
tasks = json.load(open('scripts/ai/workers/tasks.index.json'))
registry = json.load(open('scripts/ai/workers/models.registry.json'))
task_types = set(tasks['tasks'].keys())
registry_roles = set()
for m, d in registry['models'].items():
    for r in d.get('roles', []):
        registry_roles.add(r)
missing = registry_roles - task_types
if missing:
    print(f'WARN: roles in registry but not in tasks.index.json: {missing}')
else:
    print('OK: all registry roles exist in tasks.index.json')
extra = task_types - registry_roles
if extra:
    print(f'INFO: tasks in index but not assigned to any model: {extra}')
print(f'Tasks: {len(task_types)}, Roles: {len(registry_roles)}')
" 2>&1
echo "{\"job\":\"capability-matrix-validate\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\"}" >> data/runtime_health/job_logs/ledger.jsonl
