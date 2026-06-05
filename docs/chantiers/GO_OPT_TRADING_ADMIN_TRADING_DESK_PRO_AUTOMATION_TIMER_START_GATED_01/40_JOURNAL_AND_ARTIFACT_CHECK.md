---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01_JOURNAL
doc_type: journal_and_artifact_check
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 40_JOURNAL_AND_ARTIFACT_CHECK - Journal and Artifact Check

## Timer journal

```text
Started desk_pro_dry_run.timer - Run Desk Pro dry-run every 15 minutes.
```

## Service journal summary

- service start observed: YES
- service finish observed: YES
- service exit code: `0/SUCCESS`
- output payload status: `FAIL`

## Dry-run payload observations

Le journal du service montre un payload dry-run avec:

- `mode: dry_run`
- `status: FAIL`
- `no_trade: true`
- `no_telegram: true`
- `no_webhook: true`
- `no_systemd: true`

Erreurs visibles dans le payload:

- `missing engine`
- `invalid direction: 'LONG'`
- `missing timestamp`
- `unexpected source: 'timer_trigger'`
- `unexpected event_type: 'signal'`
- `desk_snapshot missing`

## Artifact scan observation

- les scans passifs retrouvent des artefacts Desk Pro historiques locaux et partages
- aucun nouvel artefact specifique a ce run n'est identifiable avec certitude depuis les listes observees

## Safety result

- aucun secret observe
- aucun trade observe
- aucun webhook observe
- aucun Telegram observe

## RISKS

- À qualifier.
