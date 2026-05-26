---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_KANBAN
doc_type: kanban
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
source_kind: canonical
updated_at: 2026-05-26
---

# Kanban — GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01

## Scope boundary

`	ext
GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01 ne représente pas une chaîne produit finale.
Ce parent couvre uniquement la surface Google Sheets comme consumer/export/reporting/journal.

Chaîne produit normalisée (registre) : GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01 / PF_DATA_CENTER.
Hub consumer final opérateur : PF_DESK_PRO.

NEXT produit réel (hors scope Google Sheets) :
GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01
`

## BACKLOG

| Carte | Objectif | Livrable |
| --- | --- | --- |
| GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_TEMPLATE_EXPORT_01 | Préparer un template Sheets transportable | docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/GOOGLE_SHEETS_TEMPLATE_SPEC.md |
| GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MIGRATION_PLAN_01 | Préparer migration ancienne structure → schéma global | docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/MIGRATION_PLAN.md |

## READY

`	ext
Aucune carte READY : le socle V1 (fixtures + validations + writer + premier consumer) est intégré.
`

## DOING

`	ext
Aucun chantier actif dans le parent umbrella (côté doc/contrats).
`

## REVIEW

`	ext
À remplir si un nouveau bundle doc-only est produit (template export / plan de migration).
`

## DONE

`	ext
Intégré sur sot/mainline (état réel) :

- GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01 (inventaire repo + map)
- Tables canoniques V1 (matérialisé via CANONICAL_SHEETS.md)
- Contrats colonnes V1 (GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01)
- Règles de validation V1 (matérialisé via VALIDATION_RULES.md + validator.py)
- Fixtures V1 (GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01)
- API write contrôlée (GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01)
- Consumer market_metrics V1 (GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01)
- Patch source_ref consumer market_metrics (PR #825)
- Migration titres worksheets (GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01)
`

## EXTERNAL_LINKS / BRIDGES

`	ext
- PF_GOOGLE_SHEETS_CONSUMER / google_sheets__market_reporting = implemented via PF_DATA_CENTER (PR #829)
- Ce pont vit sous PF_DATA_CENTER, pas sous ce parent umbrella.
`


## BLOCKED / RISKS

| Risque | Impact | Mitigation |
| --- | ---: | --- |
| Trop de tables dès le départ | schéma lourd, peu utilisable | commencer fixtures-first + tables minimales |
| Mélange trading live / docs / dashboard | confusion ownership | séparer producers, consumers, registry |
| Google Sheets utilisé comme DB principale | dette technique | garder Sheets comme interface / export / contrôle, pas source live critique |
| Timestamps non normalisés | données inutilisables en backtest | imposer ISO UTC + source timestamp |
| Colonnes ajoutées manuellement | drift de schéma | schema_version + validation doc |
