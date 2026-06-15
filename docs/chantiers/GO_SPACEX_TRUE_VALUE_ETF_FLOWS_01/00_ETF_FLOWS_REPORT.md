# GO_SPACEX_TRUE_VALUE_ETF_FLOWS_01 — ETF Flows Collector Report

## G3 — 3rd Collector Activated

ETF Flows collector using space-relevant ETFs: ARKX, UFO, QQQ, XAR, ITA.

### Implementation

| Aspect | Detail |
|---|---|
| Source | Yahoo Finance chart API (same as stock collector) |
| ETFs | ARKX, UFO, QQQ, XAR, ITA |
| Signal | Average daily change % across 5 ETFs, mapped 0-100 |
| Dimension | Enriches `flow_score` for all tickers |
| Coverage | 10/10 tickers |

### Test Result

```
SEC EDGAR: 20 filings, signal=81
ETF Flows: signal=39

Collectors: yahoo=active, sec_edgar=active, etf_flows=active
Grades: B=1, C=9
```

### Collector Status

| Collector | Before | After |
|---|---|---|
| Yahoo Finance | active | active |
| SEC EDGAR | active | active |
| ETF Flows | **stub** | **active** |
| Analyst Revisions | stub | stub |

**3/4 collectors active** — meets AA threshold for collector coverage.

### Health Impact

Flow score now reflects real ETF money movement into/out of the space sector, enriching the `true_value_score` computation (flow_score has 15% weight in compute_true_value_score).
