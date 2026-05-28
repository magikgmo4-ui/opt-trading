# First PASS Checklist — Android Operator V1

## Pass 1 : Termux installé

- [ ] Termux installé depuis F-Droid (pas Google Play)
- [ ] Termux:Tasker installé
- [ ] `pkg update && pkg upgrade` réussi
- [ ] Bootstrap terminé sans erreur
- [ ] `~/.termux/tasker/` existe (mode 700)
- [ ] `~/operator/` existe (mode 700)

## Pass 2 : SSH fonctionnel

- [ ] `~/.ssh/id_ed25519_termux` existe (mode 600)
- [ ] `~/.ssh/id_ed25519_termux.pub` existe
- [ ] `~/.ssh/config` existe (mode 600)
- [ ] Clé publique autorisée sur **db-layer**
- [ ] Clé publique autorisée sur **admin-trading**
- [ ] Clé publique autorisée sur **fantome**
- [ ] Clé publique autorisée sur **student**
- [ ] `ssh db-layer 'hostname'` → réponse correcte
- [ ] `ssh admin-trading 'hostname'` → réponse correcte
- [ ] `ssh fantome 'hostname'` → réponse correcte
- [ ] `ssh student 'hostname'` → réponse correcte

## Pass 3 : tmux accessible

- [ ] `ssh db-layer 'tmux ls'` → sessions listées
- [ ] `ssh admin-trading 'tmux ls'` → sessions listées
- [ ] `openclaw-core` session présente sur db-layer
- [ ] `fleet-status` session présente sur db-layer
- [ ] `desk-pro` session présente sur admin-trading
- [ ] `screeners` session présente sur admin-trading

## Pass 4 : Health checks

- [ ] `bash modules/termux_operator/scripts/health_probes.sh` → OK tous les probes
- [ ] `fleet` alias → réponse de fleet orchestrator
- [ ] `health` alias → réponse de health check
- [ ] `sessions-db` alias → liste sessions db-layer
- [ ] `sessions-at` alias → liste sessions admin-trading
- [ ] `matrix` alias → test SSH 12/12

## Pass 5 : Tasker intégré

- [ ] Termux:Tasker plugin installé dans Tasker
- [ ] Au moins un profil Tasker → Termux → SSH fonctionnel
- [ ] `%result` = 0 sur health check Tasker
- [ ] `%stdout` contient la sortie du health check
- [ ] Widget health check visible sur l'écran d'accueil
- [ ] Timeout ≥ 30s sur les actions Tasker

## Pass 6 : Non-destructif

- [ ] Aucun script ou bouton ne fait de restart
- [ ] Aucun script ou bouton ne fait de git push
- [ ] Aucun script ou bouton n'affiche de `.env`
- [ ] Aucun script ou bouton ne modifie le runtime
- [ ] Tous les health checks sont READ-ONLY

## Pass 7 : Recovery

- [ ] `RECOVERY_SCENARIOS.md` accessible sur le mobile
- [ ] Procédure reboot testée mentalement
- [ ] Procédure SSH fail testée mentalement
- [ ] Procédure battery kill testée mentalement
- [ ] Quick recovery card visible

## Pass 8 : Batterie et permissions

- [ ] Optimisation batterie désactivée pour Termux
- [ ] Notifications activées pour Termux
- [ ] Termux peut tourner en arrière-plan

## Résultat

- [ ] **Tous les checks PASS** → V1 opérationnelle
- [ ] **Un check FAIL** → corriger avant de fermer le GO

Date du test : `________________`
Appareil : `________________`
Opérateur : `________________`
