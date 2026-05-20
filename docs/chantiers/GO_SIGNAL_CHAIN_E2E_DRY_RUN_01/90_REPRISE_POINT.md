---
doc_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01_REPRISE_POINT
doc_type: reprise
repo: opt-trading
go_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT

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

## Run pipeline

```powershell
python scripts\e2e\dry_run_pipeline.py
```

## Run daily session journal

```powershell
python scripts\e2e\daily_session_journal.py --no-closeout
python scripts\e2e\daily_session_journal.py --no-closeout --sync-sheets
python scripts\e2e\daily_session_journal.py --no-closeout --sync-sheets --sheets-controlled-write
```

## Outputs

- `data/journal/daily/<run_id>.json`
- `data/journal/daily/<run_id>.csv`

Le report pipeline contient les previews Telegram dans:

- `steps[].step == "1c_notification_dispatcher_dry_run"`

## Validation locale

Commande executee dans cette passe :

```powershell
python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\e2e\test_daily_session_journal.py -q
```

Resultat :

```text
run en cours au moment du cadrage, sans erreur observee dans la sortie partielle
```

## Tableau Kanban du bundle

Le tableau Kanban du bundle reste la navigation principale. Ce point de reprise
sert seulement a transmettre l'etat local de la preuve E2E dry-run dans la
chaine du produit final total.

## Prochain item Kanban exact

`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

## Gaps encore ouverts

- closeout final umbrella absent
- evidence pack transverse final non compile
- controlled-write Sheets toujours hors scope de cette preuve
