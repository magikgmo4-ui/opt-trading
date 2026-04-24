---
doc_id: GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01_IDE_BUNDLE_README
doc_type: ide_bundle_readme
repo: opt-trading
project: opt-trading
module: airtable_bridge
go_id: GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01
status: ready_for_review
lifecycle_stage: implementation_bundle
surface: bundles
source_kind: working_bundle
updated_at: 2026-04-24
topic_keys:
  - airtable_bridge
  - ide_bundle
  - implementation
  - revalidation_required
links:
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/08_SESSION_INDEPENDENT_REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/05_IMPLEMENTATION_SPEC.md
  - docs/desk_pro_trae_master_prompt_pack.md
  - docs/master_pack/00_current_state_and_standards.md
---

# IDE BUNDLE — GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01

## NOTE_REPRISE_REVALIDATION

Ce bundle est créé comme bundle IDE de travail pour préparer l'implémentation de `modules/airtable_bridge/`.

Il devra être revalidé plus tard avec la documentation canonique attendue dans `/bundles/`, car cette documentation de référence n'est pas disponible pour le moment dans le contexte lu.

Conséquence : ce bundle est utilisable comme support d'implémentation, mais son statut reste `ready_for_review`, pas `locked`.

## Objet

Préparer un bundle autonome pour implémenter `modules/airtable_bridge/` sans dépendre de la session ChatGPT.

## Ordre de lecture obligatoire

1. `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
2. `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/08_SESSION_INDEPENDENT_REPRISE.md`
3. `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/05_IMPLEMENTATION_SPEC.md`
4. `docs/desk_pro_trae_master_prompt_pack.md`
5. `docs/master_pack/00_current_state_and_standards.md`
6. présent bundle

## Règles d'implémentation

- Airtable doit rester optionnel.
- Le bridge doit être fail-open.
- Aucun secret dans Git.
- Pas de dépendance runtime critique à Airtable.
- Pas de tick data dans Airtable.
- Batch Airtable max : 10 records.
- Scripts requis : `sanity_check.sh`, `cmd.sh`, `menu.sh`.
- Scripts compatibles invocation par symlink via `readlink -f`.
- Tests sans réseau obligatoires.

## Module cible

```text
modules/airtable_bridge/
├── README.md
├── .env.example
├── app/
│   ├── __init__.py
│   ├── client.py
│   └── payloads.py
├── scripts/
│   ├── sanity_check.sh
│   ├── cmd.sh
│   └── menu.sh
├── tests/
│   └── test_payloads.py
└── examples/
    ├── trade_payload.json
    └── signal_payload.json
```

## Prompts inclus

- `GO_PROMPT_01_IMPLEMENT_MODULE.md`
- `GO_PROMPT_02_VALIDATE_MODULE.md`
- `GO_PROMPT_03_DOCUMENT_CLOSEOUT.md`

## Critère PASS

- Module créé sans secret.
- Sanity local PASS sans réseau.
- Mode réseau skip propre si secrets absents.
- Fail-open respecté.
- Documentation module présente.
- Closeout produit.

## Critère FAIL

- Airtable devient critique.
- Secrets écrits dans repo.
- Refactor hors périmètre.
- Absence de tests sans réseau.
- Absence de note de revalidation `/bundles/`.
