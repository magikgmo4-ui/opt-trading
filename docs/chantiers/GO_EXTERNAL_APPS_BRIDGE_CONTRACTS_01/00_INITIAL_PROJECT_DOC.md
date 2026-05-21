---
doc_id: GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-21
links:
  - config/machine_runtime_map.yml
  - modules/airtable_bridge/
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md
  - docs/index/inbox/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_MACHINE_RUNTIME_MAP_01.md
---

# GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01

## Objectif

Contractualiser toutes les apps externes avec un `APP_BRIDGE_CONTRACT` commun : permissions, logs, gates, rollback (GAP_04 du parent).

## Périmètre

Apps à contractualiser :
- Airtable
- ClickUp
- Botpress
- Google Sheets
- Telegram
- Gmail
- Calendar
- Drive
- Figma
- LocalCMS

## Preuve concrète pour l'ouverture

- `config/machine_runtime_map.yml` déclare des surfaces machines qui interagissent avec ces apps
- `modules/airtable_bridge/` existe (bridge partiel)
- Classification apps existante dans `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md`

## Livrables

- Template `APP_BRIDGE_CONTRACT` (commun à toutes les apps)
- Contrat rempli pour chaque app
- Relier chaque contrat à la matrice de capacité (GAP_01)
- Valider les actions interdites par contrat
