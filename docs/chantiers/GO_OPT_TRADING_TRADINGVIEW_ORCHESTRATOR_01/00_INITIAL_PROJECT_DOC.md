# GO_OPT_TRADING_TRADINGVIEW_ORCHESTRATOR_01

## Objectif

Construire un système durable et orchestrable via OpenClaw permettant de piloter
TradingView (alertes, charts, indicateurs, Pine Script, layouts) par prompt/commande
avec gate humain, sans jamais toucher TradingView manuellement.

## Mécanisme

```
Prompt / commande → job packet tv_job_v1 → WRITE_GATED gate → SSH cursor-ai
→ tradingview-mcp CLI (node) → TradingView Desktop (CDP:9222)
```

## Machine cible

`cursor-ai` (Windows 192.168.0.177) — TradingView Desktop + tradingview-mcp installé.

## Types d'opérations

### Lecture (pas de gate) — TV_SNAPSHOT
| Type | Description |
|------|-------------|
| `snapshot` | État complet : alertes, chart, indicateurs, quote |
| `alert.list` | Inventaire des alertes actives |
| `screenshot` | Capture du chart courant |

### Mutation (gate --gate-approved requis) — TV_WRITE_GATED
| Type | Description |
|------|-------------|
| `alert.create` | Créer une alerte (prix + message webhook) |
| `alert.delete` | Supprimer une alerte par ID |
| `alert.rotate_webhook_key` | Pivoter TV_WEBHOOK_KEY dans tous les alerts |
| `indicator.add` | Ajouter un indicateur |
| `indicator.remove` | Supprimer un indicateur |
| `indicator.set` | Modifier les inputs d'un indicateur |
| `symbol.set` | Changer le symbol affiché |
| `timeframe.set` | Changer le timeframe |
| `pine.set` | Injecter un Pine Script |
| `pine.save` | Sauvegarder le Pine Script courant |
| `layout.switch` | Changer de layout TradingView |

## Fichiers produits

| Fichier | Rôle |
|---------|------|
| `schemas/tv_job_v1.json` | JSON Schema du job packet |
| `modules/tradingview_orchestrator/app/tv_runner.py` | Runner principal (admin-trading) |
| `modules/tradingview_orchestrator/scripts/cmd.sh` | CLI entry point |
| `modules/tradingview_observer/app/job_executor.ps1` | Pattern PS1 (cursor-ai) |
| `scripts/ai/workers/runner_tv.py` | Adapter dispatcher → tv_runner |
| `scripts/ai/workers/tasks.index.json` | +TV_SNAPSHOT, +TV_WRITE_GATED |
| `scripts/ai/workers/openclaw_strict_worker_dispatcher.py` | Routing TV_* → runner_tv |

## Commandes

```bash
# Lecture (pas de gate)
tv-orchestrator snapshot
tv-orchestrator alert-list
tv-orchestrator screenshot

# Générer un job packet
tv-orchestrator new alert.create '{"price":100000,"condition":"crossing","message":{"key":"..."}}'

# Exécuter avec gate
tv-orchestrator run jobs/examples/tv_job_rotate_webhook_key.json --gate-approved

# Dry-run (voir PS1 sans exécuter)
tv-orchestrator run jobs/examples/tv_job_rotate_webhook_key.json --dry-run
```

## Workflow complet (mutation)

1. `tv-orchestrator new alert.create '...'` → job packet JSON
2. Réviser le packet (vérifier params, pas de secret en clair si possible)
3. `tv-orchestrator run <packet.json> --dry-run` → voir le PS1 généré
4. Approuver : `tv-orchestrator run <packet.json> --gate-approved`
5. Résultat dans `reports/tradingview/`

## Prérequis cursor-ai

- TradingView Desktop ouvert avec CDP actif (`tv launch` ou manuel)
- `C:\Users\ghost\.claude\tools\tradingview-mcp\src\cli\index.js` installé
- SSH depuis admin-trading vers cursor-ai fonctionnel
- `C:\Users\ghost\opt-trading\` repo présent

## Prochaine étape

Exécuter `tv-orchestrator snapshot` pour valider la connexion E2E,
puis `tv-orchestrator run jobs/examples/tv_job_rotate_webhook_key.json --gate-approved`
pour finaliser la rotation TV_WEBHOOK_KEY dans les alertes TradingView.
