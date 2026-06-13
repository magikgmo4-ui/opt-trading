# GO_TV_JOB_SCHEMA_HARDENING_01

## Objective

Make TradingView automation jobs safe to generate and dispatch for SPCX alert
automation.

## Scope

- Enforce `params.webhook_url` for `alert.create`.
- Refuse unsupported TradingView frequency API values.
- Materialize `TV_WEBHOOK_KEY` placeholders only at runtime.
- Mask webhook keys in dry-run output.
- Generate SPCX jobs with flat webhook payloads and API-valid frequencies.
- Keep the Windows agent from silently creating alerts without webhook URL or
  with unmaterialized key placeholders.

## Acceptance

- `tv_runner.py --dry-run` accepts canonical SpaceX jobs without requiring a
  real secret.
- `alert.create` refuses legacy `webhook`, unsupported frequencies, and missing
  webhook URL.
- `spacex_tv_reconcile.py` generates jobs using `webhook_url`.
- `AlertAutomationEngine` emits jobs compatible with `TVOrchestratorAgent`.
- `spacex_wire_alert.json` declares `on_bar_close` explicitly.
