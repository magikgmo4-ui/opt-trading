# 10 — Cross-review existant

## PRs et modules recroisés

| Source | Pertinence |
|---|---|
| PR #618 (GO parent TMUX_FLEET) | Fournit cmd.sh v1 + README + fleet-status.sh — base de ce GO |
| PR #614 (strict-workers skeleton) | Non modifié — aucun overlap avec health_aggregate |
| `modules/runtime_health/fleet_orchestrator.py` | Modèle pour la collecte SSH multi-machine — réutilisé |
| `modules/gateway_openclaw/scripts/cmd.sh` | Interface cible pour openclaw-health/openclaw-probe |
| `scripts/tmux/health_check.py` | Modèle de style pour health_aggregate.py |
| `tests/tmux/test_health_check.py` | Modèle de style pour test_health_aggregate.py |

## Doublons évités

| Ce qui existe | Ce GO n'en crée pas un second |
|---|---|
| `fleet_orchestrator.py` — collecte SSH runtime_health | health_aggregate.py ne refait pas fleet_orchestrator, il agrège tmux + health |
| `gateway_openclaw/scripts/cmd.sh health` | openclaw-health est un wrapper, pas une réimplémentation |
| `scripts/tmux/health_check.py` | health_aggregate.py s'appuie sur health_check.py pour le local |

## Interfaces respectées

- `cmd.sh` garde toutes ses commandes existantes (fleet-status, machine-status, tmux-status, attach-hint, logs, health-all)
- Nouvelles commandes ajoutées en extension seulement
- health_aggregate.py est standalone + importable pour les tests
