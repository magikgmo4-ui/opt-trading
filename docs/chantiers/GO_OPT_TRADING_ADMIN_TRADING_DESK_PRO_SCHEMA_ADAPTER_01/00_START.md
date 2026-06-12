---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01_START
doc_type: start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01
parent_go: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
previous_go: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 00_START - Desk Pro Schema Adapter

## GO ID

`GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01`

## Previous GO

`GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01` — verdict `PASS` @ `fc5f64a`

## Base branch

```
origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01 @ fc5f64a
```

## Objectif

Créer l'adapter minimal permettant à Desk Pro de consommer un `signal_event` V1 à partir du format V0 disponible actuellement, sans casser les flux existants.

## Invariants

- Patch minimal, pas de refactor global
- Ne pas casser Desk Pro existant
- Ne pas modifier runtime/service systemd
- Ne pas déclencher webhook réel
- Ne pas envoyer Telegram
- Ne pas lire ni afficher `.env`
- Tests locaux seulement, sans side effects runtime

## Runtime side effects attendus

`NONE`

## RISKS

- À qualifier.
