#!/usr/bin/env bash
# Run the semi-auto pilot (dry_run only, non-destructive).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROMPT_PATH="${1:-}"

if [[ -z "$PROMPT_PATH" ]]; then
  echo "usage: $0 <go_prompt_path>" >&2
  exit 1
fi

if [[ ! -f "$PROMPT_PATH" ]]; then
  echo "error: prompt file not found: $PROMPT_PATH" >&2
  exit 1
fi

cd "$REPO_ROOT"

if [[ ! -d venv ]]; then
  echo "error: venv not found — run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt" >&2
  exit 1
fi

source venv/bin/activate
python3 -m modules.automation_ops.semiauto_pilot.pilot_runner "$PROMPT_PATH"
