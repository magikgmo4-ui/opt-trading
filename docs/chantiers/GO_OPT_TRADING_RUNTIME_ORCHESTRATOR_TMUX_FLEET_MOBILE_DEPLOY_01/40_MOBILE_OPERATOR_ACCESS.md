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
