---
doc_id: GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01_EXECUTION
doc_type: chantier/execution_summary
repo: opt-trading
go_id: GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01
status: pass
lifecycle_stage: e2e_smoke
updated_at: 2026-05-06
---

# 10_EXECUTION_SUMMARY — E2E Smoke

## Verdict: PASS — 12/12

| Scenario | Intent | Expected | Got |
| --- | --- | --- | --- |
| SCENARIO_01 | screener | ok | ok |
| SCENARIO_02 | analysis | ok | ok |
| SCENARIO_03 | help | ok | ok |
| SCENARIO_04 | journal | ok | ok |
| SCENARIO_05 | status | ok | ok |
| SCENARIO_06 | execute_trade | blocked | blocked |
| SCENARIO_07 | git_push | blocked | blocked |
| SCENARIO_08 | unknown | blocked | blocked |
| SCENARIO_09 | rate_limit >10/min | error | error |
| SCENARIO_10 | circuit_breaker | error | error |
| SCENARIO_11 | structured_logging | true | true |
| SCENARIO_12 | no_secrets_in_logs | true | true |

## Gap: Telegram reel

Le test simule les payloads Telegram. Pour un test E2E reel, configurer:
1. Telegram Bot Token dans `.env`
2. Webhook Telegram → Botpress webhook endpoint
3. Botpress → Adapter HTTP

## RISKS

- À qualifier.
