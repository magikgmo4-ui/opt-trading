# GO_OPT_TRADING_TMUX_SESSIONS_FLEET_START_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_TMUX_SESSIONS_FLEET_START_01` |
| Objet | Script fleet_start.sh : démarrer sessions tmux monitoring + services sur db-layer et admin-trading |
| Branche | `go/GO_OPT_TRADING_TMUX_SESSIONS_FLEET_START_01` |

## Modes

| Mode | Sessions démarrées |
|---|---|
| `--monitoring` | db-layer: `fleet-status` seulement (safe, read-only) |
| `--full` | db-layer: fleet-status + openclaw-core + strict-workers + kg-repo + localcms-ui ; admin-trading: screeners + desk-pro + trading-pipeline + market-data + apps-connectors |
| `--dry-run` | Affiche les commandes sans les exécuter |

## État post-monitoring

- `fleet-status` : ✅ active sur db-layer (4 fenêtres : fleet/health/logs/status)
- Sessions critiques (openclaw-core, screeners, strict-workers) : nécessitent services actifs → `--full`
