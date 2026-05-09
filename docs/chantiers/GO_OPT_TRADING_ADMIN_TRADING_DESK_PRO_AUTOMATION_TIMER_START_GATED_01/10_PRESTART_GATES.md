---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01_PRESTART
doc_type: prestart_gates
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 10_PRESTART_GATES - Prestart Gates

## Commands executed

```bash
systemd-analyze verify modules/desk_pro/systemd/desk_pro_dry_run.service modules/desk_pro/systemd/desk_pro_dry_run.timer
bash -n modules/desk_pro/desk_pro_dry_run.sh
PYTHONPATH=/opt/trading python -m pytest tests/test_signal_event_adapter.py tests/test_admin_trading_contract_compatibility_smoke.py tests/test_desk_pro_dry_run.py -q
systemctl status desk_pro_dry_run.timer --no-pager || true
systemctl status desk_pro_dry_run.service --no-pager || true
systemctl list-unit-files desk_pro_dry_run.service desk_pro_dry_run.timer || true
systemctl cat desk_pro_dry_run.timer || true
systemctl cat desk_pro_dry_run.service || true
```

## Results

- `systemd-analyze verify`: PASS
- `bash -n`: PASS
- `pytest`: PASS (`50 passed in 0.16s`)
- service prestart state: `loaded`, `static`, `inactive`
- timer prestart state: `loaded`, `enabled`, `inactive`
- rollback documented: YES
- manual service start before this GO: NO

## Gate verdict

Tous les prestart gates requis etaient PASS avant `systemctl start desk_pro_dry_run.timer`.
