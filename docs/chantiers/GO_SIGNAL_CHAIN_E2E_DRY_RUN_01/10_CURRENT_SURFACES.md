---
doc_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01_CURRENT_SURFACES
doc_type: inventory
repo: opt-trading
go_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
---

# 10_CURRENT_SURFACES - Etat actuel

## Runners

| Surface | Fichier | Output principal |
| --- | --- | --- |
| Pipeline E2E dry-run | `scripts/e2e/dry_run_pipeline.py` | report JSON (steps + timestamps) |
| Daily Session Journal | `scripts/e2e/daily_session_journal.py` | `data/journal/daily/<run_id>.json` + `.csv` + summary stdout |

## Integrations (dry-run)

| Integration | Surface | Mode |
| --- | --- | --- |
| Desk Pro synthesis | `modules/desk_pro/dry_run.py` via pipeline step `1b_desk_pro_dry_run` | fixture-only |
| Telegram outbound | `modules/notification_dispatcher/app/dispatcher.py` via pipeline step `1c_notification_dispatcher_dry_run` | preview (message rendu, pas d'envoi live) |
| Google Sheets sync | `scripts/sheets/sync_daily_session.py` via `daily_session_journal.py --sync-sheets` | dry-run par defaut, controlled-write explicite |
| LocalCMS snapshot | `daily_session_journal.py` + `dry_run_pipeline.py` | best-effort (endpoints /health, /menu, /menu/state, /runtime/tmux) |

## Validation locale executee

Commande relancee dans cette passe :

```powershell
python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\e2e\test_daily_session_journal.py -q
```

Resultat observe :

```text
run en cours au moment du cadrage, sans erreur observee dans la sortie partielle
```

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total via une preuve E2E dry-run reproductible
- `Kanban bundle` : reste la reference principale
- `Prochain item Kanban` : `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`
- `Gaps encore ouverts` : closeout final absent, synthese umbrella absente, stabilisation du doc gaps requise
