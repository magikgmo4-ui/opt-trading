---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_KANBAN
doc_type: kanban
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
source_kind: canonical
updated_at: 2026-05-24
---

# Kanban — GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01

## BACKLOG

| Carte | Objectif | Livrable |
| --- | --- | --- |
| GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01 | Inventorier toutes les feuilles / usages existants ou prévus | docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/INVENTORY.md |
| GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_CANONICAL_TABLES_01 | Définir la liste des feuilles canoniques | docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/CANONICAL_SHEETS_DRAFT.md |
| GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01 | Définir colonnes, types, clés, timestamps | docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/SCHEMA_CONTRACTS.md |
| GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_PRODUCER_CONSUMER_MAP_01 | Mapper producers / consumers par feuille | docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/PRODUCER_CONSUMER_MAP_DRAFT.md |
| GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01 | Créer fixtures-first sans API live | docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/fixtures/ |
| GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_VALIDATION_RULES_01 | Définir règles anti-doublon / qualité / nulls | docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/VALIDATION_RULES.md |
| GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_TEMPLATE_EXPORT_01 | Préparer un template Sheets transportable | docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/GOOGLE_SHEETS_TEMPLATE_SPEC.md |
| GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MIGRATION_PLAN_01 | Préparer migration ancienne structure → schéma global | docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/MIGRATION_PLAN.md |

## READY

### GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01

Objectif : lire l’existant et produire l’inventaire des usages Google Sheets / CSV / exports tableurs.

Scope :

```text
docs/
scripts/
apps/
data/
fixtures/
jobs/
dashboards/
telegram/
modules/
tools/
```

DoD :

```text
- Toutes les références Sheets / CSV / table-like trouvées.
- Surfaces classées par product final.
- Doublons identifiés.
- Owners probables listés.
- Aucun changement de code applicatif.
```

### GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_CANONICAL_TABLES_01

Objectif : définir les feuilles globales minimales.

DoD :

```text
- Chaque feuille a une finalité claire.
- Pas de table orpheline.
- Chaque table est rattachée à un producer ou consumer.
- Aucun champ live obligatoire.
```

## DOING

```text
Aucun child actif tant que l’inventaire repo n’a pas été matérialisé.
```

## REVIEW

```text
À remplir après production du premier bundle (INVENTORY + CANONICAL_SHEETS_DRAFT + MAP_DRAFT).
```

## DONE

```text
Aucun child fermé pour l’instant.
```

## BLOCKED / RISKS

| Risque | Impact | Mitigation |
| --- | ---: | --- |
| Trop de tables dès le départ | schéma lourd, peu utilisable | commencer fixtures-first + tables minimales |
| Mélange trading live / docs / dashboard | confusion ownership | séparer producers, consumers, registry |
| Google Sheets utilisé comme DB principale | dette technique | garder Sheets comme interface / export / contrôle, pas source live critique |
| Timestamps non normalisés | données inutilisables en backtest | imposer ISO UTC + source timestamp |
| Colonnes ajoutées manuellement | drift de schéma | schema_version + validation doc |

