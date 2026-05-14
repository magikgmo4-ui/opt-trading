---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01
machine: fantome
status: cadrage
lifecycle_stage: opening
topic_keys:
  - strict_workers
  - pool_extension
  - model_registry
  - endpoint_revalidation
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01/90_CLOSEOUT.md
point_de_reprise: "Revalider les modeles ABSENT, ajouter les VERIFIED, etendre les task types de maniere bornee"
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01/90_CLOSEOUT.md
  - scripts/ai/workers/models.registry.json
  - scripts/ai/workers/tasks.index.json
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
---

# GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01 — INITIAL PROJECT DOC

## 1_MASTER_TARGET

Etendre et revalider le pool de workers stricts en interrogeant l'endpoint OpenCode Zen courant (`https://opencode.ai/zen/v1/models`), en ajoutant les nouveaux modeles VERIFIED, en retirant les modeles disparus, et en mettant a jour le task index sans toucher au runner ni au runtime.

## 2_PARENT_HERITAGE

| Heritage | Source |
|----------|--------|
| Runner lock operationnel | `GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01` (PASS, merge #355) |
| Registry actuel | `scripts/ai/workers/models.registry.json` (14 VERIFIED, 6 ABSENT, 20 total) |
| Task index actuel | `scripts/ai/workers/tasks.index.json` (6 task types, DRAFT_ONLY) |
| Parent doc-only | `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` (CLOSEOUT_DOC_ONLY, merge 05f16f2) |

## 3_BORNES_DU_CHILD

Ce child est strictement borne a :

1. **Reinterroger l'endpoint** — `https://opencode.ai/zen/v1/models` au 2026-05-14
2. **Comparer avec le registry actuel** — identifier les ajouts, retraits, changements
3. **Mettre a jour models.registry.json** — ajouter les nouveaux VERIFIED/VERIFIED_FREE, marquer comme RETIRED les disparus
4. **Mettre a jour tasks.index.json** — ajouter les nouveaux modeles aux preferred_workers appropries
5. **Aucun write runtime** — toujours en DRAFT_ONLY, runner inchange
6. **Ne pas toucher au runner** — run_task.sh intact

## 4_PLAN_D_EXECUTION

### Etape 1 — Audit endpoint courant

```text
GET https://opencode.ai/zen/v1/models
Date: 2026-05-14
```

### Etape 2 — Comparaison registry

```text
Pour chaque modele du registry :
- VERIFIED + present endpoint → conserve VERIFIED
- VERIFIED + absent endpoint → RETIRED_CURRENT_ENDPOINT, roles deselectionnes
- ABSENT + present endpoint → promu VERIFIED / VERIFIED_FREE
- ABSENT + absent endpoint → conserve ABSENT_CURRENT_ENDPOINT
- Nouveau dans endpoint, absent registry → ajoute VERIFIED_FREE (A1)
```

### Etape 3 — Mise a jour

```text
- models.registry.json : ajouts, retraits, changements de statut
- tasks.index.json : preferred_workers ajustes
- Rapport de revalidation : 01_ENDPOINT_REVALIDATION_REPORT.md
```

### Etape 4 — Verdict

```text
Produire 90_CLOSEOUT.md avec :
- liste des changements
- nouveau total modeles VERIFIED/VERIFIED_FREE
- verdict PASS / BLOCKED / REMAINING_GAP
```

## 5_INVARIANTS

```text
- Aucun secret, .env, token, cle expose
- Aucune commande git (add, commit, push, rebase, merge) sauf pour la PR finale
- Aucun write runtime non valide
- Toute sortie = DRAFT_ONLY
- Seuls les modeles VERIFIED/VERIFIED_FREE du registry mis a jour sont autorises
- Runner run_task.sh intact
- Stash branch_arbitration preserve
- Aucun index global modifie
```

## 6_CRITERES_PASS

```text
PASS si :
- models.registry.json mis a jour avec au moins 1 nouveau VERIFIED
- tasks.index.json coherent avec le registry
- Tous les modeles VERIFIED/VERIFIED_FREE sont confirmes endpoint
- Tous les modeles ABSENT le restent sans etre routes
- Aucun modele RETIRED route dans tasks.index.json
- Runner run_task.sh inchange
- Git diff limite a docs/chantiers/ + scripts/ai/workers/
```

## 7_RESUME_POINT

```text
fantome
→ sot/mainline @ 1571af5
→ GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01
→ Revalider endpoint → ajouter VERIFIED → etendre pool
→ Runner intact, read-only/draft-only uniquement
→ Ne pas ouvrir Write gate A4
```
