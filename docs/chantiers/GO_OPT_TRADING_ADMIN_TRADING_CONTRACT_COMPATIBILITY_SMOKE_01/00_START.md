---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01_START
doc_type: start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01
parent_go: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
previous_go: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 00_START - Contract Compatibility Smoke

## GO ID

`GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01`

## Previous GO

`GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01` — verdict `PASS` @ `f458385`

## Base branch

```
origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01 @ f458385
```

## Objectif

Valider en smoke local et sans side effects runtime la compatibilité producer/consumer entre :
1. `signal_event` V1 (adapter V0→V1)
2. `visual_context` V1 (contrat documentaire)
3. `desk_snapshot` (produit par desk_bridge)
4. Desk Pro consumer/synthèse

## Invariants

- Smoke local contrôlé uniquement
- Ne pas modifier runtime/service systemd
- Ne pas déclencher webhook réel
- Ne pas envoyer Telegram
- Ne pas lire ni afficher `.env`
- Fichiers fixture/test seulement sous `tests/fixtures/` et `tests/`

## Runtime side effects attendus

`NONE`

## RISKS

- À qualifier.
