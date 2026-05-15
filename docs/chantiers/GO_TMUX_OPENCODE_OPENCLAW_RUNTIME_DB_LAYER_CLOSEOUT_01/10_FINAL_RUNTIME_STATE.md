# Etat runtime final valide

## Etat final retenu
- Owner runtime confirme : `openclaw`.
- Hote runtime confirme : `db-layer`.
- Repertoire de travail confirme sous owner runtime : `/home/openclaw`.
- Binaire confirme : `/usr/local/bin/openclaw`.
- Version confirmee : `OpenClaw 2026.3.11 (29dc654)`.

## Gateway et session
- Session `tmux` active : `openclaw-gateway`.
- Processus runtime presents :
  - `openclaw`
  - `openclaw-gateway`
- Listener loopback present sur :
  - `127.0.0.1:18789`
  - `[::1]:18789`

## Sante et acces local
- `bash modules/gateway_openclaw/scripts/cmd.sh health` : `OK`.
- `bash modules/gateway_openclaw/scripts/cmd.sh probe` :
  - `Connect: ok`
  - `RPC: ok`
  - gateway `db-layer (192.168.0.100)`
  - app `2026.3.11`
- Dashboard local joignable sur `http://127.0.0.1:18789/`.
- Reponse HTML relue : `OpenClaw Control`.

## Preuves read-only executees
- `ssh db-layer 'sudo -iu openclaw bash -lc "whoami; hostname; pwd; openclaw --version || true"'`
- `ssh db-layer 'sudo -iu openclaw bash -lc "tmux ls 2>/dev/null || true"'`
- `ssh db-layer 'sudo -iu openclaw bash -lc "ps aux | grep -i openclaw | grep -v grep || true"'`
- `ssh db-layer 'sudo -iu openclaw bash -lc "ss -ltnp 2>/dev/null | grep -E \"18789|openclaw\" || true"'`
- `ssh db-layer 'sudo -iu openclaw bash -lc "curl -fsS http://127.0.0.1:18789/ 2>/dev/null | head -40 || true"'`
- `ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh health && bash modules/gateway_openclaw/scripts/cmd.sh probe"'`

## Lecture retenue
- La cause principale du cycle precedent est consideree comme corrigee :
  - gateway absent
  - mauvais contexte utilisateur
- L'etat valide maintenant est un gateway sain sous `openclaw`, avec session `tmux` et loopback `18789` operationnels.

## Gaps restants
- Aucun besoin de requalifier `state_dir` comme cause primaire a ce stade.
- Aucun besoin d'activer un orchestrator supplementaire dans cette passe.
