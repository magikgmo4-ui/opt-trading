---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_PIPELINE_WIRING_01_TEST_PLAN
doc_type: test_plan
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_PIPELINE_WIRING_01
status: open
lifecycle_stage: implementation
surface: modules/telegram_screener
created_at: 2026-05-28
updated_at: 2026-05-28
---

# 20_TEST_PLAN — GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_PIPELINE_WIRING_01

## Test categories

### Happy path (full pipeline)
- trade → claim
- news → claim
- alpha → claim

### Error handling
- unparseable text → error
- unknown channel → rejected
- disabled channel → rejected
- below min_tier → rejected
- parser mismatch → rejected

### Properties
- succeeded=true when claim present
- succeeded=false when error
- no produced/claim when rejected
- clear error messages for each failure type
- route decision available even when rejected

### Batch
- mixed results (accept + reject + accept)
- empty → empty

### Integration
- default registry from YAML
- claim has all required fields
- channel_alias preserved in claim

## Expected test count

21 tests

## Running

```bash
python3 -m pytest tests/test_telegram_screener_pipeline.py -v
```
