---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01_PHASE01_MOBILE_CONTROL_DRY_RUN
doc_type: dry_run_plan
go_id: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01
status: open
updated_at: 2026-05-21
---

# 40_PHASE01_MOBILE_CONTROL_DRY_RUN

## Objectif

Preparer le premier dry-run mobile/Termux pour controler OpenClaw sur la Phase 01 non-trading sans action destructive.

## Base canonique

Phase 01 actuelle :

- 12 jobs selectionnes ;
- 11 PASS ;
- 1 PRECHECK_PASS ;
- 0 FAIL ;
- gate `PHASE_01 = PASS_WITH_FOLLOWUP` ;
- follow-up : `strict-worker-readonly-smoke` en execution modele end-to-end.

## Dry-run cible

Nom propose :

```text
MOBILE_CONTROL_PHASE01_DRY_RUN_01
```

## Sequence dry-run

| Step | Action | Expected result |
|---|---|---|
| 1 | afficher etat OpenClaw/non-trading | status visible |
| 2 | lister jobs Phase 01 | 12 jobs visibles |
| 3 | verifier eligibility mobile | only read-only/dry-run/local-only |
| 4 | preflight repo state | PASS ou BLOCKED_WITH_REASON |
| 5 | preflight ledger | ledger writable local ou readable |
| 6 | refresh health status | report local |
| 7 | replay ledger | replay PASS |
| 8 | run anti-leak scan | PASS |
| 9 | refresh LocalCMS snapshot | tmp/report local |
| 10 | produire dry-run report | report final |

## Jobs Phase 01 autorises depuis mobile au dry-run

| job_id | mobile control | notes |
|---|---|---|
| repo-status-check | yes | read-only |
| repo-diff-check | yes | read-only |
| repo-pr-audit | yes | read-only |
| automation-health-status | yes | local report |
| ledger-heartbeat | yes | local ledger event |
| ledger-replay-check | yes | read-only replay |
| anti-leak-scan | yes | security preflight |
| capability-matrix-validate | yes | local evidence |
| ai-team-handoff-dry-run | yes | dry-run |
| hitl-scenarios-smoke | yes | dry-run |
| localcms-automation-status-sync | yes | local snapshot |
| strict-worker-readonly-smoke | precheck only | full model E2E remains follow-up |

## Success criteria

- no external write ;
- no signal/trading ;
- no secret emitted ;
- each executed job has evidence ;
- ledger event present for orchestrated execution ;
- final report contains PASS / PRECHECK_PASS / BLOCKED_WITH_REASON per job ;
- LocalCMS snapshot refreshed when available.

## Failure criteria

- any job tries to leave non-trading scope ;
- any job lacks evidence ;
- ledger unavailable without fallback report ;
- HITL gate bypass attempted ;
- mobile entry attempts forbidden action.

## Output target future

```text
reports/ai/mobile_control/MOBILE_CONTROL_PHASE01_DRY_RUN_01.json
reports/ai/mobile_control/MOBILE_CONTROL_PHASE01_DRY_RUN_01.md
```

## Next GO apres doc-only

Si ce GO est valide, ouvrir un GO runtime separe pour implementer le wrapper mobile-control ou l'adapter OpenClaw correspondant.
