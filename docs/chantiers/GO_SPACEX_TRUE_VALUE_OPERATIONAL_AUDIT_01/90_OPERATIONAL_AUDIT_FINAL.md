# 90_OPERATIONAL_AUDIT_FINAL — GO_SPACEX_TRUE_VALUE_OPERATIONAL_AUDIT_01

## Executive Summary

Photographie runtime réelle du système `stock_true_value` au `2026-06-15T12:00Z`.

**Verdict: NOT PRODUCTION READY** — 3 blocages critiques.

---

## A — Runtime Inventory

### Systemd Services

| Service | Status | Source |
|---|---|---|
| `localcms.service` | **running** | systemd |
| `openclaw-gateway.service` | **running** | systemd |
| `shared-sshfs.service` | **running** | systemd |

### Cron Jobs

| Job | Schedule | Source |
|---|---|---|
| `telegram_production.sh` | */30 min | crontab |
| `pipeline_cycle.sh` | */30 min | crontab |

### TMUX Sessions

| Status | Note |
|---|---|
| **not running** | Aucun tmux actif |

### Registry Producers

| Producer | Status | Last Write | Age |
|---|---|---|---|
| `coinglass.v1` | stale | 2026-06-11 | 4 days |
| `spacex_super_desk_v5` | ok | 2026-06-12 | 3 days |
| `spacex_true_value` | **inactive** | null | — |

### Routes

| Route | HTTP | Status |
|---|---|---|
| `/health` | 200 | OK |
| `/menu` | 200 | OK |
| `/runtime/tmux` | 200 | OK |
| `/journal/daily` | 200 | OK |
| `/metrics/daily` | 200 | OK |
| `/true-value` | **404** | ❌ |
| `/true-value/json` | **404** | ❌ |
| `/spacex` | **404** | ❌ |
| `/credentials/json` | **404** | ❌ |

---

## B — Data Freshness

### Fresh (< 30 min)

| Dataset | Age |
|---|---|
| `market_metrics/latest.json` | 7m |
| `telegram_context/latest.json` | 7m |
| `telegram_signals/*/latest.json` (~50 channels) | 7m |
| `telegram_screener/signals/latest.json` | 7m |
| `telegram_screener/channel_stats/latest.json` | 7m |
| `telegram_screener/trade_signals/*/latest.json` (~44 channels) | 7m |
| `outputs/stock_true_value/latest/scores.json` | 1m |

### Acceptable (< 6h)

(none)

### Stale (< 24h)

(none)

### Dead (> 24h)

| Dataset | Age |
|---|---|
| `telegram_screener/trade_signals/*/latest.json` (~50 signals) | 9 days |
| `telegram_performance/latest.json` | 10 days |
| `analysis_verdict/latest.json` | 10 days |
| `data_center_coverage/latest.json` | 11 days |
| `vision_analysis/latest.json` | 11 days |
| `spacex_super_desk/latest.json` | 1 day |

### Freshness Score

- Fresh: 100+ datasets (telegram signals/market_metrics)
- Dead: 60+ datasets (vision, analysis, legacy signals)
- **Coverage**: ~62% fresh, ~38% dead

---

## C — Pipeline Validation

### End-to-End Test

```
Step 1: Collector (Yahoo Finance) → 10/10 tickers fetched
Step 2: Scoring Engine → 10 scores computed
Step 3: Report → daily report + ranking generated
Step 4: Output → scores.json + summary.md written
```

| Check | Result |
|---|---|
| Collector fetch success | 10/10 (Yahoo only) |
| Score computation | 10/10 |
| Output generation | OK |
| Schema validation | PASS |

### Collector Status

| Collector | Status | Live? |
|---|---|---|
| Yahoo Finance | active | ✅ |
| SEC EDGAR | stub | ❌ |
| ETF Flows | stub | ❌ |
| Analyst Revisions | stub | ❌ |

**Score Quality**: With only 1/4 collectors active, most tickers get grade C. True scores require all sources.

---

## D — Consumer Validation

### LocalCMS

| Route | Expected | Actual | Status |
|---|---|---|---|
| `/true-value` | 200 (HTML) | **404** | ❌ |
| `/true-value/json` | 200 (JSON) | **404** | ❌ |
| `/spacex` | 200 (HTML) | **404** | ❌ |

**Root Cause**: `localcms.service` was NOT restarted after PR #1176 merge. The running binary uses pre-PR code. Fix: `sudo systemctl restart localcms.service`.

### Telegram

- Dry-run: 10 alerts generated
- All 10 tickers trigger "HIGH CONFIDENCE" (>80%)
- Forbidden terms: 0 violations
- Real send: NOT tested (requires TELEGRAM_BOT_TOKEN + --telegram flag)

### Google Sheets

- Dry-run: validation PASS, 3 rows schema-valid
- Real write: NOT tested (requires GOOGLE_SHEETS_SYNC_SHEET_ID + ALLOW_GOOGLE_SHEETS_API_WRITE=1)

---

## E — Governance Validation

| Check | Result | Detail |
|---|---|---|
| R1: Schema Drift | PASS | scores.json structure valid |
| R2: Source Drift | PASS | 1 active collector |
| R3: Collector Health | PASS | Yahoo API reachable |
| R4: Confidence | PASS | 0 low-confidence items |
| R5: Score Stability | PASS | < 2 days history |

Note: R4 and R5 pass trivially — R4 shows 100% confidence because only 1 source feeds minimal data. R5 needs more history (>2 days) for real comparison.

---

## F — Operational Dashboard

Not yet deployed. Spec exists in Phase 3 (`/true-value` route). Requires LocalCMS restart.

---

## Operational Health Score

```yaml
operational_health: 61%
  freshness: 62% (25% weight) → 15.5
  pipeline: 100% (25% weight) → 25.0
  governance: 100% (20% weight) → 20.0
  consumers: 0% (15% weight) → 0.0
  collectors: 25% (15% weight) → 3.75
```

**Grade: C**

---

## Critical Blockers

| # | Issue | Impact | Fix |
|---|---|---|---|
| 1 | LocalCMS not restarted after PR #1176 | `/true-value` route 404 | `sudo systemctl restart localcms.service` |
| 2 | Only 1/4 collectors active (Yahoo) | Score quality low (all C except SPCX) | Activate SEC, ETF, Analyst collectors |
| 3 | 38% datasets dead (> 24h) | Vision, performance, analysis stale | Restart vision/data_center producers |

---

## Next Actions

1. **Immediate**: Restart LocalCMS → verify `/true-value` route
2. **Short-term**: Activate SEC EDGAR collector (already has `sec_edgar.py`)
3. **Short-term**: Restart data_center producers (vision, spacex_super_desk)
4. **Medium-term**: Implement ETF flows + Analyst revisions collectors
5. **Medium-term**: Deploy operational dashboard `/desk/true-value/ops`

---

## Verdict

**NOT PRODUCTION READY** — Grade C (61%).

The scoring engine and pipeline work correctly end-to-end. However:
1. Consumer routes are not available (LocalCMS needs restart)
2. Score quality is degraded (single collector = minimal data)
3. Broad dataset decay across the system (38% dead)

Recommended: fix blockers 1 and 3 first, then re-audit.
