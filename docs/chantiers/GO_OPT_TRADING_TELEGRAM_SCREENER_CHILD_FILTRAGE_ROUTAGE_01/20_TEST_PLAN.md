---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01_TEST_PLAN
doc_type: test_plan
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01
status: open
lifecycle_stage: implementation
surface: modules/telegram_screener
created_at: 2026-05-28
updated_at: 2026-05-28
---

# 20_TEST_PLAN — GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01

## Test categories

### Channel existence
- route_accepts_valid_signal — channel found → accepted
- route_rejects_unknown_channel — alias not in registry → rejected
- route_rejects_when_no_channels_in_registry — empty registry → rejected

### Enabled flag
- route_rejects_disabled_channel — enabled=False → rejected

### Trust tier
- route_rejects_below_min_tier — D with min_tier=C → rejected
- route_accepts_at_min_tier — C with min_tier=C → accepted
- route_accepts_above_min_tier — A with min_tier=C → accepted
- default_min_tier_is_D — min_tier defaults to D

### Parser matching
- route_rejects_parser_mismatch — TRADE expected_parsers=["news"] → rejected
- route_accepts_news_with_news_parser — NEWS expected_parsers=["news"] → accepted
- route_accepts_alpha_with_alpha_parser — ALPHA expected_parsers=["alpha"] → accepted
- route_accepts_trade_with_setup_parser — TRADE expected_parsers=["setup"] → accepted

### Category (soft)
- route_category_mismatch_logged_not_rejected — accepted with metadata warning
- route_no_category_mismatch_when_signal_has_no_category — no warning
- route_category_match_accepted — no warning when matched

### Batch
- route_batch_mixed — 2 accepted, 1 rejected
- route_batch_returns_empty_list_for_empty_input — empty input → empty output

### Multiple channels
- multiple_channels_route_to_correct_one — picks correct channel by alias

### Registry integration
- route_with_registry_loaded_from_yaml — uses real channels.yaml

## Expected test count

23 tests (22 unit + 1 integration via YAML loader)

## Running

```bash
python3 -m pytest tests/test_telegram_screener_router.py -v
```
