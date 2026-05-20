# 40 — Mobile operator access

## Objectif

Accès mobile au runtime sans déplacer le runtime sur le mobile.

```
mobile -> SSH -> tmux server-side -> OpenClaw/OpenCode/session cible
```

## Apps possibles

- Termius
- Termux + OpenSSH
- JuiceSSH
- Tailscale + SSH

## Pré-requis

- Accès SSH aux machines (clé SSH mobile protégée)
- Réseau privé ou VPN si requis
- Jamais de secret copié dans notes/clavier mobile

## Connexions

### db-layer

```bash
ssh db-layer
tmux ls
tmux attach -t openclaw-core
```

Détacher : `Ctrl+b` puis `d`

### admin-trading

```bash
ssh admin-trading
tmux ls
tmux attach -t screeners
tmux attach -t desk-pro
```

## Commandes read-only utiles

```bash
hostname
whoami
tmux ls
tmux list-windows -t openclaw-core
tail -n 80 /opt/trading/logs/tmux_health.log
cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run
```

## Hints utiles avant device reel

Depuis un poste autorise, les hints read-only deja presents dans le repo sont :

```bash
bash modules/openclaw_tmux_operator/scripts/cmd.sh attach-hint db-layer openclaw-core
bash modules/openclaw_tmux_operator/scripts/cmd.sh attach-hint admin-trading desk-pro
bash modules/openclaw_tmux_operator/scripts/cmd.sh attach-hint admin-trading screeners
```

Ces commandes aident a preparer le smoke mobile, mais ne remplacent pas la
validation sur device reel.

## Interdits mobile

- Ne pas afficher `.env`
- Ne pas lancer `git push`
- Ne pas redémarrer `trade_executor` / `kil_v1`
- Ne pas envoyer write app externe sans gate
- Ne pas exécuter de commande destructive
- Ne pas faire tourner OpenClaw localement sur mobile

## Usage recommandé

Mobile sert à :
- Vérifier état, lire logs
- Attacher/détacher tmux
- Donner instruction courte
- Confirmer ou refuser une gate
- Surveiller pendant déplacement

Mobile ne sert pas à :
- Développer longuement
- Gérer secrets
- Modifier runtime critique
- Traiter conflits Git

## Gap courant

- checklist mobile physique encore non executee sur reseau operateur
