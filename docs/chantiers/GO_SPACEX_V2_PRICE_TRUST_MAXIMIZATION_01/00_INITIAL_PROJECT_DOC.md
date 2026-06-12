---
doc_id: GO_SPACEX_V2_PRICE_TRUST_MAXIMIZATION_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_SPACEX_V2_PRICE_TRUST_MAXIMIZATION_01
parent_go: GO_SPACEX_V2_MAX_SOURCE_MODE_PLAN_01
status: draft
created_at: 2026-06-12
---

# GO_SPACEX_V2_PRICE_TRUST_MAXIMIZATION_01

## [7_CANONICAL_STATE]

```
SPCX: $173 | price_trust: 0.26 | source_count: 1 (Yahoo only)
3 price sources inactive: nasdaq (NO_PRICE), tradingview (0 events), bot_vision (no OCR)
```

## [6_FINAL_TARGET]

```
price_trust > 0.50  when >= 2 price sources agree
source_count >= 2
```

## Source contribution map

| Source | Weight | Status | Action |
|--------|--------|--------|--------|
| yahoo_chart | 0.26 | LIVE | keep |
| nasdaq_quote | 0.32 | NO_PRICE_AVAILABLE_YET | wait for API to return price |
| tradingview_webhook | 0.26 | 0 SPCX events | create TV alert → /tv/spacex |
| bot_vision_adapter | 0.16 | no OCR price | improve price extraction from screenshots |

## Gaps

| Gap | Priority | Fix |
|-----|----------|-----|
| Nasdaq API lag | P0 | Wait or add Polygon.io fallback |
| TV webhook 0 events | P0 | Manual: create alert on TradingView.com |
| Bot Vision no price | P2 | Improve OCR or parse json_preview |

## Validation

```bash
# Check if nasdaq went live
python3 -c "
import json
with open('data/ipo/spacex/scored/latest_snapshot.json') as f:
    snap = json.load(f)
nq = (snap.get('latest_events',{}) or {}).get('nasdaq_quote',{})
print('nasdaq:', nq.get('price_status'), nq.get('regular_market_price'))
"

# Check enriched consensus
python3 -c "
import json
with open('data/ipo/spacex/enriched/latest.json') as f:
    e = json.load(f)
c = e['consensus']
print('price_trust:', c.get('price_trust'))
print('source_count:', c.get('source_count'))
print('price:', c.get('consensus_price'))
"
```
