# Android Recovery Scenarios — Termux + SSH + tmux

## Scenario 1 : Reboot Android complet

**Cause** : Mise à jour système, batterie vide, redémarrage manuel.

**Procédure** :

1. Ouvrir Termux (manuellement, le démarrage auto n'est pas fiable).
2. Attendre l'initialisation (5-10 secondes).
3. Tester SSH :
   ```bash
   ssh -o BatchMode=yes -o ConnectTimeout=10 db-layer 'echo ok'
   ```
4. Vérifier tmux :
   ```bash
   ssh db-layer 'tmux ls || true'
   ssh admin-trading 'tmux ls || true'
   ```
5. Attacher les sessions critiques :
   ```bash
   ssh db-layer -t 'tmux attach -t openclaw-core || tmux ls'
   ssh db-layer -t 'tmux attach -t fleet-status || tmux ls'
   ```
6. Lancer health check complet :
   ```bash
   bash ~/opt-trading/modules/termux_operator/scripts/health_probes.sh
   ```
7. Vérifier que `fleet` et `health` aliases fonctionnent.

**Temps de reprise estimé** : 1-3 minutes.

## Scenario 2 : Battery optimisation a tué Termux

**Cause** : Android a mis Termux en veille prolongée.

**Symptômes** :
- Impossible de SSH
- Tasker retourne `%result` non nul
- Termux ne répond plus

**Procédure** :

1. Ouvrir Termux.
2. Vérifier que le shell répond (`echo ok`).
3. Tester SSH et tmux (cf. Scenario 1).
4. Vérifier les paramètres batterie :
   ```
   Paramètres Android → Batterie → Optimisation batterie → Termux → Ne pas optimiser
   ```
5. Redémarrer le bootstrap si la config SSH a été perdue :
   ```bash
   pkg update && pkg upgrade -y
   bash ~/opt-trading/modules/termux_operator/scripts/bootstrap.sh
   ```

**Prévention** : `Ne pas optimiser` pour Termux, garder les notifications activées.

## Scenario 3 : SSH key expired / compromised

**Cause** : Rotation de clé, réinstallation, machine remplacée.

**Symptômes** :
- `Permission denied (publickey)`
- `ssh db-layer` échoue

**Procédure** :

1. Vérifier que la clé existe :
   ```bash
   ls -la ~/.ssh/id_ed25519_termux
   ```
2. Si absente, regénérer :
   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_termux -N "" -C "termux_recovery_$(date +%Y%m%d)"
   ```
3. Afficher et copier la clé publique :
   ```bash
   cat ~/.ssh/id_ed25519_termux.pub
   ```
4. Depuis db-layer, autoriser la clé :
   ```bash
   bash /opt/trading/modules/termux_operator/scripts/authorize_termux_key.sh "ssh-ed25519 AAAA..."
   ```
5. Tester :
   ```bash
   ssh db-layer 'hostname'
   ```

## Scenario 4 : tmux session perdue (machine rebootée)

**Cause** : Machine distante redémarrée, tmux sessions perdues.

**Symptômes** :
- `tmux ls` retourne "no sessions" ou "failed to connect"
- Les health checks échouent pour les sessions critiques

**Procédure** :

1. Identifier les sessions manquantes :
   ```bash
   ssh db-layer 'tmux ls || echo "no sessions"'
   ssh admin-trading 'tmux ls || echo "no sessions"'
   ```
2. Redémarrer les sessions depuis la machine distante :
   ```bash
   # Sur db-layer
   cd /opt/trading && bash scripts/tmux/fleet_start.sh
   # ou machine par machine
   tmux new-session -d -s openclaw-core
   tmux new-session -d -s fleet-status
   ```
3. Vérifier :
   ```bash
   ssh db-layer 'tmux ls'
   ```
4. Lancer health check :
   ```bash
   bash ~/opt-trading/modules/termux_operator/scripts/health_probes.sh
   ```

## Scenario 5 : Tasker profile perdu

**Cause** : Réinstallation de Tasker, wipe Android, changement d'appareil.

**Procédure** :

1. Installer Tasker + Termux:Tasker (F-Droid).
2. Effectuer le bootstrap Termux complet :
   ```bash
   bash ~/opt-trading/modules/termux_operator/scripts/bootstrap.sh
   ```
3. Créer les scripts Tasker :
   ```bash
   mkdir -p ~/.termux/tasker
   bash ~/opt-trading/modules/termux_operator/scripts/keyboard_setup.sh  # si existe
   ```
4. Recréer les profils Tasker (cf. `TASKER_INTEGRATION.md`).
5. Tester chaque profil.

## Scenario 6 : Changement réseau (Wi-Fi → 4G)

**Cause** : L'appareil change de réseau, les connexions SSH sont interrompues.

**Symptômes** :
- `Connection timed out`
- Les health checks échouent temporairement

**Procédure** :

1. Attendre 30 secondes (les `ServerAliveInterval` doivent reprendre).
2. Tester :
   ```bash
   ssh db-layer 'echo ok'
   ```
3. Si échec, vérifier la connectivité réseau :
   ```bash
   ping -c 1 192.168.0.100
   ```
4. Si les IP changent (4G vs Wi-Fi), utiliser des noms DNS ou Tailscale.
5. Relancer health check :
   ```bash
   bash ~/opt-trading/modules/termux_operator/scripts/health_probes.sh
   ```

## Quick Recovery — Carte de référence

```
Reboot Android
├── Ouvrir Termux
├── ssh db-layer 'echo ok'
├── ssh db-layer 'tmux ls || true'
├── ssh admin-trading 'tmux ls || true'
├── health_probes.sh
└── → OK

Battery kill
├── Paramètres → Batterie → Ne pas optimiser
├── Ouvrir Termux
└── health_probes.sh

SSH fail
├── Vérifier ~/.ssh/id_ed25519_termux
├── authorize_termux_key.sh
└── ssh db-layer 'hostname'

tmux perdu
├── ssh db-layer 'tmux ls'
├── ssh db-layer 'bash scripts/tmux/fleet_start.sh'
└── health_probes.sh
```
