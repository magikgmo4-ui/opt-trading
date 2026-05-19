# 30 — Plan de tests

## Niveaux

| Niveau | Description | Mode |
|---|---|---|
| 0 | Git scope — branche propre, PR #614 JSON intact | Local |
| 1 | `python3 -m unittest tests.openclaw_tmux_operator.test_health_aggregate` | Local (injection) |
| 2 | `health_aggregate.py --dry-run` — sortie JSON valide | Local |
| 3 | `cmd.sh health-aggregate --dry-run` — exit 0, JSON | Local |
| 4 | `cmd.sh session-logs openclaw-core 10` — sortie texte | Local |
| 5 | `cmd.sh openclaw-health db-layer` | Réseau prod (SSH) |
| 6 | `cmd.sh openclaw-probe db-layer` | Réseau prod (SSH) |
| 7 | `health-aggregate` réel (sans --dry-run) sur db-layer | Réseau prod |

## Critères PASS

- Niveaux 0-4 : PASS sans réseau de prod
- Niveaux 5-7 : PASS depuis db-layer uniquement (GAP-01 inchangé)
- Aucun test ne modifie de session tmux
- Aucun test n'écrit dans `/opt/trading/data/`

## Commandes CI (niveaux 0-4)

```bash
python3 -m unittest tests.openclaw_tmux_operator.test_health_aggregate -v
python3 modules/openclaw_tmux_operator/scripts/health_aggregate.py --dry-run
bash modules/openclaw_tmux_operator/scripts/cmd.sh health-aggregate --dry-run
```
