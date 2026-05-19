# Derivatives Collector

This module is responsible for collecting and normalizing derivatives market data (Open Interest, Funding Rates, Liquidations, Long/Short Ratios) from various exchanges.

## Purpose
- Provide a unified interface for derivatives metrics.
- Support multiple data sources (mock, Coinglass, Exchange APIs).
- Export data in standard formats (JSON, CSV) for downstream consumption (Risk Engine, Strategy).
- Expose an additive lifecycle compatibility runner for collector-family artifacts.

## Structure
- `app/`: Python source code.
- `config/`: Configuration templates.
- `scripts/`: Shell scripts for management and execution.

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu.
- `cmd.sh`: CLI wrapper.
- `sanity_check.sh`: Validate installation.
- `lifecycle_compat.sh`: Run the additive lifecycle compatibility runner directly.

Historical command surface through `cmd.sh`:
- `collect`
- `sample`
- `export`
- `status`

Lifecycle compatibility command surface through `cmd.sh`:
- `lifecycle`
- `lifecycle-sample`
- `lifecycle-export`
- `lifecycle-status`

## Configuration
Copy `config/env.example` to `config/.env` and adjust settings.

## Data Points
- Open Interest (USD/Coin)
- Funding Rate (Predicted/Current)
- Liquidations (Long/Short)
- Long/Short Ratio (Global/Top Traders)

## Lifecycle compatibility notes
The lifecycle compatibility runner is additive:
- legacy JSON / CSV exports remain valid downstream outputs
- compatibility artifacts are written alongside the configured `OUTPUT_DIR`
- no spot schema is reused for derivatives outputs
