# GO_OPENCLAW_STATE_DIR_REPAIR_10

## Statut
- Verdict : `PASS`
- Date de verification : `2026-04-30`

## Correction de diagnostic retenue
- cause principale : gateway absent dans la session utilisateur `openclaw`
- axe principal : `runtime owner` + contexte utilisateur `openclaw` + demarrage controle du gateway
- `state_dir` : point de vigilance secondaire seulement, non traite comme cause primaire dans cette passe

## Verifications utilisateur `openclaw`
- `getent passwd openclaw` :
  - utilisateur present
  - home : `/home/openclaw`
  - shell : `/bin/bash`
- contexte `sudo -iu openclaw bash -lc` :
  - `whoami` = `openclaw`
  - `hostname` = `db-layer`
  - `pwd` = `/home/openclaw`
  - `HOME=/home/openclaw`
  - `PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin`
- binaire :
  - `command -v openclaw` = `/usr/local/bin/openclaw`
  - `openclaw --version` = `OpenClaw 2026.3.11 (29dc654)`

## Verification pre-start
- `tmux ls` : aucune session active `openclaw-gateway`
- `modules/gateway_openclaw/scripts/cmd.sh status` :
  - `SESSION_STATUS=stopped`
  - cible loopback `ws://127.0.0.1:18789`
  - gateway non joignable initialement en RPC
- lecture d aide confirmee :
  - `openclaw --help`
  - `openclaw gateway --help`
- commande repo-side confirmee :
  - `modules/gateway_openclaw/scripts/start.sh`
  - lancement effectif par `tmux new-session -d -s openclaw-gateway "openclaw gateway run >> '$LOG_FILE' 2>&1"`

## Action executee
- demarrage controle du gateway sous `openclaw` via :

```bash
sudo -iu openclaw bash -lc 'cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh start'
```

## Verification post-start
- `tmux ls` :
  - session `openclaw-gateway` presente
- `ps aux | grep -i openclaw | grep -v grep` :
  - process `openclaw`
  - process `openclaw-gateway`
- `ss -ltnp | grep 18789` :
  - listener present sur `127.0.0.1:18789`
  - listener present sur `[::1]:18789`
- `curl -fsS http://127.0.0.1:18789/ | head -40` :
  - reponse HTML `OpenClaw Control`
- `bash modules/gateway_openclaw/scripts/cmd.sh health` :
  - `OK`
- `bash modules/gateway_openclaw/scripts/cmd.sh probe` :
  - `Connect: ok`
  - `RPC: ok`
  - gateway `db-layer (192.168.0.100)`
  - app `2026.3.11`

## Limites
- aucun secret n a ete expose
- aucune modification `admin-trading`
- aucun orchestrator additionnel active
- aucune modification state dir / config / policy

## Conclusion
- le gateway `OpenClaw` est maintenant demarre sous l utilisateur `openclaw`
- la session `tmux` `openclaw-gateway` est active
- le port `18789` repond
- le `state_dir` ne doit pas etre traite comme cause primaire sur cette passe
