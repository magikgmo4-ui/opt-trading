# gateway_openclaw

Pilotage du gateway OpenClaw via `tmux`, adapte au mode operatoire retenu quand `systemd --user` n'est pas disponible.

## Role
- demarrer, stopper et attacher la session gateway
- lire les logs foreground
- verifier `health` et `probe`
- standardiser le pilotage sous l'utilisateur `openclaw`

## Contenu
- `app/gateway_env.sh` : variables communes (user, home, session, log file)
- `scripts/cmd.sh`, `start.sh`, `stop.sh`, `attach.sh`, `logs.sh`, `sanity.sh`, `install_shortcuts.sh`
- `docs/README.md`

## Runtime
- utilisateur cible par defaut : `openclaw`
- session `tmux` : `openclaw-gateway`
- log foreground : `~openclaw/.openclaw/logs/gateway_foreground.log`

## Statut
- actif
- composant runtime explicite de la suite OpenClaw

## Notes de consolidation
- ce module reste distinct de `doctor_openclaw`
- `doctor_openclaw` diagnostique; `gateway_openclaw` pilote le runtime du gateway
