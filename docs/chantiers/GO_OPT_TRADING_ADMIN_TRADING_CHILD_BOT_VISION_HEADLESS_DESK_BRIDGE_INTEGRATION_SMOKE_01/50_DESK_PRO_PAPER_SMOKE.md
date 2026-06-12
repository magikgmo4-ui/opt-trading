---
doc_id: INTEGRATION_SMOKE_01_DESK_PRO
doc_type: desk_pro_smoke
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 50_DESK_PRO_PAPER_SMOKE

## Commande

```bash
cd /opt/trading && /opt/trading/venv/bin/python -m modules.desk_pro_runner.app.desk_pro_runner run
```

## Resultat

```
Desk Pro run completed. OK: 11, Failed: 0.
Run ID: desk_run_20260504_234500
Mode: PAPER
Exit: 0
```

## Pipeline 11 modules

1. market_scanner → OK
2. liquidation_analyzer → OK
3. probability_engine → OK
4. opportunity_ranker → OK
5. decision_engine → OK
6. risk_engine → OK
7. execution_engine → OK
8. position_engine → OK
9. perf_engine → OK
10. journal_engine → OK
11. portfolio_engine → OK

## Runner status

```json
{
  "runner_status": "OK",
  "mode": "PAPER",
  "latest_run_id": "desk_run_20260504_234500",
  "summary": "Desk Pro runner ready."
}
```

## Verdict Desk Pro

**PASS** — 11/11 OK, PAPER mode confirme, aucun trading reel.
Backup latest preservee dans /shared/desk_pro/backups/.

## RISKS

- À qualifier.
