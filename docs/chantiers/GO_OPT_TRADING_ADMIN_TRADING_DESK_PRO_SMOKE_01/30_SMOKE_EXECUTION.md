---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01_EXECUTION
doc_type: execution_log
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_SMOKE_EXECUTION — Desk Pro PAPER

## Commande

```bash
cd /opt/trading && /opt/trading/venv/bin/python -m modules.desk_pro_runner.app.desk_pro_runner run
```

## Sortie

```
>>> Starting Desk Pro Orchestration...
>>> Orchestration Complete.
  -> Running journal_engine...
  -> Running portfolio_engine...
----------------------------------------
Run Complete. Summary saved to: /opt/trading/data/desk_runs/desk_run_20260504_193939/run_summary.json
Desk Pro run completed. OK: 11, Failed: 0.
```

## Resultat

| Metrique | Valeur |
| --- | --- |
| Exit code | 0 (SUCCESS) |
| Modules OK | 11 |
| Modules Failed | 0 |
| Duree | < 1 sec (mock data) |
| Mode | PAPER |

## Nouveau run

| Fichier | Contenu |
| --- | --- |
| Run ID | desk_run_20260504_193939 |
| Repertoire | /opt/trading/data/desk_runs/desk_run_20260504_193939/ |
| Fichiers | 12 JSON (11 engines + run_summary) |

## Aucun trading reel

Tous les modules ont tourne en PAPER mode avec mock data. Aucun ordre transmis.

## Note: /shared pas auto-rafraichi

La commande `run` genere les resultats dans `data/desk_runs/` mais ne met pas a jour `/shared/desk_pro/latest/`. Pour cela, utiliser:
- `desk_pro_runner run-and-show` (run + dashboard + export)
- `desk_pro_runner export-json-latest`
- `desk_pro_cmd.sh copy-latest-to-shared`
