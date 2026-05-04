---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01_ENTRYPOINT
doc_type: entrypoint_identification
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_SMOKE_ENTRYPOINT_AND_INPUT

## Entrypoint

| Propriete | Valeur |
| --- | --- |
| Commande | `cd /opt/trading && /opt/trading/venv/bin/python -m modules.desk_pro_runner.app.desk_pro_runner run` |
| Wrapper | `cmd-desk_pro_runner run` (meme commande via wrapper shell) |
| Mode | PAPER (confirme par status et run) |
| Pipeline | 11 modules en sequence |

## Mode PAPER

Confirme:
- `desk_pro_runner status` retourne `"mode": "PAPER"`
- Aucun ordre reel n'est transmis aux exchanges
- Les donnees sont mock/sample en PAPER mode

## Input

Desk Pro en PAPER mode utilise des donnees mock internes. Aucun input externe (screenshots, market data live) requis.

## Pipeline (desk_pro_orchestrator)

1. market_scanner
2. liquidation_analyzer
3. probability_engine
4. opportunity_ranker
5. decision_engine
6. risk_engine
7. execution_engine
8. position_engine
9. perf_engine
10. journal_engine
11. portfolio_engine

## Backup

/shared/desk_pro/latest/ sauvegarde dans:
`/shared/desk_pro/backups/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01_20260504T193920Z/latest_before/`
