---
doc_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01_INITIAL
doc_type: initial_project_doc
go_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: passed_with_evidence
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-21
links:
  - registry/ui_surfaces_registry.yaml
  - config/machine_runtime_map.yml
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/10_GAPS_REGISTER.md
---

# GO_LOCALCMS_AUTOMATION_COCKPIT_01

## Objectif

Créer le cockpit opérateur LocalCMS : pages automation, workers, jobs, approvals, ledger, signals, safe buttons, kill switch (GAP_11 du parent).

## Périmètre

- Automation overview page
- Workers state page
- Jobs queue page
- Approvals page
- Ledger page
- Signals page
- Safe buttons (actions read-only, redémarrage contrôlé)
- Kill switch visible (coupe-circuit)

## Preuve concrète pour l'ouverture

- `registry/ui_surfaces_registry.yaml` : 21 UI surfaces existantes, cockpit automation manquant
- `config/machine_runtime_map.yml` : machines déclarées avec services et timers à afficher

## Livrables

- 6 pages cockpit documentées (automation, workers, jobs, approvals, ledger, signals)
- Safe buttons design
- Kill switch design
