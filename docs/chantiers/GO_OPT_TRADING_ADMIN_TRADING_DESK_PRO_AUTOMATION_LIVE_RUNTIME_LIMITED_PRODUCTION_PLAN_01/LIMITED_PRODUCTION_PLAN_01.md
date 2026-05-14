---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_PLAN_01
doc_type: limited_production_plan
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_PLAN_01
status: active
updated_at: 2026-05-13
---

# LIMITED_PRODUCTION_PLAN_01

## 1_INITIAL_NEED

After controlled pilot PASS, prepare a limited production runtime environment for Desk Pro dry-run with explicit quotas, windows, kill-switch, and audit trail.

## 4_MASTER_PROJECT_PLAN linkage

Depends on:
- dry-run/timer sequence (PR #303)
- artifact output sequence (PR #325)
- input enrichment sequence (PR #347)
- live runtime smoke plan + execution (#349, #350)
- controlled pilot plan + execution (#353, #358)

## 6_FINAL_TARGET

Define a **limited production** plan with:
- quotas (max executions, max artifacts, max duration per window)
- execution windows
- exposure limits
- kill-switch
- rollback
- audit trail
- PASS/WARN/FAIL/STOP criteria

## 7_CANONICAL_STATE

- `sot/mainline` @ `a640a1d`
- Controlled pilot PASS published
- Timer installed, enabled, active/waiting
- Tests: 84/84 PASS
- Safety flags: true throughout
- No STOP triggers

## 8_VALIDATED_PLAN

Docs-only. No execution in this GO.

## 12_INVARIANTS

- No production free
- No implicit runtime expansion
- No real order
- No secret exposure
- Plans only, execution in separate GO

## Périmètre

- Desk Pro dry-run only
- No live trade, no Telegram, no webhook
- observation: systemd timer + service + artifacts + safety flags
- Aucune interaction avec le trading réel

## Quotas

| Quota | Valeur | Action si dépassé |
| --- | --- | --- |
| Max runs per window | 96 (24h × 4/h) | STOP at 96 |
| Max artifact size | 500MB total | WARN, STOP at 600MB |
| Max consecutive WARN | 20 | WARN, STOP at 30 |
| Max FAIL per hour | 1 per hour | WARN, STOP at 3 per hour |
| Max history growth | 1000 lines/day | WARN, STOP at 1500 |

## Fenêtres d'exécution

- Continuous (timer manages its own 15min cadence)
- No additional window restriction needed
- Manual override kill-switch available at all times

## Limites d'exposition

| Limite | Valeur |
| --- | --- |
| Max runtime per manual intervention | 7 days without review |
| Max rollback recovery time | 15min |
| Kill-switch response time | immediate |
| Any suspicious log entry | Hold and review |

## Conditions d'entrée

- Preceding controlled pilot: PASS
- Tests: 84/84 PASS
- All safety flags true on entry
- No pending rollback
- No STOP triggers in last 24h

## Conditions de sortie

- STOP trigger fired
- Quota exhausted
- Manual kill-switch
- Review cycle pass

## Kill-switch

- `sudo systemctl stop desk_pro_dry_run.timer`
- `sudo systemctl disable desk_pro_dry_run.timer`

## Rollback

- `sudo systemctl disable --now desk_pro_dry_run.timer`
- `sudo rm -f /etc/systemd/system/desk_pro_dry_run.service`
- `sudo rm -f /etc/systemd/system/desk_pro_dry_run.timer`
- `sudo systemctl daemon-reload`
- `sudo systemctl reset-failed desk_pro_dry_run.service desk_pro_dry_run.timer`

## Audit trail

- `journalctl -u desk_pro_dry_run.service --no-pager` for each run
- `history.jsonl` for artifact trail
- `latest.json` for current state
- Timestamped execution reports in docs

## PASS / WARN / FAIL / STOP

| Result | Criteria |
| --- | --- |
| PASS | All quotas respected, errors=[], safety flags true |
| WARN | Expected warnings only (e.g. visual_context missing) |
| FAIL | Errors non-empty, consecutive FAILs |
| STOP | Safety flag false, quota exceeded, kill-switch activated |

## Prochain GO

After this plan merges:
`GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_EXECUTION_01`
