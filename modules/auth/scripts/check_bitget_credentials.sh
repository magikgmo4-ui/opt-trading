#!/bin/bash
set -euo pipefail

PROFILE="${1:-readonly_main}"

echo "=== Bitget Credentials Check ==="
echo "Profile: $PROFILE"
echo

/opt/trading/venv/bin/python3 -c "
import sys
sys.path.insert(0, '/opt/trading')
from modules.auth.bitget_credentials import load_credentials, list_profiles_status

status, creds = load_credentials('$PROFILE')
print(f'Status: {status}')
if status == 'ok':
    print(f'  api_key: {creds[\"api_key\"][:8]}...')
    print(f'  secret_key: {creds[\"secret_key\"][:8]}...')
    print(f'  passphrase: ***')
elif status == 'incomplete':
    print('  Some fields are missing in env vars')
else:
    print('  No credentials found for this profile')

print()
print('All profiles:')
for p, s in list_profiles_status().items():
    print(f'  {p}: {s}')
"
