---
doc_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT - GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01

## MASTER_TARGET

Ce child reste subordonne au parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01` et a son
produit final total voulu :

- runtime operateur distant
- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener
- Telegram inbound screener
- Telegram outbound notification
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## Résumé

- Inventaire repo posé pour la chaîne "signal monitoring" : webhook + workers + Desk Pro + dispatcher + Telegram outbound + Sheets daily sync.
- Les surfaces "NEXT" du bundle qui restent à ouvrir ensuite sont surtout transverses (taxonomie/routing), pas du code d'exécution live.

## Validation locale

Commande executee dans cette passe :

```powershell
python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q
```

Resultat :

```text
31 passed in 78.94s
```

## Lecture minimale

1. `10_CHAIN_SURFACE_PROOF_MAP.md`
2. `20_REUSE_MATRIX_AND_CONSTRAINTS.md`

## Commandes de vérification (local)

```powershell
python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q
```

## Next GO (bundle)

```text
GO_EVENT_TAXONOMY_01
```

## Tableau Kanban du bundle

Le tableau Kanban du bundle reste la navigation principale. Ce point de reprise
sert seulement a transmettre l'etat local du child d'inventaire dans la chaine
du produit final total.

## Prochain item Kanban exact

`GO_EVENT_TAXONOMY_01`

## Gaps encore ouverts

- absence d'enveloppe canonique transverse d'evenements
- absence de map canonique events -> destinations Telegram
- absence de parser inbound Telegram screener trades/setups
- absence de schema Google Sheets global relie a cette baseline
