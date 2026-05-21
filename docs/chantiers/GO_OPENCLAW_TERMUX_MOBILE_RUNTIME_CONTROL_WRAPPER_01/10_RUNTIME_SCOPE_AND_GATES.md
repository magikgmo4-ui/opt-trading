---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01_RUNTIME_SCOPE_AND_GATES
doc_type: runtime_scope
go_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01
status: open
updated_at: 2026-05-21
---

# 10_RUNTIME_SCOPE_AND_GATES

## Runtime scope initial

Le wrapper runtime initial doit couvrir uniquement les classes d'actions suivantes :

| Class | Runtime allowed | Notes |
|---|---|---|
| status | yes | read-only |
| list-jobs | yes | read-only, phase-filtered |
| preflight | yes | read-only checks |
| run-dry | yes | Phase 01 local-only jobs only |
| evidence | yes | read-only evidence lookup |
| approve | no | HITL packet support later |
| external write | no | Phase 08 only, out of scope |
| signal/trading | no | out of scope |

## Input gates

Before any run, the wrapper must verify:

- requested phase exists;
- requested job exists in the register or phase packet;
- job mode is read-only, dry-run or local-only;
- job has expected evidence definition;
- job is not signal/trading;
- job does not require external write;
- repo root can be resolved;
- output folder can be created under reports/ai/mobile_control.

## Output gates

Every wrapper call must emit:

- action class;
- phase;
- job id when applicable;
- timestamp;
- PASS / PRECHECK_PASS / BLOCKED_WITH_REASON / FAIL;
- evidence path;
- safety summary.

## Block conditions

The wrapper must block when:

- job is not in the allowed phase/job list;
- job requires external write;
- job is signal/trading;
- job requires secret access;
- job requires destructive Git operation;
- job lacks an evidence target;
- command mapping is unknown.

## Phase 01 allowed jobs

The first implementation should only hard-map Phase 01 jobs documented by the parent rollout:

- repo-status-check
- repo-diff-check
- repo-pr-audit
- automation-health-status
- ledger-heartbeat
- ledger-replay-check
- anti-leak-scan
- capability-matrix-validate
- ai-team-handoff-dry-run
- hitl-scenarios-smoke
- localcms-automation-status-sync
- strict-worker-readonly-smoke as precheck/follow-up only

## Non-goals

- no scheduler activation;
- no daemon;
- no external app write;
- no mobile secret handling;
- no trading/signal execution;
- no automatic commit/merge/push workflow.
