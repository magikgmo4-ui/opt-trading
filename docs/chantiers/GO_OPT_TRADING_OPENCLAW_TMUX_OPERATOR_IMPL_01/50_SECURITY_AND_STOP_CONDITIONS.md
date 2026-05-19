# 50 — Sécurité et stop conditions

## Règles READ_ONLY

| Règle | Détail |
|---|---|
| Pas de write session | `cmd.sh` ne lance ni n'arrête aucune session tmux |
| Pas de restart | Aucune commande start/stop/restart service |
| Pas de secret | Aucun token, mot de passe, clé dans le module |
| SSH BatchMode | `BatchMode=yes ConnectTimeout=5` — pas d'interaction, timeout court |
| Dry-run disponible | `health-aggregate --dry-run` pour CI sans SSH |

## Stop conditions

| Condition | Comportement |
|---|---|
| SSH timeout | `aggregate_machine` retourne `reachable=False`, pas d'exception |
| Log absent | `session-logs` retourne exit 1 + message >&2 |
| Machine Windows dans le map | Exclue automatiquement de `health-aggregate` |
| openclaw non disponible | `openclaw-health` affiche `openclaw health unavailable`, exit 0 |

## Périmètre interdit

- Ne pas ajouter de commande write (send-keys, new-session, kill-session)
- Ne pas appeler `scripts/ai/workers/run_task.sh`
- Ne pas modifier `tasks.index.json` / `models.registry.json`
- Ne pas déclencher de workflow CI
