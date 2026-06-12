# Gateway et port 18789

## Etat verifie
- Aucun listener `18789` n'a ete observe pendant ce GO.
- Aucun processus `openclaw` n'a ete observe via `ps`.
- La session `tmux` attendue `openclaw-gateway` n'apparait pas active au moment du controle.
- Le module `gateway_openclaw` retourne `SESSION_STATUS=stopped`.
- La cible loopback attendue reste `ws://127.0.0.1:18789`.
- Le probe runtime renvoie `ECONNREFUSED 127.0.0.1:18789`.

## Preuves read-only executees
- `ssh db-layer 'ss -ltnp 2>/dev/null | grep -E "18789|openclaw" || true'`
- `ssh db-layer 'ps aux | grep -i openclaw | grep -v grep || true'`
- `ssh db-layer 'ls -la /tmp/openclaw-* 2>/dev/null || true'`
- `ssh db-layer 'find /tmp -maxdepth 2 -iname "openclaw*.log" -type f 2>/dev/null | tail -20 || true'`
- `ssh db-layer 'tail -120 /tmp/openclaw-*/openclaw-*.log 2>/dev/null || true'`
- `ssh db-layer "sudo -iu openclaw bash -lc 'cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh status'"`
- `ssh db-layer "sudo -iu openclaw bash -lc 'tmux ls 2>/dev/null || true'"`
- `ssh db-layer "sudo -iu openclaw bash -lc 'tail -120 ~/.openclaw/logs/gateway_foreground.log 2>/dev/null || true'"`

## Interpretation prudente
- L'etat live au `2026-04-30` est un gateway local arrete, pas un simple doute documentaire.
- L'absence simultanee de process `openclaw`, de port `18789` et de session `tmux` va dans le meme sens.
- Le dossier `/tmp/openclaw-*` existe encore, mais sans log temporaire exploitable courant dans cette passe.
- Le fichier `~/.openclaw/logs/gateway_foreground.log` garde toutefois une preuve historique de demarrages valides :
  - `2026-04-03`
  - `2026-04-04`
  - `2026-04-09`
  - `2026-04-22`
- Les dernieres lignes relues montrent qu'au `2026-04-22`, le gateway montait bien le canvas local et ecoutait sur `ws://127.0.0.1:18789`, puis plus aucune preuve de demarrage plus recente n'a ete relevee ici.

## Etat retenu
- `OpenClaw` est installe sur `db-layer`.
- Le gateway local n'est pas operatoire au moment de cette revue.
- Ce GO ne corrige rien et n'essaie aucun redemarrage.

## RISKS

- À qualifier.
