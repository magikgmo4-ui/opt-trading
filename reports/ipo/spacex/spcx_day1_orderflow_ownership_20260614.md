# SPCX Day-1 Orderflow & Ownership Ledger

Generated: 2026-06-14T07:43:22.504885+00:00
Symbol: SPCX
IPO Price: $135.00
First Trade: 2026-06-12

## Market Snapshot

- Price: $160.95
- Gap vs IPO: 19.222222222222214%
- Relative Volume: 0.0

## Orderflow Analysis

### Composite Score: 70.5/100

- **liquidity**: 75/100 (ultra_tight_spread)
- **tape_flow**: 65/100 (below_vwap, 253_large_prints, massive_volume)
- **auction**: 90/100 (bullish_opening_auction, bullish_closing_auction, strong_bullish_auction_day)
- **volume_quality**: 70/100 (253_block_trades_institutional)
- **price_context**: 50/100

### Signals
- SPCX_ORDERFLOW_NEUTRAL_POSITIVE
- INSTITUTIONAL_FLOW_253_LARGE_PRINTS

## Ownership Pressure

### Pressure Score: 36.8/100

- **insider_concentration**: 25/100 (voting_power_concentrated, few_insiders)
- **lockup_overhang**: 30/100 (most_shares_locked, massive_unrealized_gains)
- **institutional_quality**: 60/100 (moderate_institutional)
- **cost_basis_overhang**: 25/100 (pre_ipo_holders_deep_in_the_money, massive_pre_ipo_position)
- **greenshoe_status**: 55/100 (large_greenshoe_still_active, greenshoe_166600000_shares)

### Signals
- OWNERSHIP_STRUCTURE_CONCERNING
- COST_BASIS_OVERHANG_PRESENT

### Warnings
- Pre-IPO holders have very low cost basis — profit-taking risk

## Data Quality Notes

- Aggressor side inferred via quote rule (trade vs bid/ask midpoint)
- Micro-trades (< $25K, < 100 shares) filtered
- Large prints > $500K tracked individually
- Ownership data from public SEC filings + press reports
- Pre-IPO cost basis marked as *estimated* unless confirmed in filing
- Individual buyer/seller identities NOT tracked (legally impossible in real-time)
