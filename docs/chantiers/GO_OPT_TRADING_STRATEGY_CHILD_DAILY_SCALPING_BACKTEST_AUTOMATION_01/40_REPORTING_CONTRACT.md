---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01_REPORTING_CONTRACT
doc_type: reporting_contract
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01
status: open
updated_at: 2026-05-20
---

# 40_REPORTING_CONTRACT

## Métriques obligatoires par variant

```text
trades_count
winrate
avg_win_R
avg_loss_R
expectancy_R          = winrate * avg_win_R - (1-winrate) * avg_loss_R
profit_factor         = sum(win_R) / abs(sum(loss_R))
max_drawdown_R
max_losing_streak
avg_time_in_trade_bars
false_signal_rate     = setups détectés - trades pris / setups détectés
score_7plus_winrate   = winrate sur setups score >= 7
score_lt7_winrate     = winrate sur setups score < 7
```

## Critères de promotion auto-calculés

| Critère | Seuil | Verdict si non atteint |
|---|---:|---|
| `trades_count` | >= 100 | `NEED_MORE_DATA` |
| `expectancy_R` | > 0.15 | `REWORK_RULESET` |
| `profit_factor` | > 1.25 | `REWORK_RULESET` |
| `score_7plus_winrate > score_lt7_winrate` | obligatoire | `REWORK_RULESET` |

## Verdict final auto-généré

```text
si trades_count < 100          → NEED_MORE_DATA
sinon si tous critères OK      → PROMOTE_TO_PAPER_FORWARD
sinon si expectancy < 0        → REJECT_VARIANT
sinon                          → REWORK_RULESET
```

## Format markdown verdict (30_BACKTEST_VERDICT_01.md)

```markdown
# BACKTEST_VERDICT_01

**Symbol:** XAUUSD  **Timeframe:** M5/M15  **Date:** YYYY-MM-DD

## Résultats par variant

| Variant | Trades | Winrate | Expectancy R | PF | Max DD R | Verdict |
|---|---:|---:|---:|---:|---:|---|
| ORB_ONLY | ... | ... | ... | ... | ... | ... |
...

## Variant retenu

**COMBINED_SMC_ORB_VWAP** — Expectancy: X.XXR — PF: X.XX

## Décision finale

**PROMOTE_TO_PAPER_FORWARD** / REWORK_RULESET / REJECT_VARIANT / NEED_MORE_DATA

## Prochaine étape

→ GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PAPER_FORWARD_01
```
