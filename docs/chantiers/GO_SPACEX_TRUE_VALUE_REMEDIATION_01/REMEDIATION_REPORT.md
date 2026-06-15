# REMEDIATION_REPORT — GO_SPACEX_TRUE_VALUE_REMEDIATION_01

## Remediation Summary

Fixes for blockers identified in `GO_SPACEX_TRUE_VALUE_OPERATIONAL_AUDIT_01`.

---

## R1 — LocalCMS Recovery

**Blocker**: `/true-value` route returns 404.

**Root Cause**: `localcms.service` was not restarted after PR #1176 merge. The running binary uses pre-PR code from before the `/true-value` route was added to `main.py`.

**Fix**: Ops action — requires sudo on the host.

```bash
sudo systemctl restart localcms.service
curl -s http://127.0.0.1:8700/true-value/json | python3 -c "import json,sys; print(len(json.load(sys.stdin)['items']))"
# Expected: 10
```

**Status**: ⬜ Pending ops action (requires sudo).

---

## R2 — Collector Coverage

**Blocker**: Only 1/4 collectors active (Yahoo Finance). Score quality degraded.

**Fix**: Activated SEC EDGAR collector (code change in `live_collector.py`).

### Changes

| Collector | Before | After |
|---|---|---|
| Yahoo Finance | active | active |
| SEC EDGAR | **stub** | **active** |
| ETF Flows | stub | stub |
| Analyst Revisions | stub | stub |

### SEC EDGAR Details

- CIK: 1181412 (SPCX)
- Fetches: Up to 20 recent filings (S-8, 424B4, 3, 3, etc.)
- Signal: Scale 0-100 based on filing diversity + recency
- Score enrichment: Fundamental score = 60% price signal + 40% SEC signal
- Applies to SPCX only (other tickers use Yahoo only)

### Test Result

```
SEC EDGAR: 20 filings, signal=81.0
Items: 10, Sources: 10 ok / 0 err
Grades: B=1 C=9
```

**Status**: ✅ Done. 2/4 collectors active.

---

## R3 — Dataset Freshness

**Blocker**: 38% datasets dead (> 24h). Vision, performance, analysis stale.

**Root Cause**: `spacex_super_desk` and vision producers are not running. Telegram pipeline runs on cron but produces data_center views that are NOT written by our module.

**Fix**: Ops action — restart data_center producers, verify telegram pipeline writes.

```bash
# Verify telegram pipeline is producing fresh data
ls -la data/data_center/views/telegram_signals/by_symbol/XAU_USD/latest.json

# Restart spacex_super_desk producer if available
cd /home/fantome/opt-trading-clean
PYTHONPATH=. python3 modules/ipo_tracking/spacex_collect_once.py 2>/dev/null || echo "producer not available as module"
```

**Dead datasets inventory** (for reference):
- `vision_analysis/latest.json`: 272h old
- `data_center_coverage/latest.json`: 271h old
- `analysis_verdict/latest.json`: 246h old
- `telegram_performance/latest.json`: 244h old
- `spacex_super_desk/latest.json`: 1+ day
- `telegram_screener/trade_signals/*`: 9 days

**Status**: ⬜ Partial — telegram signals + market_metrics are fresh (62%). Remaining 38% need producer restarts.

---

## R4 — Re-Audit

Planned after R1-R3 completion.

---

## Collector Status After Remediation

| Collector | Status | Coverage |
|---|---|---|
| Yahoo Finance | active | 10/10 tickers |
| SEC EDGAR | active | 1/10 (SPCX only) |
| ETF Flows | stub | 0/10 |
| Analyst Revisions | stub | 0/10 |

**Target for PRODUCTION READY**: >= 3/4 collectors active.

---

## Verdict

**In Progress** — R2 complete (code). R1 and R3 require ops actions on the host. After all three are resolved, re-run `GO_SPACEX_TRUE_VALUE_OPERATIONAL_AUDIT_02`.
