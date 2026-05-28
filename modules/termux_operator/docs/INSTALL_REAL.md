# TERMUX — Installation réelle sur Android

Ce document décrit l'installation complète de Termux sur un appareil Android
pour l'opérateur mobile opt-trading.

## 1. Source — F-Droid uniquement

La version Google Play de Termux n'est plus maintenue.
Utiliser exclusivement F-Droid :

```
https://f-droid.org/en/packages/com.termux/
```

Installer également :

- `Termux:Tasker` (plugin Tasker) :
  `https://f-droid.org/en/packages/com.termux.tasker/`
- `Termux:Boot` (démarrage automatique) :
  `https://f-droid.org/en/packages/com.termux.boot/`

## 2. Permissions Android

Après installation :

1. Ouvrir Termux une première fois → laisser initialiser (`~`).
2. Paramètres Android → Applications → Termux.
3. Permissions :
   - `Notifications` : **Activées** (empêche le kill background).
   - `Stockage` : **Activé** (optionnel, utile pour transferts).
4. Paramètres → Batterie → Optimisation batterie → Termux → **Ne pas optimiser**.

## 3. Bootstrap

```bash
pkg update && pkg upgrade -y
pkg install -y git
git clone https://github.com/magikgmo4-ui/opt-trading ~/opt-trading
bash ~/opt-trading/modules/termux_operator/scripts/bootstrap.sh
```

Le bootstrap :

- Installe openssh / tmux / git / jq / coreutils / nano / python
- Crée `~/.termux/tasker/` (mode 700) pour les scripts Tasker
- Crée `~/operator/` (mode 700) pour les notes locales
- Génère une clé SSH `~/.ssh/id_ed25519_termux`
- Écrit `~/.ssh/config` pour les machines de la flotte
- Ajoute les alias fleet/health/sessions dans `~/.bashrc`

## 4. Vérification post-install

```bash
ssh -V                # doit afficher version
tmux -V               # doit afficher version
ls -ld ~/.termux/tasker  # doit exister, mode 700
jq --version          # doit afficher version
```

## 5. Clé publique

En fin de bootstrap, la clé publique est affichée.
Copier cette clé et l'ajouter aux `authorized_keys` de chaque machine :

```bash
# Depuis db-layer (ou autre machine)
bash modules/termux_operator/scripts/authorize_termux_key.sh "ssh-ed25519 AAAA..."
```

## 6. Scripts Tasker (optionnel)

Si Tasker est utilisé :

```bash
bash ~/opt-trading/modules/termux_operator/scripts/install_tasker_scripts.sh
```

Installe les scripts templates dans `~/.termux/tasker/`.
Configuration détaillée dans `TASKER_INTEGRATION.md`.

## 7. Contraintes Android connues

| Contrainte | Solution |
|---|---|
| Battery optimisation tue Termux | `Paramètres → Batterie → Ne pas optimiser` |
| Background killed after reboot | Ouvrir Termux manuellement après reboot |
| Notifications désactivées → perte session | Garder notifications activées |
| Wi-Fi change → SSH déconnecté | `ServerAliveInterval 30` dans SSH config |
| Termux:Tasker non installé | Installer depuis F-Droid |

## 8. Test final

```bash
source ~/.bashrc
fleet        # état flotte
health       # santé tmux
sessions-db  # sessions db-layer
sessions-at  # sessions admin-trading
matrix       # test SSH 12/12
```
