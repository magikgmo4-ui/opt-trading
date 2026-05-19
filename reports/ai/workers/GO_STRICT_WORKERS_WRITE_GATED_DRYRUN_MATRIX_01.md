# STRICT WORKER REPORT — WRITE_GATED_DRYRUN

## 13_ESTABLISHED

| Element | Valeur |
|---|---|
| GO | GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01 |
| Status | DRAFT_ONLY / DRY_RUN |
| Autonomy | A4 (write gated, dry-run only) |
| Default worker | glm-5.1 |
| Write mode | DRY_RUN — aucun write reel |
| Contexte | 7/8 job packets run (READ_INVENTORY, FAST_TRIAGE, ENDPOINT_AUDIT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, PATCH_DRAFT) + 1 en cours (WRITE_GATED_DRYRUN) |
| Decouverte cle | ring-2.6-1t-free + trinity-large-preview-free retirees de l endpoint depuis le 2026-05-14 |

## 14_HYPOTHESIS

1. Le patch propose dans PATCH_DRAFT (mettre a jour models.registry.json) est le seul write necessaire actuellement sur la chaine strict workers
2. Le write est dans l allowlist (scripts/ai/workers/job_packets/** ne match pas, mais models.registry.json n est pas dans l allowlist — il est dans forbidden_targets!)
3. Donc: le patch registry ne PEUT PAS etre execute via WRITE_GATED — il doit passer par une PR manuelle

## WRITE_PLAN

Le write propose dans PATCH_DRAFT cible **scripts/ai/workers/models.registry.json** — mais ce fichier est explicitement dans la `forbidden_targets` de WRITE_GATED:

```json
"forbidden_targets": [
  "docs/index/GO_INDEX.md",
  "docs/index/BRANCH_STATE.md",
  "scripts/ai/workers/run_task.sh",
  "scripts/ai/workers/_validate_job.py",
  "scripts/ai/workers/models.registry.json",
  "scripts/ai/workers/tasks.index.json"
]
```

**WRITE PLAN: BLOCKED — forbidden target detected**

Actions alternatives:
1. Creer une PR manuelle qui modifie models.registry.json
2. Ou creer un nouveau job packet specifique pour la mise a jour du registry (avec WRITE_GATED modifie pour autoriser le registry)
3. Ou utiliser un write reel (GO_STRICT_WORKERS_A4_WRITE_REEL_TEST.json) depuis une branche feature

## WRITE_DIFF_ATTENDU

Non applicable — write bloque par forbidden_targets.

```diff
# Patch NON executable via WRITE_GATED
```

## VALIDATION_EXTERNE

La modification du registry requiert une approbation ecrite explicite car:
- Le registry est reference par tous les job packets
- Une erreur dans le registry bloque toute la chaine strict workers
- Le registry est source de verite pour les validations CI/CD

Processus recommande:
1. Creer une branche feature
2. Appliquer le diff de PATCH_DRAFT
3. Lancer la CI/CD (validate + smoke)
4. Creer une PR
5. Merge apres approbation

## DRY_RUN_RESULT

| Check | Resultat |
|---|---|
| Dry-run required | ✓ (dry_run_required: true) |
| Target: models.registry.json | BLOCKED (forbidden target) |
| Lines > 50 | N/A (bloque avant) |
| Write outside allowlist | N/A (bloque avant) |
| Forbidden target detected | ✓ STOP |

## RISQUES

1. Si on force le write vers models.registry.json via un autre canal, le registry peut devenir incoherent avec l endpoint
2. Les 2 modeles retirees (ring-2.6-1t-free, trinity-large-preview-free) sont toujours dans 3 job packets — la CI/CD smoke echouera si elle tente d utiliser l endpoint avec ces modeles
3. Le forbidden_targets sur le registry est correct (garde-fou de securite) mais bloque la mise a jour legitime

## VERDICT_WRITE_GATED

DRY_RUN — BLOCKED par forbidden_targets sur models.registry.json. Patch registry requiert une PR manuelle.

Write reel NON effectue. Dry-run TERMINE.
