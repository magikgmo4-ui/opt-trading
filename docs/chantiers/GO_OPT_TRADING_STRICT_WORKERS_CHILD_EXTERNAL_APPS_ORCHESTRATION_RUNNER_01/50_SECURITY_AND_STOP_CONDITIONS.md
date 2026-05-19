# Security & Stop Conditions

## Stop immédiat (BLOCKED)

Le runner DOIT s'arrêter immédiatement si l'une des conditions suivantes est détectée :

| Condition | Raison |
|---|---|
| `.env` ou `**/*secret*` ou `**/*token*` ou `**/*credential*` dans les inputs | Violation de la politique no-secret |
| Modèle absent du registry (`ABSENT_CURRENT_ENDPOINT`) | Worker non disponible |
| Modèle retiré (`RETIRED_CURRENT_ENDPOINT`) | Worker retiré de l'endpoint |
| Modèle remplacé (`OBSOLETE_REPLACED`) | Worker obsolète |
| `job_packet_id` invalide ou inexistant | Packet non trouvé |
| Job packet pas dans `scripts/ai/workers/job_packets/` | Hors scope |
| `mode` non autorisé par le packet (ex: WRITE_GATED sur PATCH_DRAFT) | Incohérence mode/packet |
| `task_type` inconnu dans `tasks.index.json` | Type non défini |
| `default_worker` pas `VERIFIED` dans le registry | Worker non vérifié |
| Credentials bridge absents pour l'app ciblée | APP_BLOCKED_NO_CREDENTIALS |
| Git status modifié avant exécution (dirty tree) | Risque de modification non contrôlée |
| Write demandé sur une `forbidden_target` | Cible protégée |
| Write demandé sans `explicit_write_approval` | Approval manquante |
| `dry_run=false` sans validation externe | Passage en production non autorisé |
| Appel à `git add`, `git commit`, `git push`, `git rebase`, `git merge` | Opérations git interdites |
| Appel à `rm -rf`, `chmod -R`, `chown -R` | Opérations système destructives |

## Alerte sans blocage (WARNING)

Le runner doit LOGGUER un avertissement (sans bloquer) pour :

| Condition | Action |
|---|---|
| `default_worker` pas dans `worker_candidates` | Logger, utiliser le premier candidat valide |
| App bridge en fail-open (Airtable) | Logger l'erreur bridge sans bloquer |
| Batch > 10 records (Airtable) | Logger, tronquer à 10 |
| Temps d'exécution > 120s | Logger, continuation |
| Sortie > 500 lignes | Logger, tronquer |
| Dry-run actif (pas de write réel) | Logger, mode lecture seule |

## Règles de validation externe (WRITE_GATED)

Pour tout WRITE_GATED :

1. Le packet DOIT contenir `explicit_write_approval` avec `approved=true`
2. Le `scope_files` DOIT être dans la `write_allowlist` de `tasks.index.json`
3. Le `max_lines_change` DOIT être respecté
4. Le `dry_run` DOIT être `true` pour le premier passage
5. La cible NE DOIT PAS être dans `forbidden_targets`
6. Un modèle fort ou humain DOIT valider le diff avant write réel
7. Le write réel DOIT être réversible (rollback plan documenté)
