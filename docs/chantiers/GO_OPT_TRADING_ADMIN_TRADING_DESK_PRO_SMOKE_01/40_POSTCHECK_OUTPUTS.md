---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01_POSTCHECK
doc_type: postcheck_outputs
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_POSTCHECK_OUTPUTS — Apres smoke

## Services critiques

| Service | Statut |
| --- | --- |
| tv-webhook | active |
| tv-perf | active |
| vision_bot | active |
| bot_vision_step2 | active |
| ngrok-tv | active |

Aucun service perturbe.

## macro-xau.timer

**DISABLED + INACTIVE** — confirme non reactive.

## Runner status

```json
{
  "runner_status": "OK",
  "mode": "PAPER",
  "orchestrator_available": true,
  "dashboard_available": true,
  "latest_run_available": true,
  "latest_run_id": "desk_run_20260504_193939",
  "summary": "Desk Pro runner ready."
}
```

Nouveau `latest_run_id` reference le smoke.

## /shared/desk_pro/latest/

Fichiers inchanges (run ne copie pas vers /shared automatiquement). Backup securise.

## Nouveau run data

`/opt/trading/data/desk_runs/desk_run_20260504_193939/`:
- decision_engine.json
- execution_engine.json
- journal_engine.json
- liquidation_analyzer.json
- market_scanner.json
- opportunity_ranker.json
- perf_engine.json
- portfolio_engine.json
- position_engine.json
- probability_engine.json
- risk_engine.json
- run_summary.json

12 fichiers generes (11 engines + summary). OK: 11, Failed: 0.

## Historique

39 runs dans data/desk_runs/ (38 historiques + 1 smoke).

## Observation

`desk_pro_runner run` ne met pas a jour /shared. Le workflow canonique est `run-and-show` ou `copy-latest-to-shared` apres run. Ce n'est pas un bug, c'est le comportement documente.
