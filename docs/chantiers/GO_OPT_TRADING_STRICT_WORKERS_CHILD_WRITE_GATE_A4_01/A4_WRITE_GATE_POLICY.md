# A4_WRITE_GATE_POLICY — Règles d'engagement A4

go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01
version: 0.1-draft
date: 2026-05-14

## 1. Principe

```text
A4 (WRITE_GATED) n'est PAS write libre.
A4 = write sous gated lock avec validation externe obligatoire.
Le défaut est TOUJOURS le refus.
```

## 2. Règles de refus obligatoires

Le runner DOIT REFUSER tout job packet WRITE_GATED si :

| Règle | Condition de refus |
|-------|--------------------|
| R1 | `explicit_write_approval` absent ou `false` |
| R2 | Fichier cible hors `write_allowlist` |
| R3 | Fichier cible est un index global |
| R4 | Input contient un motif de secret (.env, token, key) |
| R5 | Commande demandée est dans `denied_commands` |
| R6 | Job packet invalide contre tasks.index.json |
| R7 | Modèle assigné n'est pas A4 capable |
| R8 | `dry_run` est `false` (dry-run obligatoire pour tout write) |

## 3. explicit_write_approval

Chaque job packet WRITE_GATED doit contenir :

```json
{
  "explicit_write_approval": {
    "approved": true,
    "approver": "humain ou modele fort A2",
    "approval_date": "ISO-8601",
    "scope_files": ["fichier1.md", "fichier2.md"],
    "max_lines_change": 50,
    "dry_run": true,
    "validation_required": ["git_diff", "strong_model_review"]
  }
}
```

## 4. write_allowlist

```text
Chemins autorisés en écriture A4 :

docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_*/**/*.md
docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_*/BRANCH_STATE.md
reports/ai/workers/*.md
scripts/ai/workers/job_packets/*.json

Chemins INTERDITS quoi qu'il arrive :

docs/index/GO_INDEX.md
docs/index/BRANCH_STATE.md
docs/index/MACHINE_WORK_SPLIT.md
scripts/ai/workers/run_task.sh
scripts/ai/workers/_validate_job.py
scripts/ai/workers/models.registry.json
scripts/ai/workers/tasks.index.json
modules/
.env
**/secret*
**/token*
```

## 5. Pipeline de validation

```text
1. Worker propose write → dry-run d'abord
2. Validateur (modele fort A2 ou humain) revoit le dry-run
3. Git diff vérifié (pas d'effet de bord)
4. Si OK → write appliqué dans une transaction bornée
5. Si KO → refus, rollback, rapport d'erreur
```

## 6. Test négatif requis avant tout test positif

```text
Avant d'autoriser le moindre write, le runner doit prouver qu'il REFUSE :
- un job sans explicit_write_approval
- un job hors allowlist
- un job avec input ressemblant à un secret
- un job sur un index global
- un job sans dry_run=true
```

## RISKS

- À qualifier.
