#!/usr/bin/env python3
"""Strict workers job packet validator — called by run_task.sh"""
import json, sys, os, fnmatch, glob as gmod

tasks_idx = os.environ['TASKS_INDEX_PATH']
models_reg = os.environ['MODELS_REGISTRY_PATH']
packet_file = os.environ['JOB_PACKET_PATH']
output_dir = os.environ['OUTPUT_DIR_PATH']

with open(tasks_idx) as f:  tasks = json.load(f)
with open(models_reg) as f: models = json.load(f)
with open(packet_file) as f: packet = json.load(f)

errors = []
warnings = []

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

task_defs = tasks.get('tasks', {})
if task_type not in task_defs:
    errors.append(f'UNKNOWN_TASK_TYPE: {task_type} not in tasks.index.json')

all_models = models.get('models', {})
verified = {k for k, v in all_models.items() if v.get('status') == 'VERIFIED'}
if not verified:
    errors.append('NO_VERIFIED_MODELS_IN_REGISTRY')

valid = [w for w in candidates if w in verified]
if not valid:
    errors.append(f'NO_VERIFIED_WORKER: candidates={candidates}, verified={sorted(verified)}')

if default_worker not in candidates:
    warnings.append(f'DEFAULT_NOT_IN_CANDIDATES: {default_worker} not in {candidates}')
if default_worker not in verified:
    errors.append(f'DEFAULT_WORKER_NOT_VERIFIED: {default_worker}')

denied_patterns = tasks.get('denied_inputs', [])
allowed_inputs = scope.get('allowed_inputs', [])

for fpath in allowed_inputs:
    matches = gmod.glob(fpath, recursive=True)
    if not matches:
        errors.append(f'INPUT_NOT_FOUND: {fpath}')
    for pattern in denied_patterns:
        if fnmatch.fnmatch(fpath, pattern):
            errors.append(f'DENIED_INPUT: {fpath} matches denied pattern {pattern}')

allowed_outputs = scope.get('allowed_outputs', [])
output_file = os.path.join(output_dir, f'{job_id}.md')
out_ok = any(fnmatch.fnmatch(output_file, pat) for pat in allowed_outputs)
if not out_ok:
    errors.append(f'OUTPUT_NOT_ALLOWED: {output_file} not in allowed_outputs={allowed_outputs}')

denied_cmds = tasks.get('denied_commands', [])

if errors:
    print(json.dumps({"status": "FAILED", "errors": errors, "warnings": warnings}))
    sys.exit(1)

task_def = task_defs[task_type]
result = {
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
print(json.dumps(result))
