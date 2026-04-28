---
doc_id: GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01_BRANCH_PROOF_MATRIX
doc_type: proof_matrix
repo: opt-trading
project: opt-trading
module:
  go_id: GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01
status: open
lifecycle_stage: proof_matrix
topic_keys:
  - opt-trading
  - doc_ops
  - branch_arbitration
  - branch_cleanup
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/00_cadrage.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/03_branch_arbitrage_seed.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01/01_audit_a_verifier.md
---

# GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01 — branch proof matrix

## ETABLI

- Branche GO: `go/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01`
- Base canonique: `sot/mainline`
- Source seed: `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/03_branch_arbitrage_seed.md`
- Branches seed traitées: `7`
- Suppression exécutée: non
- Merge exécuté: non
- Modification `docs/index/BRANCH_STATE.md`: non
- Périmètre: preuve documentaire seulement

## TABLEAU_PREUVE

| BRANCH | INTENTION | EXISTS_LOCAL | EXISTS_REMOTE | SCOPE_REAL | STATUS_VS_MAINLINE | AHEAD_BY | BEHIND_BY | FILES_AHEAD_SUMMARY | PROVISIONAL_DECISION | COMMAND_CANDIDATE | EXECUTION_STATUS |
| --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| `wip/GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01` | DROP_LOCAL_ONLY_CANDIDATE | FROM_AUDIT_TO_VERIFY | NO | local_only_unverified | REMOTE_ABSENT_LOCAL_AUDIT_DIVERGED | 1 | 123 | audit snapshot only; remote absent after branch search | BLOCKED_NEEDS_LOCAL_PROOF | `git branch -D wip/GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01` after local proof | NOT_EXECUTED |
| `METHODE_MULTI_MACHINE_GIT_SYNC` | DROP_REMOTE_CANDIDATE | NOT_CHECKED | YES | remote_only_by_current_github_check | DIVERGED | 14 | 92 | `METHODE_MULTI_MACHINE_GIT_SYNC.md`, `METHODE_OUVERTURE_GO_PARENT_BRANCH_FIRST.md`, `docs/INDEX.md`, AI team architecture docs | READY_TO_DELETE_REMOTE_PENDING_FINAL_CONFIRM | `git push origin --delete METHODE_MULTI_MACHINE_GIT_SYNC` | NOT_EXECUTED |
| `feat/journal-api-extractor-v1` | DROP_LOCAL_ONLY_CANDIDATE | FROM_AUDIT_TO_VERIFY | NO | local_only_unverified | REMOTE_ABSENT_LOCAL_AUDIT_DIVERGED | 6 | 235 | audit snapshot only; remote absent after branch search | BLOCKED_NEEDS_LOCAL_PROOF | `git branch -D feat/journal-api-extractor-v1` after local proof | NOT_EXECUTED |
| `audit/opt-trading-20260320a` | DROP_REMOTE_CANDIDATE | NOT_CHECKED | YES | remote_only_by_current_github_check | DIVERGED | 20 | 686 | `audit/2026-03-20/*`, `docs/ot/*`, `student/validation/*`, very large `journal.md`, plus legacy removals | READY_TO_DELETE_REMOTE_PENDING_FINAL_CONFIRM | `git push origin --delete audit/opt-trading-20260320a` | NOT_EXECUTED |
| `docs/github-park-parent-closeout-01` | CLOSEOUT_ONLY_REVIEW | NOT_CHECKED | YES | remote_only_by_current_github_check | DIVERGED | 1 | 131 | only `docs/index/GO_INDEX.md` modified; no closeout file visible in current compare | BLOCKED_NEEDS_REVIEW | no merge/delete; inspect commit then decide | NOT_EXECUTED |
| `docs/github-park-pass-close-01` | CLOSEOUT_ONLY_REVIEW | NOT_CHECKED | YES | remote_only_by_current_github_check | DIVERGED | 4 | 131 | adds `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/90_closeout.md`; modifies `ACTIVE_STREAMS.md`, `GO_INDEX.md`, `REPRISE.md` | READY_FOR_CLOSEOUT_IMPORT_REVIEW | selective import / cherry-pick only after review | NOT_EXECUTED |
| `feat/go-strategy-docs-v1` | CLOSEOUT_ONLY_REVIEW | NOT_CHECKED | YES | remote_only_by_current_github_check | DIVERGED | 1 | 732 | adds `docs/strategy/INDEX.md`; not a closeout file | REFERENCE_ONLY_OR_BLOCKED_NEEDS_REVIEW | no merge/delete; inspect whether strategy index still useful | NOT_EXECUTED |

## CLOSEOUT_ONLY_DETAILS

### `docs/github-park-parent-closeout-01`

- Remote exists: yes.
- Current compare vs `sot/mainline`: `ahead_by=1`, `behind_by=131`, `DIVERGED`.
- Files ahead: `docs/index/GO_INDEX.md` only.
- Provisional decision: `BLOCKED_NEEDS_REVIEW` because the branch name says closeout, but the visible delta is an index modification, not a closeout artifact.

### `docs/github-park-pass-close-01`

- Remote exists: yes.
- Current compare vs `sot/mainline`: `ahead_by=4`, `behind_by=131`, `DIVERGED`.
- Files ahead:
  - `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/90_closeout.md`
  - `docs/index/ACTIVE_STREAMS.md`
  - `docs/index/GO_INDEX.md`
  - `docs/index/REPRISE.md`
- Provisional decision: `READY_FOR_CLOSEOUT_IMPORT_REVIEW` because a closeout artifact is visible, but the index updates must be reviewed before any import.

### `feat/go-strategy-docs-v1`

- Remote exists: yes.
- Current compare vs `sot/mainline`: `ahead_by=1`, `behind_by=732`, `DIVERGED`.
- Files ahead: `docs/strategy/INDEX.md`.
- Provisional decision: `REFERENCE_ONLY_OR_BLOCKED_NEEDS_REVIEW` because the delta is a strategy index, not a closeout artifact.

## DROP_CANDIDATE_DETAILS

### Local-only candidates

The following branches are not visible as remote branches in the current GitHub branch search and were local in the previous cleanup audit. They require local terminal proof before deletion:

- `wip/GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01`
- `feat/journal-api-extractor-v1`

Candidate proof commands:

```powershell
git branch --list "wip/GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01"
git branch --list "feat/journal-api-extractor-v1"
git branch -r --list "origin/wip/GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01"
git branch -r --list "origin/feat/journal-api-extractor-v1"
```

Deletion commands are candidates only and must not be executed until local proof is confirmed:

```powershell
git branch -D wip/GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01
git branch -D feat/journal-api-extractor-v1
```

### Remote deletion candidates

The following branches are visible as remote branches and match user deletion intent:

- `METHODE_MULTI_MACHINE_GIT_SYNC`
- `audit/opt-trading-20260320a`

Candidate commands, not executed:

```powershell
git push origin --delete METHODE_MULTI_MACHINE_GIT_SYNC
git push origin --delete audit/opt-trading-20260320a
```

## HYPOTHESIS

- Local-only branches may already be absent from one or more machines; local proof is required before marking them `READY_TO_DELETE_LOCAL`.
- `docs/github-park-parent-closeout-01` may be obsolete or partially absorbed, but the current visible delta is not sufficient for import.
- `feat/go-strategy-docs-v1` may be useful as reference, but it is not a closeout-only artifact from the visible file list.

## 12_INVARIANTS

- Aucune suppression exécutée.
- Aucun merge exécuté.
- Aucune modification `docs/index/BRANCH_STATE.md`.
- Commandes documentées seulement.
- Toute suppression réelle exige validation explicite après preuve.

## 16_TODO

1. Valider la matrice de preuve.
2. Confirmer les deux branches local-only sur la machine cible.
3. Produire `02_execution_plan.md` avec commandes séparées par type: local delete, remote delete, closeout-only review.
4. Demander validation explicite avant toute suppression réelle.

## 17_RESUME_POINT

```powershell
cd C:\Users\ghost\opt-trading
git fetch origin --prune
git checkout go/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01
git status --short --branch
git rev-list --left-right --count origin/sot/mainline...HEAD
```

Prochaine action:

```text
Produire docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/02_execution_plan.md après validation de cette matrice.
```
