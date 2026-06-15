# GO_SPACEX_TRUE_VALUE_STABILITY_MONITORING_01 — Initial Project Doc

## 1_MASTER_TARGET

Valider la stabilite reelle du systeme sur 7 jours d'exploitation.

## 3_CURRENT_STATE

| Component | Local (laptop) | admin-trading |
|---|---|---|
| LocalCMS `/true-value` | — | 200 OK |
| Data Center | stale/dead | fresh (<15min) |
| Yahoo Finance | active | active |
| SEC EDGAR | active | active |
| Governance | 5/5 PASS | 5/5 PASS |
| Pipeline E2E | 10/10 PASS | 10/10 PASS |

## 4_MASTER_PLAN

| Phase | Metric | Weight |
|---|---|---|
| S1 | Uptime | 25% |
| S2 | Freshness | 25% |
| S3 | Score Drift | — (diagnostic) |
| S4 | Collectors | 20% |
| S5 | Alerts | 15% |
| S6 | Governance | 15% |

### Grades

```
AAA: >= 95%
AA:  >= 90%
A:   >= 80%
B:   >= 70%
C:   <  70%
```

## Tool

`modules/stock_true_value/stability_monitor.py` — collects all S1-S6 metrics every 15 minutes. Run:

```bash
python modules/stock_true_value/stability_monitor.py
```

Outputs to `outputs/stock_true_value/stability/YYYY-MM-DD_HHMM_snapshot.json`.

## 11_KEY_DECISIONS

No new features. Measurement only. No broker, no orders.

## 17_RESUME_POINT

Day 0: baseline snapshot taken.
Day 1-7: collect snapshots every 15 min.
Day 7: consolidate → 90_STABILITY_REPORT.md with final grade.
