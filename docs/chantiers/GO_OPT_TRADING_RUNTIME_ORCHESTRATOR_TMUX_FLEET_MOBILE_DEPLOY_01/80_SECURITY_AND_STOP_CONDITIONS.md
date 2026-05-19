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

## App bridges

Respecter le runner contract existant :
- READ_ONLY
- DRAFT_ONLY
- WRITE_GATED
- dry_run true par défaut
- Validation externe obligatoire pour write
