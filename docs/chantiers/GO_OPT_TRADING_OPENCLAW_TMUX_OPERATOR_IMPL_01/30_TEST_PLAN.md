# 30 — Plan de tests

## Cadre de validation

Ce GO distingue :

- preuves Python locales executables depuis ce workspace
- verifications `bash` / SSH a executer depuis un host Linux ou le reseau
  operateur

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

## Criteres de validation

- niveaux 0-2 : preuves locales possibles ici
- niveaux 3-7 : a executer sur host Linux/WSL fonctionnel ou reseau prod
- aucun test ne modifie de session tmux
- aucun test n'ecrit dans `/opt/trading/data/`

## Commandes CI (niveaux 0-4)

```bash
python3 -m unittest tests.openclaw_tmux_operator.test_health_aggregate -v
python3 modules/openclaw_tmux_operator/scripts/health_aggregate.py --dry-run
bash modules/openclaw_tmux_operator/scripts/cmd.sh health-aggregate --dry-run
```

## Notes de cette passe

- `python -m unittest tests.openclaw_tmux_operator.test_health_aggregate -v`
  est executable dans ce workspace Windows
- les commandes `bash modules/openclaw_tmux_operator/scripts/cmd.sh ...`
  restent bloquees ici tant qu'aucune distribution WSL Linux n'est installee
