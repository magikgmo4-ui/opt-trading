# gateway_openclaw

Module durable de pilotage du gateway OpenClaw via `tmux`, adapté au mode opératoire validé sur `db-layer` lorsque `systemd --user` n'est pas disponible.

## Surface
- `sanity`
- `status`
- `start`
- `logs`
- `attach`
- `stop`
- `health`
- `probe`
- `paths`

## Principe
- utilisateur cible par défaut : `openclaw`
- session `tmux` par défaut : `openclaw-gateway`
- log par défaut : `~openclaw/.openclaw/logs/gateway_foreground.log`
- backend de démarrage : `openclaw gateway run`

## Variables d'environnement
- `OPENCLAW_GATEWAY_USER` — défaut `openclaw`
- `OPENCLAW_GATEWAY_SESSION` — défaut `openclaw-gateway`
- `OPENCLAW_GATEWAY_LOG_DIR` — défaut `~openclaw/.openclaw/logs`
- `OPENCLAW_GATEWAY_LOG_FILE` — défaut `~openclaw/.openclaw/logs/gateway_foreground.log`
- `OPENCLAW_GATEWAY_TAIL_LINES` — défaut `80`

## Exemples
```bash
bash modules/gateway_openclaw/scripts/sanity.sh
bash modules/gateway_openclaw/scripts/cmd.sh status
bash modules/gateway_openclaw/scripts/cmd.sh start
bash modules/gateway_openclaw/scripts/cmd.sh logs
bash modules/gateway_openclaw/scripts/cmd.sh attach
bash modules/gateway_openclaw/scripts/cmd.sh stop
```

## Shortcuts
```bash
bash modules/gateway_openclaw/scripts/install_shortcuts.sh
menu-gateway_openclaw
cmd-gateway_openclaw start
```

## Notes d'exploitation
- `attach` ouvre la session `tmux` cible ; détacher avec `Ctrl+b` puis `d`
- `stop` tue la session `tmux` du gateway
- ce module n'essaie pas d'installer `tmux`, `node` ou `openclaw` ; `sanity` vérifie simplement les prérequis
