#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE="$BASE/state_cache.json"
SCHEMA="$BASE/state_schema.json"
PROJECT_ROOT="$(cd "$BASE/../../.." && pwd)"
mkdir -p "$BASE"

if [ ! -f "$SCHEMA" ]; then
  echo '{"error":"state_schema.json not found","updated_at":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"}' > "$CACHE"
  exit 1
fi

aggregate_state() {
  python3 -c "
import json, subprocess, sys, urllib.request
from pathlib import Path

schema = json.loads(Path('$SCHEMA').read_text())
results = []
for mod in schema.get('modules', []):
  mod_id = mod['id']
  mtype = mod.get('type', '')
  status = 'unknown'
  detail = ''
  if mtype == 'http':
    try:
      r = urllib.request.urlopen(mod['endpoint'], timeout=5)
      if r.status == 200:
        status = 'up'
      else:
        status = 'degraded'
      detail = f'HTTP {r.status}'
    except Exception as e:
      status = 'down'
      detail = str(e)
  elif mtype == 'ws':
    status = 'unknown'
    detail = 'ws check not implemented'
  elif mtype == 'process':
    try:
      r = subprocess.run(mod['check'], shell=True, capture_output=True, timeout=5)
      if r.returncode == 0:
        status = 'up'
      else:
        status = 'down'
      detail = 'process check'
    except Exception as e:
      status = 'down'
      detail = str(e)
  results.append({
    'id': mod_id,
    'status': status,
    'detail': detail,
    'machine': mod.get('machine', ''),
    'critical': mod.get('critical', False),
    'last_check': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
  })
out = {'version':'1.0','updated_at':'$(date -u +%Y-%m-%dT%H:%M:%SZ)','modules':results}
Path('$CACHE').write_text(json.dumps(out, indent=2))
print('OK')
" 2>&1
}

aggregate_state
