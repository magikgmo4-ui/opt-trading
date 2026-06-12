# ENFORCEMENT_PLAN

## Objectif

Transformer la politique de rétention documentée en garde-fous opératoires vérifiables.

## Dépendances

- `GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01` (merged)
- `docs/chantiers/.../SESSION_RETENTION_POLICY_01.md`
- `docs/chantiers/.../RUNBOOK_SESSION_ROTATION_01.md`

## Axes

### A. Script de diagnostic et purge

- script bash détectant les sessions saturées (PROMPT_ERROR, input tokens = 0)
- purge des sessions archivées > 30 jours
- rapport d'état avant/pendant/après

### B. Garde-fous vérifiables

| Garde-fou | Vérification | Automatisable |
|-----------|-------------|:-------------:|
| Seuil max 10 runs par session | Compter les runs dans le session log | Oui (script) |
| Détection PROMPT_ERROR | grep dans les .jsonl | Oui (script) |
| Input tokens > 0 | Vérifier lastCallUsage.input | Oui (script) |
| Rotation forcée après 7 jours | Date de création du fichier .jsonl | Oui (cron) |

### C. Smoke post-purge

- Exécuter le smoke canonique après chaque purge
- Vérifier cold < 180s, warm < 60s
- Vérifier input tokens > 0

### D. Passage/échec

| Critère | PASS | FAIL |
|---------|:----:|:----:|
| Script purge exit 0 | ✔ | ✘ |
| Session archivée détectée | ✔ | — |
| After-purge cold smoke < 180s | ✔ | timeout |
| After-purge warm smoke < 60s | ✔ | timeout |
| Aucun trade/worker | ✔ | trade détecté |

## Procédure de validation

1. Exécuter le script de diagnostic
2. Forcer une rotation si session saturée
3. Exécuter le smoke canonique
4. Vérifier les métriques
5. Documenter le résultat dans CHECKPOINT.md

## RISKS

- À qualifier.
