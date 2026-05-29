---
doc_id: GO_OPT_TRADING_RUNS_VALIDATION_BACKLOG_CANONICALIZE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RUNS_VALIDATION_BACKLOG_CANONICALIZE_01
status: active
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
GO_ID: GO_OPT_TRADING_RUNS_VALIDATION_BACKLOG_CANONICALIZE_01
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: null
MASTER_TARGET_ID: null
MASTER_PROJECT_PLAN_ID: null
PARENT_GO_ID: GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
NEXT_ATTACH_TARGET: null
6_FINAL_TARGET: canonicaliser le backlog des runs/phases/verifications en attente dans un registre unique
BUNDLE_TARGET: docs/index/RUNS_VALIDATION_BACKLOG_01.md
TRANSPORT_MODE: none
CLOSE_GATE_MASTER_TARGET: not_applicable
topic_keys:
  - runs
  - validation
  - backlog
  - phases
  - machines
  - github_actions
  - openclaw
  - runtime
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_RUNS_VALIDATION_BACKLOG_CANONICALIZE_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/index/RUNS_VALIDATION_BACKLOG_01.md
  - docs/index/inbox/GO_OPT_TRADING_RUNS_VALIDATION_BACKLOG_CANONICALIZE_01.md
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Disposer d'un registre canonique, relisible et actionnable des runs, phases, validations en attente et verifications ulterieures, afin d'eviter que les preuves restent dispersees entre docs de chantiers, machines, emails GitHub Actions, automations et sorties de sessions.

## 3_INITIAL_NEED

L'utilisateur a constate que plusieurs runs ont ete lances sur differentes machines et differents chantiers pour verification ulterieure, mais que les runs, phases et dates de verification n'ont pas ete listes centralement.

Demande validee : faire une passe de verification sur les mots plausibles :

```text
run, runs, phase, PHASE, execution, execution_log, validation, pending, PENDING,
DRAFT_ONLY, PRECHECK_PASS, PASS_WITH_WARNINGS, PARTIAL_PASS, BLOCKED,
CLOSEOUT_BLOCKED, NOT_PROVEN, FIXTURE_ONLY, follow-up, a verifier, verification,
attente, a terme
```

Machines/surfaces a recroiser :

```text
student, db-layer, fantome, admin-trading, cursor-ai, windows, mobile, Termux,
GitHub Actions, automations ChatGPT
```

## 4_MASTER_PROJECT_PLAN

Ce chantier ne ferme aucun parent et ne relance aucun run. Il cree uniquement une base canonique documentaire :

1. ouvrir un child GO documentaire rattache a la continuite Doc Ops ;
2. creer `docs/index/RUNS_VALIDATION_BACKLOG_01.md` comme registre principal ;
3. creer l'entree inbox locale du GO ;
4. inscrire les runs/validations deja identifies avec statut et prochaine action ;
5. conserver les index globaux inchanges, sauf mission dediee.

## 6_FINAL_TARGET

Livrer un registre initial `RUNS_VALIDATION_BACKLOG_01.md` contenant les runs et phases detectes comme :

- `DUE_NOW` ;
- `SCHEDULED` ;
- `BLOCKED_BY_CI_SCOPE` ;
- `PARTIAL_PASS` ;
- `PASS_WITH_WARNINGS` ;
- `FIXTURE_ONLY_OR_NOT_PROVEN`.

## 8_VALIDATED_PLAN

Plan valide par l'utilisateur : creer un ledger canonique avec colonnes :

```text
RUN_ID | GO_ID | machine | branch | commit | run_date | status | evidence_path | verification_due_date | next_action
```

## 9_SELECTED_SOLUTION

Solution retenue : documentation canonique repo-first, sans execution runtime ni modification des index globaux.

## 10_SELECTED_SETUP

- Branche : `go/GO_OPT_TRADING_RUNS_VALIDATION_BACKLOG_CANONICALIZE_01`
- Parent rattache : `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`
- Registre principal : `docs/index/RUNS_VALIDATION_BACKLOG_01.md`
- Inbox locale : `docs/index/inbox/GO_OPT_TRADING_RUNS_VALIDATION_BACKLOG_CANONICALIZE_01.md`

## 12_INVARIANTS

- Ne pas fermer de GO parent.
- Ne pas relancer GitHub Actions.
- Ne pas ecrire sur machines runtime.
- Ne pas modifier les index globaux dans ce chantier.
- Ne pas convertir un `PASS_WITH_WARNINGS`, `PARTIAL_PASS`, `PRECHECK_PASS` ou `FIXTURE_ONLY` en `PASS_FULL` sans preuve nouvelle.

## 17_RESUME_POINT

```text
CANONICAL_NEXT = maintenir docs/index/RUNS_VALIDATION_BACKLOG_01.md
PRIMARY_DUE_NOW = strict-worker-readonly-smoke + OpenClaw db-layer->fantome remediation
SCHEDULED_CHECK = Fleet Health Phase 1 le 2026-05-30 09:00
CI_BLOCKERS = Gated PR file-scope/no-lock-overlap + Strict Workers job packets
```
