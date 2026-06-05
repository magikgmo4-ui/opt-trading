# 30_PHASE_3 — Wrapper opt-trading

## Objectif

Créer une couche opt-trading minimale pour lancer les lectures TradingView et exporter les résultats.

## Structure créée

```
modules/tradingview_observer/
  README.md              — documentation opérateur
  cmd.ps1                — point d'entrée (sanity + export)
  sanity_check.ps1       — vérification rapide 7 checks
  app/
    observer_runner.ps1  — core: exécute lectures MCP, exporte JSON
  output/
    .gitkeep
    latest_status.json          — santé CDP + chart state
    latest_quote.json           — OHLC courant
    latest_state.json           — état graphique (symbole, TF, études)
    latest_alert_inventory.json — inventaire alertes (REST API)
    latest_values.json          — valeurs des indicateurs visibles
    latest_report.json          — rapport combiné read-only
```

## Rôle

- Ne contient pas tradingview-mcp directement (installé hors repo dans `C:\Users\ghost\.claude\tools\tradingview-mcp`).
- Appelle le CLI Node.js tradingview-mcp via `& node <cli_path> <command> 2>$null`.
- Exporte JSON dans `output/`.
- Read-only par défaut. Mutation verrouillée sauf flag `-AllowMutation`.
- Prêt pour reprise par OpenClaw en Phase 4.

## Test live (2026-05-05)

```
[MODE] READ-ONLY

[1/6] CDP check...     OK: Chrome/140.0.7339.133
[2/6] tv status...     OK: BITGET:BTCUSDT.P 480
[3/6] tv quote...      OK: BITGET:BTCUSDT.P close=80495.1
[4/6] tv state...      OK: BITGET:BTCUSDT.P studies=7
[5/6] tv alert list... OK: 10 alerts
[6/6] tv values...     OK: 3 studies

=== Exports ===
  latest_alert_inventory.json (35.7 KB)
  latest_quote.json             (0.4 KB)
  latest_report.json           (51.7 KB)
  latest_state.json             (1.2 KB)
  latest_status.json            (0.5 KB)
  latest_values.json            (1.1 KB)
```

## Sorties attestées

| Fichier | Contenu |
|---------|---------|
| `latest_status.json` | `success: true, cdp_connected: true, chart_symbol: BITGET:BTCUSDT.P, chart_resolution: 480` |
| `latest_quote.json` | `symbol: BITGET:BTCUSDT.P, close: 80495.1` |
| `latest_state.json` | `symbol: BITGET:BTCUSDT.P, resolution: 480, studies: 7` |
| `latest_alert_inventory.json` | `alert_count: 10` (9 expired Pine + 1 test price) |
| `latest_values.json` | `study_count: 3` (MACD, EMA, RSI visibles) |
| `latest_report.json` | Rapport combiné de tous les exports |

## Critère PASS

Depuis opt-trading, une commande unique peut produire un inventaire TradingView local en lecture seule. **Atteint.**

## Résultat

**Statut** : PASS

## Notes techniques

- **Encoding** : UTF-8 sans BOM pour compatibilité PowerShell. `2>$null` pour ignorer stderr.
- **Auto-variable** : `@args` utilisé dans `Tv` function wrapper, pas `$Args` (conflit avec l'automatique).
- **Mutation lock** : Flag `-AllowMutation` ignoré en Phase 3 (aucune fonction d'écriture). Prêt pour Phase 4+.
- **Path** : `tradingview-mcp` hors repo → le wrapper ne crée pas de dépendance npm.

## RISKS

- À qualifier.
