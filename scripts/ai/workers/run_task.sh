#!/usr/bin/env bash
# === run_task.sh — Strict Workers Runtime Lock ===
# GO: GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01
# Phase A: Verrouiller le runner
#
# Usage: ./run_task.sh <job_packet.json>
# Output: reports/ai/workers/<job_packet_id>.md (DRAFT_ONLY via worker model)
#
# Garde-fous:
#   - timeout 120s par job
#   - sorties <= 500 lignes
#   - aucun write runtime
#   - git status clean avant execution
#   - seuls les modeles VERIFIED du registry sont autorises
set -euo pipefail

TIMEOUT_SEC=120
MAX_OUTPUT_LINES=500
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$REPO_ROOT" ]; then
    echo "ERROR: not inside a git repository" >&2
    exit 1
fi

SCRIPT_DIR="$REPO_ROOT/scripts/ai/workers"
TASKS_INDEX="$SCRIPT_DIR/tasks.index.json"
MODELS_REGISTRY="$SCRIPT_DIR/models.registry.json"
VALIDATOR="$SCRIPT_DIR/_validate_job.py"
OUTPUT_DIR="$REPO_ROOT/reports/ai/workers"

# ─── Args ───
JOB_PACKET="${1:-}"
if [ -z "$JOB_PACKET" ]; then
    echo "USAGE: $0 <job_packet.json>" >&2
    exit 1
fi
if [ ! -f "$JOB_PACKET" ]; then
    echo "ERROR: Job packet not found: $JOB_PACKET" >&2
    exit 1
fi
JOB_BASENAME=$(basename "$JOB_PACKET" .json)

# ─── Git clean check ───
cd "$REPO_ROOT"
if ! git diff --quiet 2>/dev/null; then
    echo "BLOCKED: git working tree has unstaged changes. Stash or commit before running." >&2
    exit 2
fi
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    echo "BLOCKED: git working tree has untracked files. Clean before running." >&2
    exit 2
fi

# ─── Execute validation ───
export TASKS_INDEX_PATH="$TASKS_INDEX"
export MODELS_REGISTRY_PATH="$MODELS_REGISTRY"
export JOB_PACKET_PATH="$JOB_PACKET"
export OUTPUT_DIR_PATH="$OUTPUT_DIR"
export REPO_ROOT="$REPO_ROOT"

mkdir -p "$OUTPUT_DIR"

VALIDATION_JSON=$(timeout "$TIMEOUT_SEC" python3 "$VALIDATOR" 2>&1) || {
    RC=$?
    echo "=== RUNNER LOCK: VALIDATION FAILED ==="
    echo "$VALIDATION_JSON" | python3 -c "
import json,sys
try:
    d = json.loads(sys.stdin.read())
    for e in d.get('errors',[]): print(f'  ERROR: {e}')
    for w in d.get('warnings',[]): print(f'  WARN: {w}')
except:
    print(sys.stdin.read())
" 2>/dev/null || echo "$VALIDATION_JSON"

    FAILED_REPORT="$OUTPUT_DIR/${JOB_BASENAME}_FAILED.md"
    cat > "$FAILED_REPORT" <<EOF
# VALIDATION_FAILED — $JOB_BASENAME

## TIMESTAMP
$(date -u +"%Y-%m-%dT%H:%M:%SZ")

## RAW_OUTPUT
\`\`\`
$VALIDATION_JSON
\`\`\`

## VERDICT_DRAFT_ONLY
BLOCKED — runner lock validation failed at $(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF
    echo "FAILED report: $FAILED_REPORT"
    exit $RC
}

# ─── Parse & render prompt ───
VALIDATION_FILE="$OUTPUT_DIR/.validation_${JOB_BASENAME}.json"
echo "$VALIDATION_JSON" > "$VALIDATION_FILE"
export VALIDATION_FILE

python3 << PYEOF
import json, sys, os
from datetime import datetime, timezone

with open(os.environ['VALIDATION_FILE']) as f:
    d = json.load(f)
job_id = d['job_id']
output_dir = os.environ['OUTPUT_DIR_PATH']
prompt_file = f'/tmp/{job_id}_PROMPT.txt'

sections = '\n'.join(f'{i+1}. {s}' for i, s in enumerate(d['required_sections']))
denied_cmds = '\n'.join(f'  - {c}' for c in d['denied_commands'])
denied_in = '\n'.join(f'  - {p}' for p in d['denied_inputs'])
inputs = '\n'.join(f'  - {i}' for i in d['allowed_inputs'])
invariants = '\n'.join(f'  - {k}: {v}' for k, v in d['global_invariants'].items())
warnings_text = '\n'.join(f'  - {w}' for w in d['warnings']) if d['warnings'] else '  None'

prompt = f"""# STRICT WORKER TASK — {job_id}
## VALIDATION: PASS
## TIMESTAMP: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}

### JOB
- JOB_ID: {job_id}
- TASK_TYPE: {d['task_type']}
- WORKER: {d['default_worker']}
- AUTONOMY_MAX: {d['autonomy_max']}
- WRITES_CODE: {d['writes_code']}
- VALID_WORKERS: {', '.join(d['valid_workers'])}

### ALLOWED_INPUTS
{inputs}

### REQUIRED_OUTPUT_SECTIONS
{sections}

### GLOBAL_INVARIANTS
{invariants}

### DENIED_COMMANDS
{denied_cmds}

### DENIED_INPUT_PATTERNS
{denied_in}

### WARNINGS
{warnings_text}

### INSTRUCTIONS
1. Read ONLY the allowed_inputs listed above.
2. Do NOT modify any file in the repository.
3. Do NOT execute any denied command.
4. Do NOT read any secret, .env, token, key, or credential file.
5. Produce output DRAFT_ONLY in: {d['output_file']}
6. Include ALL required sections in your output.
7. End your output with: ## VERDICT_DRAFT_ONLY
"""

with open(prompt_file, 'w') as f:
    f.write(prompt)

print(f'=== RUNNER LOCK: VALIDATION PASSED ===')
print(f'JOB: {job_id}')
print(f'TASK: {d["task_type"]}')
print(f'WORKER: {d["default_worker"]}')
print(f'AUTONOMY: {d["autonomy_max"]}')
print(f'PROMPT: {prompt_file}')
print(f'OUTPUT: {d["output_file"]}')
print()
print(f'To execute: feed PROMPT to the worker model, save output to {d["output_file"]}')
if d['warnings']:
    for w in d['warnings']:
        print(f'WARNING: {w}')
PYEOF

rm -f "$VALIDATION_FILE"
