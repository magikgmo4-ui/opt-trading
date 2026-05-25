---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01
parent_go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: open
lifecycle_stage: inventory
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_GOOGLE_SHEETS_CONSUMER
BUNDLE_TARGET: REPO_FIRST_SHEETS_CSV_TABLE_INVENTORY_V1
NEXT_GO: null
topic_keys:
  - opt-trading
  - google_sheets
  - inventory
  - csv
  - registries
  - fixtures
  - dashboards
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/00_PARENT_UMBRELLA.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/INVENTORY.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/PRODUCER_CONSUMER_MAP_DRAFT.md
  - scripts/sheets/sync_daily_session.py
  - scripts/e2e/daily_session_journal.py
  - tests/e2e/test_sync_daily_session.py
  - requirements.txt
  - registry/modules_registry.yaml
  - registry/wrappers_registry.yaml
  - registry/machines_registry.yaml
  - modules/data_center/registry/consumers.json
---

# GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01

## Objet

Compléter l’inventaire repo-first des surfaces Google Sheets / CSV / table-like (registries, dashboards, logs, fixtures) afin d’éviter les doublons et de verrouiller le futur schéma global.

## Contraintes

```text
- doc-first, repo-first
- aucun changement applicatif
- aucune écriture Google Sheets
- aucun collector live
- aucun appel API externe
- pas de secrets (IDs, credentials, URLs sensibles)
- ne pas modifier les index globaux
```

## 6_FINAL_TARGET

- Inventaire complet, classé par surface et par PF, distinguant read vs write.
- `PRODUCER_CONSUMER_MAP` enrichie (owners probables + liens).
- Gaps listés : ce qui manque pour figer le schéma global (nomenclature tabs, contrats colonnes, fixtures CSV, validation).

## BUNDLE_TARGET — REPO_FIRST_SHEETS_CSV_TABLE_INVENTORY_V1

- [ ] Inventaire Google Sheets (scripts/tests/docs/setup/env vars) consolidé
- [ ] Inventaire CSV (writes/reads) consolidé
- [ ] Inventaire “table registries” (yaml/json/csv) consolidé
- [ ] Surfaces classées par PF / owners probables
- [ ] Gaps et Next GO proposés (sans ouvrir de schéma final tant que l’inventaire n’est pas complet)

