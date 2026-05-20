---
doc_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT - GO_TELEGRAM_EVENT_ROUTING_MAP_01

## MASTER_TARGET

Ce child reste subordonne au parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01` et a son
produit final total voulu :

- runtime operateur distant
- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener
- Telegram inbound screener
- Telegram outbound notification multi-destinations
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## Résumé

- l’état actuel (dispatcher monolithique) est inventorié
- une alias map cible est définie (sans secrets)
- un routing matrix event→alias est posé

## Validation locale

Commande executee dans cette passe :

```powershell
python -m pytest modules\notification_dispatcher\tests\test_strategy_id_adapter_readonly.py tests\e2e\test_e2e_dry_run_pipeline.py tests\test_signal_event_adapter.py tests\test_desk_pro_combined_input_smoke.py -q
```

Resultat :

```text
68 passed in 79.08s
```

## Lecture minimale

1. `20_TARGET_ALIAS_MAP.md`
2. `30_ROUTING_CLASS_MATRIX.md`
3. `40_GAPS_AND_NEXT_GO.md`

## Next GO (bundle)

```text
GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01
```

## Tableau Kanban du bundle

Le tableau Kanban du bundle reste la navigation principale. Ce point de reprise
sert seulement a transmettre l'etat local du routing outbound dans la chaine du
produit final total.

## Prochain item Kanban exact

`GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01`

## Gaps encore ouverts

- alias -> env non implementes
- multi-bots et topics encore documentaires seulement
- policy dry-run/live par type et famille encore a brancher dans le dispatcher
- l'inbound Telegram reste volontairement hors de ce chantier
