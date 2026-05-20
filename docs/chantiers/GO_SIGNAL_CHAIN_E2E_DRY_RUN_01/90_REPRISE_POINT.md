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
