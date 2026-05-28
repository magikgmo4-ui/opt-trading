# Implementation Spec

## Change
Implement two runtime consumer readers on top of already-delivered Data Center views:

1. `strategy_framework__market_context` reads `by_symbol/<SYMBOL>.json`
2. `perf_engine__replay_context` reads `history/<SYMBOL>/*.json`

## Behavior
- strategy reader is tolerant: missing/malformed -> `None`
- perf replay reader is strict: missing path or malformed payload -> error
