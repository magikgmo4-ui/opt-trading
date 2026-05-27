---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 00_INITIAL_PROJECT_DOC — GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01

## GO_STRUCTURAL_ROLE

```text
GO_CHILD_ATTACHED_TO_PARENT
```

Parent :

```text
GO_DESKPRO_INPUT_EXPANSION_01
```

Parent umbrella (contexte) :

```text
GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01
```

## Master target (rappel)

```text
Desk Pro doit devenir le hub consumer capable d’unifier les inputs :
TradingView/webhook, signal_event, desk_snapshot, visual_context,
vision/headless, Telegram inbound claims, market metrics,
Sheets, Perf Engine et replay/paper.
```

## État établi (repo-first)

Inputs déjà prouvés / présents :

- `signal_event` : adapter read-only V0→V1 dans `modules/desk_pro/signal_event_adapter.py`
- `desk_snapshot` : contrat minimal utilisé en dry-run (`{symbol, tf, snapshot_ts, path, ...}`)
- `visual_context` : payload V1 minimal accepté en dry-run

Pattern existant validé :

- wrappers read-only = `normalize_*` + `validate_*` + `read_*`
- tests fixtures-first déjà présents sous `tests/fixtures/...`

## Besoin initial

Matérialiser un child “wrappers read-only / fixtures-first” sans ouvrir de runtime live.

## Objectif

Créer doc + code minimal pour :

- stabiliser des wrappers read-only pour :
  - `signal_event.v1`
  - `desk_snapshot.v1`
  - `visual_context.v1`
- préparer (contrats + fixtures) les classes encore contractuelles :
  - `vision_analysis.v1`
  - `market_metrics.v1`
  - `telegram_claim.v1`

## Contraintes

- pas de runtime live
- pas de Telegram live
- pas d’écriture Google Sheets
- pas de secrets
- tests fixtures-first uniquement
- ne pas modifier les index globaux sauf nécessité prouvée
- ne pas fermer `GO_DESKPRO_INPUT_EXPANSION_01`
- ne pas fermer le parent umbrella

## Livrables

- docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01/
  - `00_INITIAL_PROJECT_DOC.md`
  - `10_WRAPPER_CONTRACTS.md`
  - `20_FIXTURE_PLAN.md`
  - `30_VALIDATION_PLAN.md`
  - `90_REPRISE.md`
- wrappers read-only minimaux seulement si une surface naturelle existe déjà
- tests unitaires fixtures-first sans side effects

