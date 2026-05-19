# Methode d'operation retenue

## Regle principale
- Toujours operer `OpenClaw` dans le contexte utilisateur `openclaw`.
- Ne pas piloter le runtime `OpenClaw` depuis le contexte de l'utilisateur SSH courant.

## Sequence correcte
1. Verifier le contexte runtime :
   - `sudo -iu openclaw bash -lc 'whoami; hostname; pwd; echo HOME=$HOME; echo PATH=$PATH'`
   - `sudo -iu openclaw bash -lc 'command -v openclaw; openclaw --version'`
2. Verifier l'etat local :
   - `tmux ls`
   - `ps aux | grep -i openclaw | grep -v grep`
   - `ss -ltnp | grep 18789`
3. Si un demarrage est necessaire, confirmer d'abord la commande par :
   - l'aide CLI `openclaw gateway --help`
   - la doc locale
   - le module repo-side `modules/gateway_openclaw/scripts/start.sh`
4. Utiliser la facade repo-side validee si applicable :
   - `cd /opt/trading`
   - `bash modules/gateway_openclaw/scripts/cmd.sh start`
5. Verifier apres action :
   - `bash modules/gateway_openclaw/scripts/cmd.sh status`
   - `bash modules/gateway_openclaw/scripts/cmd.sh health`
   - `bash modules/gateway_openclaw/scripts/cmd.sh probe`
   - `curl -fsS http://127.0.0.1:18789/ | head -40`

## Invariants runtime
- `tmux` porte la persistance de la session locale `openclaw-gateway`.
- `OpenClaw` reste le control plane du runtime.
- `db-layer` reste seulement l'hote actuel.
- Les secrets, tokens et contenus sensibles ne doivent pas etre exposes dans les passes de controle.

## State dir
- Le `state_dir` ne doit etre traite qu'en verification secondaire.
- Il ne devient prioritaire que si le gateway refuse de demarrer ou si un fait runtime nouveau l'impose.
- Aucun nettoyage, aucune suppression ni aucune reparation de `state_dir` sans preuve et sans backup dedie.

## Methode a conserver
- La methode correcte pour `db-layer` est donc `owner-session openclaw -> module repo-side -> verification tmux/process/port/health/dashboard`.
