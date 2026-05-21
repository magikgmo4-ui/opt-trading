---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01_PHASE01B_IMPLEMENTATION_PLAN
doc_type: implementation_plan
go_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01
status: open
updated_at: 2026-05-21
---

# 30_PHASE01B_IMPLEMENTATION_PLAN

## Goal

Implement a minimal `openclaw_mobile_control.py` wrapper that can exercise Phase 01 mobile-control without external write or signal/trading scope.

## Step 1 — Static job map

Create an internal allowlist for Phase 01 jobs only.

Each entry should include:

- job_id;
- action class;
- command or callable;
- expected evidence;
- allowed write scope;
- status behavior.

## Step 2 — Preflight mode

`preflight` should verify:

- repo root resolution;
- output folder creation;
- selected job exists;
- job is allowed for mobile control;
- job does not require an external write;
- job has evidence target.

## Step 3 — Status and list-jobs

`status` should return a compact repo/mobile-control state.

`list-jobs` should return Phase 01 jobs with mobile eligibility and notes.

## Step 4 — Run-dry

`run-dry` should execute only Phase 01 allowed local/read-only commands.

For the first patch, `strict-worker-readonly-smoke` may remain `PRECHECK_PASS` unless the model E2E path is explicitly available and safe.

## Step 5 — Evidence

The wrapper should write one JSON report per invocation.

Report naming proposal:

```text
reports/ai/mobile_control/<timestamp>_<action>_<job_id_or_all>.json
```

## Step 6 — Validation

Minimum local validation commands for the implementation PR:

```text
python3 scripts/ai/workers/openclaw_mobile_control.py status --json
python3 scripts/ai/workers/openclaw_mobile_control.py list-jobs --phase PHASE_01 --json
python3 scripts/ai/workers/openclaw_mobile_control.py preflight --phase PHASE_01 --job repo-status-check --json
python3 scripts/ai/workers/openclaw_mobile_control.py run-dry --phase PHASE_01 --job repo-status-check --json
```

## Expected first implementation verdict

```text
MOBILE_CONTROL_PHASE01_MINIMAL_WRAPPER_PASS
```

or

```text
BLOCKED_WITH_REASON
```

## Out of scope

- scheduler activation;
- daemon/service install;
- external app write;
- signal/trading chain;
- full model E2E execution unless already safe and allowlisted.
