# 30_RISK_AND_GUARD_SUMMARY

## Guard System

| Guard | Check | Enforcement |
|-------|-------|-------------|
| runner_mode | == PAPER | env var |
| simulation_mode | == true | env var |
| trade_allowed | == false | env var |
| ledger_path | ends with ledger_paper.json | env var |
| active_engine | not aggressive | router_state.json |
| paper_adapter | registered | adapter list |

## Guard Enforcement Proof

- HTTP 409 when guards fail (Scenario C)
- HTTP 200 when guards pass (Scenario A)
- Detailed guard info in response

## Risk Controls

| Control | Paper | Production Required |
|---------|-------|---------------------|
| Position size | unlimited | documented limits |
| Stop loss | optional | mandatory |
| Max loss | none | documented |
| Kill switch | none | required |

## Residual Risks

1. Paper and live share same webhook server
2. No position size limits in paper
3. No kill switch in paper mode
4. Manual close required (no API endpoint)
