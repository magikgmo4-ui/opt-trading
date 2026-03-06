# Desk Pro Dashboard

The Desk Pro Dashboard is a lightweight aggregator and visualizer for the AI Trading Desk. It consolidates outputs from the `Derivatives Collector` and `Probability Engine` into a unified view for decision making.

## Purpose
- **Aggregation**: Merge data from multiple upstream modules (Market Data, Risk, Probability).
- **Visualization**: Provide a clean, text-based or simple HTML summary of the current market state and trade bias.
- **Reporting**: Export consolidated snapshots for logging or external consumption.

## Structure
- `app/`: Python source code (input parsing, merging, rendering).
- `config/`: Configuration templates and sample inputs.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for viewing the dashboard.
- `cmd.sh`: CLI wrapper for rendering and exporting.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Render dashboard from specific input
./scripts/cmd.sh render --input config/sample_dashboard_input.json

# Export to JSON
./scripts/cmd.sh export-json --output data/dashboard/latest.json

# Export to HTML
./scripts/cmd.sh export-html --output data/dashboard/latest.html
```

## Input Data
The dashboard expects JSON inputs that can come from:
1.  **Probability Engine**: `{ "probability_long": ..., "confidence": ... }`
2.  **Derivatives Collector**: `{ "open_interest": ..., "funding_rate": ... }`

It can merge these if provided separately or read a pre-consolidated file.

## Future Role
This dashboard will evolve into the primary "Heads Up Display" (HUD) for the trading desk, potentially integrating real-time WebSocket feeds and alerting.
