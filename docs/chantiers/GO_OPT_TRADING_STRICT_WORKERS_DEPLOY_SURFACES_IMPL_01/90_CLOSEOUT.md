---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01_CLOSEOUT
doc_type: closeout
repo: opt-trading
project: opt-trading
module: strict_workers
go_id: GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01
machine: fantome
status: canonical
lifecycle_stage: closeout
topic_keys:
  - opt-trading
  - strict_workers
  - deployment
  - workflows
  - runtime_map
  - closeout
surface: chantier
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01/00_INITIAL_PROJECT_DOC.md
  - .github/workflows/strict-workers-validate.yml
  - .github/workflows/strict-workers-smoke.yml
  - scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json
  - config/machine_runtime_map.yml
  - tests/runtime_health/test_warn_classification.py
---

# GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01 — 90_CLOSEOUT

## Verdict

`PASS_MINIMAL_SCOPE_CLOSED`

## 13_ESTABLISHED

Le GO a ete referme apres trois lots repo-only minimaux, tous dans le perimetre autorise du bucket 1.

### LOT_01 — validate trigger

- PR #651 mergee
- fichier touche: `.github/workflows/strict-workers-validate.yml`
- correction: ajout de `scripts/ai/workers/models.registry.json` dans les `pull_request.paths`
- justification: `_validate_job.py` lit explicitement le registry comme input de validation

### LOT_02 — machine runtime map

- PR #652 mergee
- fichiers touches:
  - `config/machine_runtime_map.yml`
  - `tests/runtime_health/test_warn_classification.py`
- correction: `fantome.optional_timers` inclut maintenant `opt-trading-runtime-health.timer`
- justification: timer deploye et valide dans la continuite repo/doc, mais absent du canon machine/runtime

### LOT_03 — smoke trigger

- PR #653 mergee
- fichier touche: `.github/workflows/strict-workers-smoke.yml`
- correction: ajout des trois docs `docs/agents/strict_workers/*.md` references par `GO_STRICT_WORKERS_READONLY_SMOKE_01.json`
- justification: ces chemins sont des `allowed_inputs` verifies par le smoke packet ; leur suppression/rename doit retrigger le smoke

## 14_SCOPE_REVIEW

Relu pour closeout:

- `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01/00_INITIAL_PROJECT_DOC.md`
- `.github/workflows/strict-workers-validate.yml`
- `.github/workflows/strict-workers-smoke.yml`
- `scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json`
- `config/machine_runtime_map.yml`
- `tests/runtime_health/test_warn_classification.py`

Constat final sur le sous-perimetre minimal:

- validate trigger couvre ses inputs versionnes connus
- smoke trigger couvre desormais ses inputs versionnes verifies
- le canon `fantome` dans `machine_runtime_map.yml` reflète le timer read-only deploye
- aucun besoin prouve de toucher `strict-workers-schedule.yml`, `deploy/systemd/*`, `overrides/*` ou `modules/*/systemd/*` dans ce lot minimal

## 15_REMAINING_GAP

Aucun gap bloquant prouve dans le sous-perimetre minimal traite par ce GO.

Points restant possibles, mais hors closeout minimal:

- une passe future sur `deploy/systemd/*` si un mismatch repo-side explicite est prouve
- une passe future sur `modules/*/systemd/*` si un raccord bucket 1 devient necessaire
- aucune activation runtime ni operation machine-side ne fait partie de ce closeout

## 16_EXCLUSIONS_RESPECTED

Non touches dans ce GO:

- `strict-workers-schedule.yml`
- `modules/strategy/*`
- `tools/strategy/validate_strategy_registry.py`
- `modules/airtable_bridge/*`
- OpenClaw policy / OpenClaw DBLayer
- Botpress, Ollama, Google Sheets, Event taxonomy, DeskPro input
- index globaux `docs/index/*`

L'artefact non suivi suivant n'a pas ete integre au GO ni aux PRs:

- `reports/ai/workers/GO_STRICT_WORKERS_READONLY_SMOKE_01_PROMPT.txt`

## 17_VALIDATIONS

- `python3 tests/runtime_health/test_warn_classification.py` -> `OK (17 tests)` pendant LOT_02
- revues GitHub/PRs mergees:
  - PR #651
  - PR #652
  - PR #653

## 18_POINT_DE_REPRISE

Le GO `GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01` peut etre considere clos pour son lot minimal autorise.

Si une suite est ouverte, elle doit partir d'un nouveau GO borne avec preuve d'un gap concret sur:

1. `deploy/systemd/*`, ou
2. `modules/*/systemd/*`, ou
3. un nouvel ecart `machine_runtime_map.yml` strictement prouve.
