# termux_operator

Bootstrap et configuration Termux pour l'opérateur mobile opt-trading.

## Installation (une seule fois)

### 1. Installer Termux
- Source : F-Droid uniquement (pas Google Play — version obsolète)
- URL : https://f-droid.org/en/packages/com.termux/

### 2. Lancer le bootstrap
```bash
# Dans Termux sur Android
pkg install git
git clone https://github.com/magikgmo4-ui/opt-trading /data/data/com.termux/files/home/opt-trading 2>/dev/null || true
bash ~/opt-trading/modules/termux_operator/scripts/bootstrap.sh
```

Ou sans clone (copier-coller depuis Claude Code) :
```bash
curl -fsSL https://raw.githubusercontent.com/magikgmo4-ui/opt-trading/sot/mainline/modules/termux_operator/scripts/bootstrap.sh | bash
```

### 3. Autoriser la clé Termux sur la flotte
Le bootstrap affiche la clé publique à la fin. Depuis Claude Code Android ou db-layer :
```bash
bash modules/termux_operator/scripts/authorize_termux_key.sh "ssh-ed25519 AAAA... termux_YYYYMMDD"
```

## Commandes rapides (après source ~/.bashrc)

```bash
fleet         # état flotte (fleet_orchestrator dry-run)
health        # tmux sessions health
sessions-db   # tmux ls sur db-layer
sessions-at   # tmux ls sur admin-trading
matrix        # test SSH 12/12
```

## Attachement tmux

```bash
ssh db-layer -t "tmux attach -t openclaw-core"
ssh db-layer -t "tmux attach -t fleet-status"
ssh admin-trading -t "tmux attach -t desk-pro"
ssh admin-trading -t "tmux attach -t screeners"
```
Détacher : `Ctrl+b` puis `d`

## Règles

- READ_ONLY par défaut : pas de start/stop service
- Pas de `.env` affiché
- Pas de `git push` depuis mobile
- Pas de redémarrage `trade_executor` / `kil_v1`
