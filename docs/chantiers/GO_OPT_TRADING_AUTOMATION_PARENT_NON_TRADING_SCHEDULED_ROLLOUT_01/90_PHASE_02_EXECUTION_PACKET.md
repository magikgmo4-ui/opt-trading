---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_PHASE_02_EXECUTION_PACKET
doc_type: execution_packet
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: active
---

# 90_PHASE_02_EXECUTION_PACKET

## Goal

Execute the repo/docs/governance and strict-workers hardening wave.

## Phase 02 exact jobs

| job_id | exact command or asset | ready_now | expected evidence | gap |
|---|---|---|---|---|
| `repo-branch-audit` | `git branch -a --merged` + `git branch -a --no-merged` | yes | merged/orphan branch report | none |
| `repo-go-index-audit` | compare `docs/chantiers/` vs `docs/index/inbox/` | partial | coverage report | needs tiny audit runner |
| `repo-doc-frontmatter-lint` | frontmatter scan over `docs/chantiers/**/*.md` | partial | lint report | needs lint runner |
| `repo-doc-link-check` | markdown link scan | partial | link report | needs link checker |
| `repo-closeout-eligibility-check` | audit on closeout docs/state | partial | closable GO report | needs rules runner |
| `repo-parent-coverage-board-refresh` | draft-only doc refresh | partial | draft patch | manual/HITL workflow |
| `repo-memory-bricks-candidate-scan` | scan docs for `19_TO_REMEMBER` candidates | partial | candidate list | needs scan runner |
| `repo-changelog-digest` | `git log --since='1 day ago' --oneline` | yes | digest report | none |
| `repo-orphan-files-audit` | `git ls-files --others --exclude-standard` | yes | orphan file report | none |
| `repo-scope-guard` | compare diff scope against GO path | partial | scope report | needs policy runner |
| `repo-pr-review-preflight` | aggregate `git status` + `git diff --check` + PR metadata | yes | preflight checklist | none |
| `repo-release-note-draft` | synthesize commits into draft note | partial | draft release note | needs draft runner |
| `strict-worker-model-registry-check` | validate `scripts/ai/workers/models.registry.json` | yes | registry validation output | none |
| `strict-worker-task-index-check` | validate `scripts/ai/workers/tasks.index.json` | yes | task index validation output | none |
| `strict-worker-job-packet-validate` | reuse `_validate_job.py` across packets | yes | packet validation report | none |
| `strict-worker-output-schema-check` | inspect generated report structure | partial | output schema report | needs schema runner |
| `strict-worker-denied-command-scan` | scan prompts/reports for denied patterns | partial | denied command report | needs scanner |
| `strict-worker-log-archive` | archive worker logs/reports | partial | archive artifact | needs archiver |
| `strict-worker-failure-report` | summarize FAIL/BLOCKED jobs | partial | failure report | needs reporter |

## Summary

- Ready now: `7/19`
- Partial: `12/19`
- Blocked: `0/19`

## Recommended execution order

### Phase 02A

Run the ready-now set first:

1. `repo-branch-audit`
2. `repo-changelog-digest`
3. `repo-orphan-files-audit`
4. `repo-pr-review-preflight`
5. `strict-worker-model-registry-check`
6. `strict-worker-task-index-check`
7. `strict-worker-job-packet-validate`

### Phase 02B

Do not derive runners first.

Review the `12` partial jobs directly from execution needs, and only then decide
whether a tiny runner, a manual protocol, or an existing command is sufficient.

Phase 02B review outcome:

- `1` runnable_as_is
- `6` manual_protocol_enough
- `5` tiny_helper_needed

Reference: `92_PHASE_02B_GAP_REVIEW.md`

Execution outcome so far:

- `Phase 02A`: `7 PASS`
- `Phase 02B1`: `6 PASS`
- `Phase 02B2`: `1 PASS`
- Remaining: `5 tiny_helper_needed`
