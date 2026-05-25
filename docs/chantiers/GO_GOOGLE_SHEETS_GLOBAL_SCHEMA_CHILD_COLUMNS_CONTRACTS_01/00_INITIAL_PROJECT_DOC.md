---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01
parent_go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: open
lifecycle_stage: schema_contracts
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_GOOGLE_SHEETS_CONSUMER
BUNDLE_TARGET: GOOGLE_SHEETS_COLUMNS_CONTRACTS_V1
NEXT_GO: null
topic_keys:
  - opt-trading
  - google_sheets
  - schema
  - columns
  - contracts
  - fixtures
  - read_only
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/CANONICAL_SHEETS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/PRODUCER_CONSUMER_MAP.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/20_GLOBAL_SCHEMA_TARGET.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
---

# GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01

## Objet

Définir les contrats de colonnes V1 pour les tabs canoniques du schéma Google Sheets (V1), en restant doc-only et fixtures-first.

Ce child part de la liste canonique des tabs (`CANONICAL_SHEETS.md`) et matérialise, pour chaque tab, un contrat minimal de colonnes (types, nullabilité, PK candidate, invariants) afin de permettre :

- la génération de fixtures (CSV/JSONL) cohérentes
- la validation read-only (parsers/normalizers futurs) sans écrire sur Sheets
- l’alignement des surfaces déjà prouvées (daily session sync) avec les noms canoniques

## Contraintes

```text
- doc-only
- fixtures-first (aucun live)
- aucune écriture Google Sheets transverse
- aucun appel API externe
- pas de secrets (IDs, credentials, URLs sensibles)
- ne pas modifier les index globaux
```

## 6_FINAL_TARGET

- `10_COLUMNS_CONTRACTS.md` : contrats V1 tab par tab
- `20_FIXTURES_PLAN.md` : plan de fixtures (CSV/JSONL + conventions + coverage)
- `30_REMAINING_GAPS_AND_NEXT_GO.md` : gaps résiduels + next GO proposé

## BUNDLE_TARGET — GOOGLE_SHEETS_COLUMNS_CONTRACTS_V1

- [ ] Colonnes + types + nullabilité + invariants pour chaque tab canonique V1
- [ ] PK candidate explicite (même composite)
- [ ] Colonnes de timestamp au format ISO UTC (YYYY-MM-DDTHH:MM:SSZ) si pertinentes
- [ ] Convention `*_ref` pour payloads non-cellulaires (paths/ids)
- [ ] Plan de fixtures minimal et rejouable
