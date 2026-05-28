# GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TERMUX_TASKER_V1_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TERMUX_TASKER_V1_01` |
| Objet | Livrer la pile Android opérateur V1 : Termux + SSH + tmux + Tasker |
| Déclencheur | Parent GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_PARENT_01 mergé (PR #626) |
| Base | `sot/mainline` @ `2facfbc2` |
| Branche | `go/GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TERMUX_TASKER_V1_01` |

## 6_FINAL_TARGET

Produit à prouver :

```
Android
→ Tasker
→ Termux
→ SSH
→ tmux
→ db-layer
```

avec :

- health checks
- recovery
- non-destructive commands
- session persistence

## 7_CANONICAL_STATE

Android reste console opérateur. Pas de runtime trading sur mobile.
tmux reste couche persistante sur les machines.
Tasker orchestre des scripts versionnés, pas des commandes critiques improvisées.

## PHASE_01 — Livrables

| # | Livrable | Fichier |
|---|---|---|
| 1 | TERMUX install doc réelle | `modules/termux_operator/docs/INSTALL_REAL.md` |
| 2 | SSH key generation guide | `modules/termux_operator/docs/SSH_KEY_GUIDE.md` |
| 3 | tmux health probes | `modules/termux_operator/scripts/health_probes.sh` |
| 4 | Tasker integration doc + scripts templates | `modules/termux_operator/docs/TASKER_INTEGRATION.md` + `scripts/tasker/*.sh` + `scripts/install_tasker_scripts.sh` |
| 5 | Android recovery scenarios | `modules/termux_operator/docs/RECOVERY_SCENARIOS.md` |
| 6 | First PASS checklist | `modules/termux_operator/docs/PASS_CHECKLIST.md` |

## 12_INVARIANTS

- Pas de secret dans les docs
- Pas de commande destructive directe depuis bouton tactile
- Pas de runtime trading sur Android
- Scripts critiques versionnés
- Sorties de health check visibles avant action de restart
- Toute action WRITE/RESTART séparée des actions READ/OBSERVE

## Construction

```
git checkout -b go/GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TERMUX_TASKER_V1_01 2facfbc2
```
