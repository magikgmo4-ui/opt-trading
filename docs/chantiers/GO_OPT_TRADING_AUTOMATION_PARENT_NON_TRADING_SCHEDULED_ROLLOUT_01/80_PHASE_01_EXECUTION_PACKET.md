---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_PHASE_01_EXECUTION_PACKET
doc_type: execution_packet
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: active
---

# 80_PHASE_01_EXECUTION_PACKET

## Base

Execution Phase 01 reprise depuis `PR #678`, donc depuis les assets reellement
livres dans `origin/sot/mainline`.

## Phase 01 exact jobs

| job_id | source asset | exact command | ready_now | expected evidence | gap |
|---|---|---|---|---|---|
| `repo-status-check` | git builtin | `git status --short --branch` | yes | branch/state output | none |
| `repo-diff-check` | git builtin | `git diff --check` | yes | whitespace/conflict output | none |
| `repo-pr-audit` | gh builtin | `gh pr list --state all --limit 50` | yes | PR digest output | none |
| `strict-worker-readonly-smoke` | `scripts/ai/workers/run_task.sh` + `GO_STRICT_WORKERS_READONLY_SMOKE_01.json` | `bash scripts/ai/workers/run_task.sh scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json` | yes | runner output + report artifact | requires clean git worktree |
| `ledger-heartbeat` | `scripts/ai/workers/ledger_writer.py` | `python3 scripts/ai/workers/ledger_writer.py --event-type HEARTBEAT --actor-id scheduler --surface-id automation --action HEARTBEAT --status PASS --payload '{}'` | yes | appended ledger event | none |
| `ledger-replay-check` | `scripts/ai/workers/ledger_replay.py` | `python3 scripts/ai/workers/ledger_replay.py --replay` | yes | replay summary | requires existing ledger file |
| `automation-health-status` | `scripts/ai/workers/health_status.py` | `python3 scripts/ai/workers/health_status.py --output reports/ai/health_status.json` | yes | `reports/ai/health_status.json` | none |
| `anti-leak-scan` | `scripts/ai/tests/anti_leak_tests.py` | `python3 scripts/ai/tests/anti_leak_tests.py` | yes | anti-leak test output | may create default kill switch file |
| `hitl-scenarios-smoke` | `scripts/ai/tests/hitl_scenarios.py` | `python3 scripts/ai/tests/hitl_scenarios.py` | yes | scenario PASS output | none |
| `capability-matrix-validate` | `scripts/ai/tests/g01_validate_scenarios.py` | `python3 scripts/ai/tests/g01_validate_scenarios.py` | yes | `scenario_results/*.json` | writes evidence in chantier docs |
| `ai-team-handoff-dry-run` | `scripts/ai/tests/g03_dry_run_handoff.py` | `python3 scripts/ai/tests/g03_dry_run_handoff.py` | yes | `dry_run_output.json` | writes evidence in chantier docs |
| `localcms-automation-status-sync` | `scripts/ai/workers/localcms_automation_status_sync.py` | `python3 scripts/ai/workers/localcms_automation_status_sync.py` | yes | `tmp/localcms_latest.json` + report artifact | none |

## Summary

- Ready now: `12/12`
- Partial: `0/12`
- Blocked: `0/12`

## First execution state

Execution replayed from a temporary worktree based on `origin/sot/mainline`.

- Fully executed PASS: `11/12`
- Runner/preflight PASS only: `1/12`
- Derivation still needed: `0/12`

Breakdown:

- PASS: `repo-status-check`
- PASS: `repo-diff-check`
- PASS: `repo-pr-audit`
- PASS: `ledger-heartbeat`
- PASS: `ledger-replay-check`
- PASS: `automation-health-status`
- PASS: `anti-leak-scan`
- PASS: `capability-matrix-validate`
- PASS: `ai-team-handoff-dry-run`
- PASS: `hitl-scenarios-smoke`
- PASS: `localcms-automation-status-sync`
- PRECHECK_PASS: `strict-worker-readonly-smoke`

## Only missing derivation

`strict-worker-readonly-smoke` has a valid runner/preflight path today, but
the current asset prepares the worker prompt and output target rather than
executing the model end-to-end by itself.

## Recommended run order

1. `repo-status-check`
2. `repo-diff-check`
3. `repo-pr-audit`
4. `ledger-heartbeat`
5. `ledger-replay-check`
6. `automation-health-status`
7. `anti-leak-scan`
8. `strict-worker-readonly-smoke`
9. `capability-matrix-validate`
10. `ai-team-handoff-dry-run`
11. `hitl-scenarios-smoke`
12. `localcms-automation-status-sync`

## Execution note

Phase 01 can start immediately on the `11` ready-now jobs. The pragmatic first
execution unit is therefore:

```text
PHASE_01A = 11 PASS + 1 PRECHECK_PASS
PHASE_01B = optional end-to-end worker execution after runner precheck
```
