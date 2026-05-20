# 80 — Security and stop conditions

## Stop immédiat

- `.env`, `secret`, `token`, `credential` dans inputs
- Dirty tree avant runner
- Machine `unreachable`
- Fleet `FAIL`
- `trade_executor` demandé sans gate
- `kil_v1` restart demandé
- Commandes destructives : `rm -rf`, `chmod -R`, `chown -R`
- Git opérations interdites en runner : `git add`, `git commit`, `git push`, `git merge`, `git rebase`
- Write externe sans `WRITE_GATED`
- Mobile tente d'exposer secrets
- `cursor-ai` traité comme Linux runtime
- prompt mot de passe / TTY inattendu pendant une verification read-only
- artefact `ide.yml` inattendu si un protocole tmux-ide est ensuite mobilise
- sortie `fleet_status=FAIL`

## Restart policy

| Composant | Restart |
|---|---|
| gateway_openclaw | Gated/autorisé si health down prouvé |
| fleet timer | Autorisé |
| screeners | Autorisé selon policy |
| desk-pro | Autorisé selon watchdog |
| trade_executor | Manuel seulement |
| kil_v1 | Jamais auto |
| trading engines | Manuel après investigation |

## Mobile restrictions

- Read-only par défaut
- Aucune clé dans presse-papiers partagé
- Pas de restart critique depuis mobile
- Attach/detach OK
- Logs OK si non sensibles

## Classification "read-only" (checklist distante)

| Etape | Commande | Classe | Side effects attendus |
|---:|---|---|---|
| 1-2 | `test -d ... && git status --short --branch` | READ_ONLY | lecture FS + lecture git |
| 3-4 | `gateway_openclaw cmd.sh health/probe` | READ_ONLY_REMOTE | requetes health/probe (pas de start/stop) |
| 5 | `fleet_orchestrator.py --dry-run` | READ_ONLY | lecture runtime_health (sshfs/ssh/cat), pas d'ecriture locale, pas de Telegram |
| 6-10 | `tmux ls` / `tmux has-session ...` | READ_ONLY | lecture tmux server |
| 11 | `deskpro_watchdog.sh run-once` | READ_MOSTLY | cree/append `tmp/deskpro_watchdog.log` + curl endpoints locaux |
| 12 | `deskpro_watchdog.sh status` | READ_MOSTLY | lecture `tmp/deskpro_watchdog.pid` + tail log si present |

Si un protocole strictement sans ecriture est requis, remplacer 11/12 par des
lectures directes (ex: `curl /desk/health`, `curl /desk/status`) sans toucher
au watchdog.

## Stop durant checklist distante

- stop si `test -d /opt/trading` echoue
- stop si `git status` revele un contexte douteux que l'operateur ne valide pas
- stop si `gateway_openclaw ... health` ou `probe` echoue
- stop si `tmux ls` montre une topologie inattendue non comprise
- stop si `deskpro_watchdog.sh run-once` retourne un etat non interpretable
- stop avant mobile si les etapes SSH read-only precedentes ne sont pas stables

## App bridges

Respecter le runner contract existant :
- READ_ONLY
- DRAFT_ONLY
- WRITE_GATED
- dry_run true par défaut
- Validation externe obligatoire pour write
