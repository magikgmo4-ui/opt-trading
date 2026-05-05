# TradingView Observer for opt-trading

Wrapper read-only minimal pour piloter TradingView MCP depuis opt-trading.

## Pre-requis

- `C:\Users\ghost\.claude\tools\tradingview-mcp` installe (PR #76 MSIX merge)
- Node.js v24+
- TradingView Desktop lance avec CDP sur `127.0.0.1:9222`

## Quick start

```powershell
# Full cycle : sanity + export JSON + bridge packet
.\cmd.ps1

# Sanity check seul
.\cmd.ps1 -Sanity

# Export JSON complet (sanity + snapshot)
.\cmd.ps1 -Snapshot

# Bridge packet dry-run (pas de transfert)
.\cmd.ps1 -Bridge

# Product sanity (tous les checks)
.\product_sanity.ps1
```

## Modes

| Mode | Commande | Description |
|------|----------|-------------|
| sanity | `.\cmd.ps1 -Sanity` | Check infrastructure + TV |
| snapshot | `.\cmd.ps1 -Snapshot` | Sanity + export 6 fichiers JSON |
| bridge | `.\cmd.ps1 -Bridge` | Export bridge packet V1 (dry-run) |
| product | `.\product_sanity.ps1` | Sanity produit global (12 checks) |

## Sorties

| Fichier | Contenu |
|---------|---------|
| `output/latest_status.json` | Sante CDP + chart state |
| `output/latest_quote.json` | OHLC courant |
| `output/latest_state.json` | Etudes sur le graphique |
| `output/latest_alert_inventory.json` | Inventaire alertes (REST API) |
| `output/latest_values.json` | Valeurs visibles des indicateurs |
| `output/latest_report.json` | Rapport combine read-only |
| `output/latest_bridge_packet.json` | Bridge packet V1 (synthèse) |

## Securite

- **Read-only par defaut** : aucune mutation d'alerte n'est possible via ce wrapper.
- **Flag `-AllowMutation` requis** pour toute operation d'ecriture.
- Ne contient pas tradingview-mcp directement.
- Ne committe pas de secrets, tokens, .env.
- Tous les fichiers `output/latest_*.json` sont ignores par git.
