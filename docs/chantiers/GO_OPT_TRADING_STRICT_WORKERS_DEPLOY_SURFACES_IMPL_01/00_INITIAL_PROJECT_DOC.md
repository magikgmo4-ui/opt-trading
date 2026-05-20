---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: strict_workers
go_id: GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01
machine: fantome
status: draft_canonical
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - strict_workers
  - deployment
  - workflows
  - systemd
  - runtime_map
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01/20_CLASSIFICATION_REVIEW.md
point_de_reprise: "Apres PR #648 mergee et validation du bucket 1, ouvrir un GO repo-only borne aux surfaces deploy/workflows strict-workers sans toucher aux familles hors scope"
updated_at: 2026-05-20
links:
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/chantiers/GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01/00_classification_matrix.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01/20_CLASSIFICATION_REVIEW.md
  - .github/workflows/strict-workers-validate.yml
  - .github/workflows/strict-workers-smoke.yml
  - deploy/systemd/opt-trading-fleet-orchestrator.service
  - deploy/systemd/opt-trading-runtime-health.service
  - config/machine_runtime_map.yml
---

# GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01 — 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir un GO repo-only borne a l'implementation des surfaces bucket 1 strict-workers orchestration/deployment deja classees et validees en doc-only, sans relancer de discovery globale et sans toucher aux familles hors scope.

## 2_REPRISE_GATE

Preuve de reprise relue avant ouverture:

- `docs/index/GO_INDEX.md` confirme `8 GO non clos retenus`
- `docs/index/ACTIVE_STREAMS.md` confirme `8 GO non clos retenus`
- `docs/index/REPRISE.md` confirme `8 GO non clos retenus`
- `docs/index/NEXT_GO_CANDIDATES.md` confirme `8 GO non clos retenus`
- PR #645 mergee : matrice de classification AI / strict-workers / apps
- PR #646 mergee : bucket 1 ouvert en review doc-only
- PR #648 mergee : cardinalite active realignee a 8 GO

## 3_SCOPE_STRICT

Surfaces autorisees pour la suite d'implementation de ce GO:

1. `.github/workflows/strict-workers-validate.yml`
2. `.github/workflows/strict-workers-smoke.yml`
3. `deploy/systemd/opt-trading-fleet-orchestrator.service`
4. `deploy/systemd/opt-trading-fleet-orchestrator.timer`
5. `deploy/systemd/opt-trading-runtime-health.service`
6. `deploy/systemd/opt-trading-runtime-health.timer`
7. `deploy/systemd/overrides/*`
8. `config/machine_runtime_map.yml`
9. `modules/*/systemd/*` uniquement comme surfaces adjacentes si un raccord repo-side est strictement necessaire

## 4_EXCLUSIONS

Ne pas toucher dans ce GO:

- `.github/workflows/strict-workers-schedule.yml`
- `modules/strategy/*`
- `tools/strategy/validate_strategy_registry.py`
- `modules/airtable_bridge/*`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_*`
- `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_*`
- Botpress, Ollama, Google Sheets, Event taxonomy, DeskPro input
- les index globaux `docs/index/*`

## 5_IMPLEMENTATION_RULES

1. Repo-only: aucun `systemctl`, aucune activation timer/service, aucun write runtime machine.
2. Les changements doivent rester limites aux artefacts versionnes du repo.
3. Toute modification de `config/machine_runtime_map.yml` doit rester strictement motivee par le bucket 1.
4. Si une adaptation releve uniquement du canon machine/runtime, ouvrir un GO separe au lieu d'elargir celui-ci.

## 6_TARGET_BRANCH

Branche dediee de travail:

`go/GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01`

## 7_EXPECTED_NEXT_STEP

Suite immediate attendue apres cette ouverture:

1. relire les artefacts bucket 1 deja classes
2. choisir le plus petit lot repo-only correct
3. implementer sans melanger strategy, Airtable, OpenClaw policy ou OpenClaw DBLayer
