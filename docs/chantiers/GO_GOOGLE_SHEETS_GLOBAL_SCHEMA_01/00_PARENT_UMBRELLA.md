---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_PARENT_UMBRELLA
doc_type: parent_umbrella
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
lifecycle_stage: umbrella
source_kind: canonical
updated_at: 2026-05-26
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/KANBAN.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/INVENTORY.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/CANONICAL_SHEETS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/PRODUCER_CONSUMER_MAP.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/fixtures/README.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/10_CURRENT_SHEETS_SURFACES.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/20_GLOBAL_SCHEMA_TARGET.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/90_REPRISE_POINT.md
---

# 00_PARENT_UMBRELLA — GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01

## 1_MASTER_TARGET

Créer un schéma global Google Sheets canonique pour opt-trading : feuilles, colonnes, types, clés, validations, règles d’écriture, règles read-only, fixtures et compatibilité avec les futurs producers/consumers.

## 3_INITIAL_NEED

Centraliser la structure Google Sheets pour éviter :

- feuilles doublées
- colonnes divergentes
- producers qui écrivent dans des formats incompatibles
- dashboards / exports / bots qui lisent des données non normalisées
- migrations manuelles non traçables

## GO_STRUCTURAL_ROLE

```text
GO_STRUCTURAL_ROLE = GO_PARENT
PARENT_TYPE = umbrella
FINAL_TARGET = Google Sheets global schema documented, validated, fixture-backed, ready for read-only consumers
```

## Contraintes

```text
- Aucun collector live dans ce parent.
- Aucun appel API externe obligatoire.
- Fixtures-first.
- Read-only d’abord.
- Aucun changement applicatif requis pour fermer le parent (doc-only OK).
- Pas de secrets.
- Pas de modification d’index globaux sauf preuve de changement de master target.
```

## Ancrage produit total

Desk Pro est le hub consumer final ; Google Sheets doit devenir un consumer transverse stable (registry + export + contrôle + journal) sans dériver en base primaire live.

## Prochain child logique

```text
GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_TEMPLATE_EXPORT_01
```

Objectif : produire un template de feuille transportable (fixtures-first), ou un plan de migration, sans rouvrir les chantiers déjà intégrés.

## Pont Data Center (établi)

Le consumer market_metrics est livré côté Google Sheets global schema, et le rattachement Data Center est implémenté :

```text
PF_GOOGLE_SHEETS_CONSUMER / google_sheets__market_reporting = implemented
```

Ce pont est hors scope du parent umbrella Google Sheets (il vit sous PF_DATA_CENTER), mais il doit être visible dans la continuité.



## Scope boundary

`	ext
GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01 = parent umbrella de schéma Google Sheets, pas chaîne produit finale.

PF_DATA_CENTER = chaîne produit / registre normalisé.
PF_DESK_PRO = hub consumer final opérateur.
PF_GOOGLE_SHEETS_CONSUMER = surface consumer / export / reporting / journal.
`


`	ext
NOTE: ce NEXT est doc/template local, pas une priorité produit centrale.
NEXT produit réel (hors scope Google Sheets) :
GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01
`
