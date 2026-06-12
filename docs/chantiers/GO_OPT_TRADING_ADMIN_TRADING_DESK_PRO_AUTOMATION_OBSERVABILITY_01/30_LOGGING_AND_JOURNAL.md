---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01_LOGGING
doc_type: logging_and_journal
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 30_LOGGING_AND_JOURNAL - Logging and Journal

## journalctl results

```text
journalctl -u desk_pro_dry_run.timer -n 80 --no-pager
-- No entries --

journalctl -u desk_pro_dry_run.service -n 120 --no-pager
-- No entries --
```

## Observation

- aucun log timer observe
- aucun log service observe
- aucun exit status runtime observe au journal
- aucune duree d'execution observee
- aucun secret affiche
- aucun indice de Telegram, webhook ou trade dans les journaux lus

## Conclusion

L'observabilite journal existe via `journalctl`, mais aucun run n'a encore produit d'entrees exploitables.

## RISKS

- À qualifier.
