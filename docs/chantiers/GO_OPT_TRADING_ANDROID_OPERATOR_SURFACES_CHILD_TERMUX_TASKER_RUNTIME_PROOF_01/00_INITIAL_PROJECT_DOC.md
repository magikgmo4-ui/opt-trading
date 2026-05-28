# GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TERMUX_TASKER_RUNTIME_PROOF_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TERMUX_TASKER_RUNTIME_PROOF_01` |
| Objet | Prouver les scripts PHASE_01 sur Android réel et flotte SSH |
| Déclencheur | PHASE_01 mergé — scaffold dispo sur `sot/mainline` |
| Base | `sot/mainline` @ `f8e3f65d` (merge PR #874) |
| Branche | `go/GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TERMUX_TASKER_RUNTIME_PROOF_01` |

## 6_FINAL_TARGET

Prouver sur un appareil Android réel :

| Check | Où |
|---|---|
| ssh db-layer `echo ok` | Termux |
| ssh admin-trading `echo ok` | Termux |
| `health_probes.sh` run | Termux |
| Tasker → Termux → SSH | Termux:Tasker |
| `tmux ls` sur chaque machine | Termux |
| `tmux attach` session | Termux |
| Recovery après reboot Android | Physique |
| PASS checklist remplie | Document |

## 7_CANONICAL_STATE

- Pas de nouveau code doc large
- Pas de mutation runtime
- Scripts déjà mergés — seulement de l'exécution réelle

## PHASE_RUNTIME — Points à prouver

1. **SSH** : `ssh db-layer hostname` sans passphrase ni prompt
2. **health_probes.sh** : 7 probes PASS sur la flotte
3. **Tasker** : widget health check → `%result=0` et `%stdout` visible
4. **tmux** : `tmux ls` liste les sessions, `tmux attach` reprend
5. **Recovery** : reboot Android → tout revient en < 3 min
6. **PASS checklist** : cocher chaque item sur le vrai device

## 12_INVARIANTS

- READ-ONLY strict : pas de start/stop/restart
- Pas de nouveau script — seulement exécuter les existants
- Tout échec = documentation dans ce GO, pas de fuite vers le runtime
- Device réel obligatoire — pas de test CI simulé
