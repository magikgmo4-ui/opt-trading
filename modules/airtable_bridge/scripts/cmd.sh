#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<EOF
Usage: $(basename "$0") <table> <json_file>

Send records to an Airtable table via the bridge client.

Args:
  table       Airtable table name (Trades, Signals, Backtests, GO_Status)
  json_file   Path to JSON file with records array

Env:
  AIRTABLE_API_KEY   Required
  AIRTABLE_BASE_ID   Required

Example:
  export AIRTABLE_API_KEY=xxx AIRTABLE_BASE_ID=yyy
  $(basename "$0") Trades ./trade.json
EOF
    exit 1
}

TABLE="${1:-}"
JSON_FILE="${2:-}"

if [ -z "$TABLE" ] || [ -z "$JSON_FILE" ]; then
    usage
fi

if [ ! -f "$JSON_FILE" ]; then
    echo "Error: file not found: $JSON_FILE"
    exit 1
fi

PYTHON_PATH="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$PYTHON_PATH/app${PYTHONPATH:+:$PYTHONPATH}"

python3 -c "
import json
import sys
sys.path.insert(0, '$PYTHON_PATH/app')
from client import send_records

with open('$JSON_FILE') as f:
    data = json.load(f)

if isinstance(data, dict):
    records = data.get('records', [data])
elif isinstance(data, list):
    records = data
else:
    print('Error: invalid JSON format')
    sys.exit(1)

result = send_records('$TABLE', records)
print(json.dumps(result, indent=2))
"
