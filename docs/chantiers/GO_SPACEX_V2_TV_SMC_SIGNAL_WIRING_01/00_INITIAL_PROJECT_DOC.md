---
doc_id: GO_SPACEX_V2_TV_SMC_SIGNAL_WIRING_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_SPACEX_V2_TV_SMC_SIGNAL_WIRING_01
parent_go: GO_SPACEX_V2_SOURCE_MAXIMIZATION_AUDIT_01
status: draft
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-12
links:
  - docs/chantiers/GO_SPACEX_V2_SOURCE_MAXIMIZATION_AUDIT_01/00_INITIAL_PROJECT_DOC.md
  - modules/spcx_v2/
  - webhook_server.py
---

# GO_SPACEX_V2_TV_SMC_SIGNAL_WIRING_01

## [7_CANONICAL_STATE]

TV webhook infrastructure IS ready (`/tv/spacex` endpoint at line 613). SMC structures ARE detected in enriched pipeline (BOS, FVG, CHOCH all True). The gap is integration:

1. SMC data exists but doesn't influence spcx_v2 scoring
2. TV webhook endpoint works, alert not created yet (manual step)

## [5_GO_PLAN]

### Fix 1: Wire SMC into setup_detector scores

Modify `compute_scores()` in `setup_detector.py`:
- BOS detected → +15 smart_money_score
- CHOCH detected → +15 smart_money_score
- FVG bullish without bearish → +10 smart_money_score
- Multiple SMC confirmations → boost trade_ready

### Fix 2: SMC reason_codes in paper_logger

Add SMC flags to `reason_codes`:
- `SMC_BOS` when BOS detected
- `SMC_CHOCH` when CHOCH detected
- `SMC_FVG_BULL` / `SMC_FVG_BEAR`
- `SMC_MULTI_CONFIRM` when 2+ structures agree

### Fix 3: pipeline_adapter SMC mapping (already done in previous fix)

### Fix 4: TV alert — manual step

From TradingView.com:
```
Alert: NASDAQ:SPCX
Webhook URL: http://<admin-trading>:8000/tv/spacex
Template: tradingview/spacex_alert_template_v5.json
```

## Files modified

```text
modules/spcx_v2/setup_detector.py   ← SMC→score wiring
modules/spcx_v2/pipeline_adapter.py  ← already reads smart_money fields
tests/test_spcx_v2_setup_detector.py ← add SMC scoring tests
```
