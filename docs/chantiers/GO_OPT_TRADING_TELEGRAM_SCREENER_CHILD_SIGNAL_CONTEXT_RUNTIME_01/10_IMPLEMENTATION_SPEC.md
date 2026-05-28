# Implementation Spec

## Intended Runtime Shape
Implement a lightweight reader that:
1. reads `data/data_center/views/market_metrics/latest.json`
2. validates that the payload is `market_metrics.v1`
3. returns a screener-usable context structure
4. degrades to empty/None on missing or malformed input (`silent_empty`)

## Constraints
- no external API calls
- no producer-path coupling
- keep behavior aligned with the consumer registry contract

## Open Surface Question
The current repository does not yet expose a concrete `modules/telegram_screener/` runtime package on `sot/mainline`.
This GO should either:
- create the minimal runtime consumer surface, or
- attach the reader to the actual screener runtime surface if that lands first.
