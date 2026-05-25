#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$ROOT"

echo "=== data_center sanity check ==="

python3 -c "
from modules.data_center.layout import load_producers_registry, load_consumers_registry
import json, sys

p = load_producers_registry()
c = load_consumers_registry()

assert p['registry_version'] == 'v1', 'producers registry_version mismatch'
assert c['registry_version'] == 'v1', 'consumers registry_version mismatch'

print(f'producers : {len(p[\"producers\"])} declared')
print(f'consumers : {len(c[\"consumers\"])} declared')

implemented = [x for x in c['consumers'] if x['implementation_status'] == 'implemented']
print(f'consumers implemented : {len(implemented)}')

assert len(implemented) >= 2, f'CLOSE_GATE_MASTER_TARGET requires >=2 implemented consumers, got {len(implemented)}'

from modules.data_center.runtime_registry import load_runtime_registry
rt = load_runtime_registry()
written = [pid for pid, info in rt.get('producers', {}).items() if info.get('last_write')]
print(f'producers with last_write : {len(written)} / {len(p[\"producers\"])}')
for pid in written:
    print(f'  {pid} : {rt[\"producers\"][pid][\"last_write\"]}')

print('PASS')
"
