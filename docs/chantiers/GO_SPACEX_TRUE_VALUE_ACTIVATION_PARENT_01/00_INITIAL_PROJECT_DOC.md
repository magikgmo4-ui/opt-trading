# GO_SPACEX_TRUE_VALUE_ACTIVATION_PARENT_01 — Initial Project Doc

## 1_MASTER_TARGET

Passer de `IMPLEMENTED/TESTED/AUDITED/DRAFT_ONLY` à `PRODUCING/CONSUMING/VISIBLE/MEASURED` sans jamais activer broker/order execution.

## 3_CURRENT_STATE

```
Data Center producer runtime      OFF
LocalCMS public route            OFF
Telegram alerts                  OFF
Google Sheets writes             OFF
Live collectors                  OFF
Broker integration               OFF
Order execution                  OFF
```

All contracts are `draft_only`.

## 4_MASTER_PROJECT_PLAN

| Phase | GO | Description |
|---|---|---|
| 0 | `PRE_ACTIVATION_AUDIT_01` | Schema/fixture/CLI/test/contract validation |
| 1 | `DRYRUN_OUTPUTS_01` | Fixture-only output generation |
| 2 | `DATACENTER_PRODUCER_01` | Register producer in runtime |
| 3 | `LOCALCMS_01` | `/true-value` cards, localhost only |
| 4 | `TELEGRAM_01` | Passive read-only alerts |
| 5 | `SHEETS_01` | Google Sheets export, 1x/day |
| 6 | `LIVE_COLLECTORS_01` | Gradual collector activation |
| 7 | `PRODUCTION_RUNTIME_01` | Daily scores + ranking + reports |
| 8 | `GOVERNANCE_01` | Continuous validation |

## 11_KEY_DECISIONS

- No order execution
- No broker connection
- No trading automation
- No execution webhooks
- Decision Support Only

## 12_INVARIANTS

Never activate without a dedicated GO: broker integration, order execution, auto trading, position management, risk engine execution.

## 17_RESUME_POINT

Order: 1→2→3→4→5→6→7→8. Lowest risk sequence, coherent with current `sot/mainline` state.
