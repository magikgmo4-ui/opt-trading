---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01_PRECHECK
doc_type: precheck
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 10_PRECHECK - Precheck

## Base verifiee

- branche creee depuis `origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01`
- commit HEAD verifie: `8369fa2`

## Fichiers lus

- `modules/desk_pro/systemd/desk_pro_dry_run.service`
- `modules/desk_pro/systemd/desk_pro_dry_run.timer`
- `modules/desk_pro/desk_pro_dry_run.sh`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01/40_INSTALLATION_RUNBOOK_DRAFT.md`
- `modules/desk_pro/dry_run.py`
- `tests/test_desk_pro_dry_run.py`

## Validations pre-install

```bash
systemd-analyze verify modules/desk_pro/systemd/desk_pro_dry_run.service modules/desk_pro/systemd/desk_pro_dry_run.timer
bash -n modules/desk_pro/desk_pro_dry_run.sh
PYTHONPATH=/opt/trading python -m pytest tests/test_signal_event_adapter.py tests/test_admin_trading_contract_compatibility_smoke.py tests/test_desk_pro_dry_run.py -q
```

## Resultat

- `systemd-analyze verify`: PASS
- `bash -n`: PASS
- `pytest`: PASS (`50 passed in 0.15s`)

## Decision

Precheck PASS, installation autorisee.

## RISKS

- À qualifier.
