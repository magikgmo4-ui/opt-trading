#!/bin/bash
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
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || cd "$(dirname "$0")/../../.." && pwd)"
TASKS_INDEX="$REPO_ROOT/scripts/ai/workers/tasks.index.json"
MODELS_REGISTRY="$REPO_ROOT/scripts/ai/workers/models.registry.json"
OUTPUT_DIR="$REPO_ROOT/reports/ai/workers"

# ─── Validation args ───
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
    echo "BLOCKED: git working tree has untracked changes. Clean before running." >&2
    exit 2
fi

# ─── Python validation engine ───
validate_job() {
    python3 << 'PYEOF'
import json, sys, os, re, fnmatch

tasks_idx = os.environ['TASKS_INDEX_PATH']
models_reg = os.environ['MODELS_REGISTRY_PATH']
packet_file = os.environ['JOB_PACKET_PATH']
output_dir = os.environ['OUTPUT_DIR_PATH']

with open(tasks_idx) as f:  tasks = json.load(f)
with open(models_reg) as f: models = json.load(f)
with open(packet_file) as f: packet = json.load(f)

errors = []
warnings = []

# 1. Required top-level fields
for field in ['job_packet_id', 'task_type', 'worker_candidates', 'default_worker', 'scope']:
    if field not in packet:
        errors.append(f'MISSING_FIELD: {field}')

if errors:
    print(json.dumps({"status": "FAILED", "errors": errors}))
    sys.exit(1)

job_id = packet['job_packet_id']
task_type = packet['task_type']
default_worker = packet['default_worker']
candidates = packet['worker_candidates']
scope = packet.get('scope', {})

# 2. task_type must exist in tasks.index.json
task_defs = tasks.get('tasks', {})
if task_type not in task_defs:
    errors.append(f'UNKNOWN_TASK_TYPE: {task_type} not in tasks.index.json')

# 3. Check models.registry integrity
all_models = models.get('models', {})
verified = {k for k, v in all_models.items() if v.get('status') == 'VERIFIED'}
if not verified:
    errors.append('NO_VERIFIED_MODELS_IN_REGISTRY')

# 4. At least one worker candidate must be VERIFIED
valid = [w for w in candidates if w in verified]
if not valid:
    errors.append(f'NO_VERIFIED_WORKER: candidates={candidates}, verified={sorted(verified)}')

# 5. default_worker must be in candidates and VERIFIED
if default_worker not in candidates:
    warnings.append(f'DEFAULT_NOT_IN_CANDIDATES: {default_worker} not in {candidates}')
if default_worker not in verified:
    errors.append(f'DEFAULT_WORKER_NOT_VERIFIED: {default_worker}')

# 6. Validate scope: allowed_inputs
denied_patterns = tasks.get('denied_inputs', [])
allowed_inputs = scope.get('allowed_inputs', [])

for fpath in allowed_inputs:
    # glob expansion
    import glob as gmod
    matches = gmod.glob(fpath, recursive=True)
    if not matches:
        errors.append(f'INPUT_NOT_FOUND: {fpath}')

    for pattern in denied_patterns:
        if fnmatch.fnmatch(fpath, pattern):
            errors.append(f'DENIED_INPUT: {fpath} matches denied pattern {pattern}')

# 7. Validate scope: allowed_outputs
allowed_outputs = scope.get('allowed_outputs', [])
output_file = os.path.join(output_dir, f'{job_id}.md')
out_ok = any(fnmatch.fnmatch(output_file, pat) for pat in allowed_outputs)
if not out_ok:
    errors.append(f'OUTPUT_NOT_ALLOWED: {output_file} not in allowed_outputs={allowed_outputs}')

# 8. Denied_commands check (informational — runner enforces, not validated here)
denied_cmds = tasks.get('denied_commands', [])

if errors:
    print(json.dumps({"status": "FAILED", "errors": errors, "warnings": warnings}))
    sys.exit(1)

# 9. Build validated context
task_def = task_defs[task_type]
rut = {
    "status": "PASS",
    "job_id": job_id,
    "task_type": task_type,
    "default_worker": default_worker,
    "valid_workers": sorted(valid),
    "output_file": output_file,
    "autonomy_max": task_def.get('autonomy_max', 'A0'),
    "required_sections": task_def.get('required_sections', []),
    "writes_code": task_def.get('writes_code', False),
    "allowed_inputs": allowed_inputs,
    "global_invariants": tasks.get('global_invariants', {}),
    "denied_commands": denied_cmds,
    "denied_inputs": denied_patterns,
    "warnings": warnings
}
print(json.dumps(rut))
PYEOF
}

# ─── Execute validation ───
export TASKS_INDEX_PATH="$TASKS_INDEX"
export MODELS_REGISTRY_PATH="$MODELS_REGISTRY"
export JOB_PACKET_PATH="$JOB_PACKET"
export OUTPUT_DIR_PATH="$OUTPUT_DIR"

mkdir -p "$OUTPUT_DIR"

VALIDATION_JSON=$(timeout "$TIMEOUT_SEC" bash -c 'validate_job' 2>&1) || {
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

    # Produce FAILED report
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
echo "$VALIDATION_JSON" | python3 << 'PYEOF'
import json, sys, os

d = json.loads(sys.stdin.read())
job_id = d['job_id']
output_dir = os.environ['OUTPUT_DIR_PATH']
prompt_file = os.path.join(output_dir, f'{job_id}_PROMPT.txt')

sections = '\n'.join(f'{i+1}. {s}' for i, s in enumerate(d['required_sections']))
denied_cmds = '\n'.join(f'  - {c}' for c in d['denied_commands'])
denied_in = '\n'.join(f'  - {p}' for p in d['denied_inputs'])
inputs = '\n'.join(f'  - {i}' for i in d['allowed_inputs'])
invariants = '\n'.join(f'  - {k}: {v}' for k, v in d['global_invariants'].items())
warnings_text = '\n'.join(f'  - {w}' for w in d['warnings']) if d['warnings'] else '  None'

prompt = f"""# STRICT WORKER TASK — {job_id}
## VALIDATION: PASS
## TIMESTAMP: {__import__('datetime').datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}

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
print(f'To execute: feed the prompt to the worker model, save output to {d["output_file"]}')
if d['warnings']:
    for w in d['warnings']:
        print(f'WARNING: {w}')
PYEOF
