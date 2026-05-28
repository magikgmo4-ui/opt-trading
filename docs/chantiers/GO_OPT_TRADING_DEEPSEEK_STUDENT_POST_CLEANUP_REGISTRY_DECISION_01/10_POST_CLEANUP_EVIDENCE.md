---
go_id: GO_OPT_TRADING_DEEPSEEK_STUDENT_POST_CLEANUP_REGISTRY_DECISION_01
doc_type: POST_CLEANUP_EVIDENCE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 10_POST_CLEANUP_EVIDENCE

## Established post-cleanup state

1. `student/scripts/` is now the canonical runtime and operator surface.

2. `scripts/student/` no longer carries primary behavior for the covered entrypoints; it is a shim compatibility layer toward `student/scripts/`.

3. `modules/deepseek_student/` remains explicitly non-runtime and documentary/scaffold in nature.

4. Central registries already describe the DeepSeek family through:
- `deepseek_hub` as operator/documentary hub
- `deepseek_response` as active compatibility component
- `deepseek_thinking` as active compatibility component

5. The central registry model still uses module-oriented entries in `registry/modules_registry.yaml`.

## Consequence

The surviving object after cleanup is not a normal module directory under `modules/`.

It is a student-side runtime surface (`student/scripts/`) plus a legacy shim layer (`scripts/student/`).

That makes a naive central module entry `deepseek_student` less natural now than before, not more.

## Central representation options after cleanup

### Option A — permanent exclusion from central registries

Pros:
- avoids forcing a module-shaped registry object onto a non-module runtime surface
- keeps `deepseek_hub` as the family-level operator abstraction
- avoids duplicating central truth for a compatibility alias

### Option B — central `legacy`

Pros:
- matches the compatibility role better than `transitional`

Cons:
- still requires deciding what the central object really is
- risks representing an alias/shim rather than a canonical module surface

### Option C — central `transitional`

Pros:
- matches prior migration wording

Cons:
- cleanup already converged the runtime truth
- the remaining role is compatibility, not active transition leadership
