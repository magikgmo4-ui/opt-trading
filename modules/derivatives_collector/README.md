# Derivatives Collector

This module is responsible for collecting and normalizing derivatives market data (Open Interest, Funding Rates, Liquidations, Long/Short Ratios) from various exchanges.

## Purpose
- Provide a unified interface for derivatives metrics.
- Support multiple data sources (mock, Coinglass, Exchange APIs).
- Export data in standard formats (JSON, CSV) for downstream consumption (Risk Engine, Strategy).

## Structure
- `app/`: Python source code.
- `config/`: Configuration templates.
- `scripts/`: Shell scripts for management and execution.

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu.
- `cmd.sh`: CLI wrapper.
- `sanity_check.sh`: Validate installation.

## Configuration
Copy `config/example.env` to `config/.env` and adjust settings.

## Data Points
- Open Interest (USD/Coin)
- Funding Rate (Predicted/Current)
- Liquidations (Long/Short)
- Long/Short Ratio (Global/Top Traders)
