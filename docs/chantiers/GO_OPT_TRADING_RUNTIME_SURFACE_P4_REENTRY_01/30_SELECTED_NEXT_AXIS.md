---
go_id: GO_OPT_TRADING_RUNTIME_SURFACE_P4_REENTRY_01
doc_type: SELECTED_NEXT_AXIS
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-31
---

# 30_SELECTED_NEXT_AXIS

## Selected next axis

`PF_TELEGRAM_INGESTION` is the recommended P4 runtime/product reentry axis.

## Selected next GO

- `GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01`

## Why this is the best reentry now

1. It is upstream of the already advanced `PF_TELEGRAM_SCREENER` chain.
2. It has a clearer product/runtime payoff than additional registry or governance refinement.
3. It can unify several newly delivered child runtime surfaces under one operational parent narrative.
4. It reorients work toward a concrete inbound product path: Telegram API -> normalized message -> screener/Desk Pro/Data Center consumers.

## What this means

P4 should reopen from the Telegram inbound side, not from registry and not from another isolated runtime residue.

## Explicit non-selection

- no new registry GO
- no immediate `mimo_open_observer` follow-up
- no broad machine/governance continuation as primary next step
