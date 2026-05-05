# TradingView Observer for opt-trading

Wrapper read-only minimal pour piloter TradingView MCP depuis opt-trading.

## Prérequis

- `C:\Users\ghost\.claude\tools\tradingview-mcp` installé (PR #76 MSIX merge)
- Node.js v24+
- TradingView Desktop lancé avec CDP sur `127.0.0.1:9222`

## Quick start

```powershell
# Vérifier l'état complet
.\cmd.ps1

# Sanity check seul
.\sanity_check.ps1

# Export JSON complet
.\cmd.ps1 -Export
```

## Sorties

| Fichier | Contenu |
|---------|---------|
| `output/latest_status.json` | Santé CDP + chart state |
| `output/latest_quote.json` | OHLC courant |
| `output/latest_alert_inventory.json` | Inventaire alertes (REST API) |
| `output/latest_report.json` | Rapport combiné read-only |

## Sécurité

- **Read-only par défaut** : aucune mutation d'alerte n'est possible via ce wrapper.
- **Flag `-AllowMutation` requis** pour toute opération d'écriture (Phase 4+).
- Ne contient pas tradingview-mcp directement.
- Ne committe pas de secrets, tokens, .env.
