# 20_OPERATOR_COMMANDS — Commandes operateur cursor-ai

## Pre-requis

- TradingView Desktop lance avec CDP sur `127.0.0.1:9222`
- Node.js v24+
- `tradingview-mcp` installe dans `C:\Users\ghost\.claude\tools\tradingview-mcp`

## Commandes wrapper

```powershell
cd C:\Users\ghost\opt-trading\modules\tradingview_observer

# Sanity check (9 checks)
.\sanity_check.ps1

# Sanity + full JSON export (6 fichiers)
.\cmd.ps1 -Snapshot

# Bridge packet V1 dry-run (synthese, aucun transfert)
.\cmd.ps1 -Bridge

# Product sanity (12 checks)
.\product_sanity.ps1

# Full default cycle : sanity + export + bridge
.\cmd.ps1
```

## Commandes OpenClaw

```powershell
cd C:\Users\ghost\opt-trading\modules\tradingview_observer_openclaw

# Sanity via OpenClaw safe runner
.\run.ps1 sanity

# Snapshot via OpenClaw safe runner
.\run.ps1 snapshot

# Bridge packet via OpenClaw safe runner
.\run.ps1 bridge
```

## Sorties

Toutes les sorties sont dans `modules/tradingview_observer/output/` :

| Fichier | Contenu |
|---------|---------|
| `latest_status.json` | Sante CDP + chart state |
| `latest_quote.json` | OHLC courant |
| `latest_state.json` | Etudes sur le graphique |
| `latest_alert_inventory.json` | Inventaire alertes (REST API) |
| `latest_values.json` | Valeurs visibles des indicateurs |
| `latest_report.json` | Rapport combine read-only |
| `latest_bridge_packet.json` | Bridge packet V1 (synthese, dry-run) |

Note : tous les `output/latest_*.json` sont ignores par git.

## RISKS

- À qualifier.
