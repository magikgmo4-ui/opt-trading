# gateway_openclaw

Module durable de pilotage du gateway OpenClaw.

Mode opérationnel courant: `openclaw-gateway.service` sur `fantome`.
Les scripts `tmux` restent disponibles pour diagnostic manuel ou reprise legacy sur `db-layer`.

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
- service systemd courant : `openclaw-gateway.service`
- hôte courant : `fantome`
- session `tmux` par défaut : `openclaw-gateway`
- log par défaut : `~openclaw/.openclaw/logs/gateway_foreground.log`
- backend de démarrage : `openclaw gateway run`

## Exécution
Exploitation courante :
```bash
sudo systemctl status openclaw-gateway.service
sudo systemctl restart openclaw-gateway.service
sudo -iu openclaw openclaw gateway health
sudo -iu openclaw openclaw gateway probe --timeout 30000
```

Exécution legacy/manual :
Le module est conçu pour être exécuté **sous l'utilisateur `openclaw`**.

Exemple :
```bash
sudo -iu openclaw
cd /opt/trading
bash modules/gateway_openclaw/scripts/cmd.sh status
```

## Variables d'environnement
- `OPENCLAW_GATEWAY_USER` — défaut `openclaw`
- `OPENCLAW_GATEWAY_SESSION` — défaut `openclaw-gateway`
- `OPENCLAW_GATEWAY_LOG_DIR` — défaut `~openclaw/.openclaw/logs`
- `OPENCLAW_GATEWAY_LOG_FILE` — défaut `~openclaw/.openclaw/logs/gateway_foreground.log`
- `OPENCLAW_GATEWAY_TAIL_LINES` — défaut `80`

## Exemples
```bash
sudo -iu openclaw
cd /opt/trading
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
