# OPENCLAW_BUILDER_FIRST_LOCAL_EXECUTION_PLAN_01

## Job Definition

```yaml
job_id: BUILDER_FIRST_LOCAL_001
type: sandbox_read_only
scope: repo-local
command_planned: "audit docs/chantiers/ structure via builder"
ssh: BLOCKED
remote: BLOCKED
secrets: none
write: none
risk: LOW
dry_run: true
```

## Execution Plan

1. Gateway check (health) → OK
2. Builder liveness check → OK
3. Job dispatch (local sandbox) → PENDING
4. Output collection → reports/ai/builder/
5. Verification → git status propre
6. Closeout → 90_CLOSEOUT.md

## Gate Status

```text
ALL_CLEAR_FOR_LOCAL_SANDBOX
SSH/remote BLOCKED = acceptable for local-only
No WAN, no bridge, no secrets
Ready for human approval
```

## RISKS

- À qualifier.
