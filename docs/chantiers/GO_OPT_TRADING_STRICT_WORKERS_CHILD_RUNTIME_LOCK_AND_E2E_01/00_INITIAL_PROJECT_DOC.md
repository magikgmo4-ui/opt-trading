---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
machine: fantome
status: cadrage
lifecycle_stage: opening
topic_keys:
  - strict_workers
  - runtime_lock
  - patch_draft
  - e2e_multi_workers
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/90_CLOSEOUT.md
point_de_reprise: "Verrouiller le runner strict_workers, preparer PATCH_DRAFT, E2E multi-workers borne"
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/03_READONLY_SMOKE_VALIDATION.md
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
---

# GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01 — INITIAL PROJECT DOC

## 1_MASTER_TARGET

Passer du parent `CLOSEOUT_DOC_ONLY` a un child runtime effectif : verrouiller le runner strict_workers, preparer un PATCH_DRAFT borne, executer un E2E multi-workers controle, et produire un verdict documente (PASS / BLOCKED / REMAINING_GAP).

## 2_PARENT_HERITAGE

Le parent `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` est CLOSEOUT_DOC_ONLY (merge `05f16f2`). Il fournit :

| Heritage | Fichier |
| --- | --- |
| Cadre canonique | `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/00_INITIAL_PROJECT_DOC.md` |
| Smoke validation | `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/03_READONLY_SMOKE_VALIDATION.md` (VALIDATION_PASS_DRAFT_ONLY) |
| Task index | `scripts/ai/workers/tasks.index.json` (DRAFT_ONLY, 6 task types) |
| Model registry | `scripts/ai/workers/models.registry.json` (13 VERIFIED, 5 ABSENT) |
| Job packet example | `scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json` |
| Autonomie etroite spec | `docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` |

## 3_BORNES_DU_CHILD

Ce child est strictement borne a :

1. **Verrouiller le runner** — produire un script runner `run_task.sh` reproductible, chargeant tasks.index.json + models.registry.json + job packet, routant vers le worker approprie, avec les garde-fous actifs
2. **PATCH_DRAFT** — preparer un job packet PATCH_DRAFT pour une tache reelle bornee (ex: doc draft, inventory patch), sans appliquer le patch
3. **E2E multi-workers** — executer 2 workers distincts en parallele sur 2 types de taches differentes, verifier que chaque worker respecte ses bornes
4. **Verdict** — PASS si tout est valide, BLOCKED si obstacle, REMAINING_GAP si limite documentee

## 4_PLAN_D_EXECUTION

### Phase A — Verrouiller le runner

```text
1. Creer scripts/ai/workers/run_task.sh
2. Le runner doit :
   - charger le job packet JSON passe en argument
   - valider que le packet reference un task_type connu dans tasks.index.json
   - valider que le worker candidat est VERIFIED dans models.registry.json
   - verifier que les inputs autorises sont presents et sans secret
   - interdire toute commande dans denied_commands
   - interdire tout acces aux fichiers dans denied_inputs
   - router le job vers le prompt approprie
   - collecter la sortie dans reports/ai/workers/<job_packet_id>.md
   - marquer la sortie DRAFT_ONLY
3. Tester le runner sur le smoke READ_INVENTORY existant
```

### Phase B — PATCH_DRAFT borne

```text
1. Creer scripts/ai/workers/job_packets/GO_STRICT_WORKERS_PATCH_DRAFT_IMPL_01.json
2. Task type: PATCH_DRAFT
3. Scope: proposer un patch minimal doc-only (ex: corriger un closeout, ajouter une entree inbox)
4. Worker cible: glm-5.1 (VERIFIED, A2, PATCH_DRAFT)
5. Sortie: DRAFT_ONLY, patch propose mais NON applique
6. Validation externe obligatoire avant tout merge
```

### Phase C — E2E multi-workers

```text
1. Lancer simultanement :
   - Worker A (qwen3.5-plus): READ_INVENTORY sur docs/agents/strict_workers/
   - Worker B (minimax-m2.5): FAST_TRIAGE sur le meme perimetre
2. Verifier :
   - Chaque worker ne lit que ses inputs autorises
   - Chaque worker ne produit que dans reports/ai/workers/
   - Aucun worker ne modifie le repo
   - Les sorties sont DRAFT_ONLY
   - Les sorties de 2 workers differents ne se contaminent pas
3. Consolider les 2 sorties dans un rapport E2E
```

### Phase D — Verdict

```text
Produire docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01/90_CLOSEOUT.md avec :
- checklist par phase
- verdict: PASS / BLOCKED / REMAINING_GAP
- preuves (SHA runner, job packets, rapports)
- NEXT_GO si applicable
```

## 5_INVARIANTS (herites du parent)

```text
- Aucun secret, .env, token, cle expose
- Aucune commande git (add, commit, push, rebase, merge)
- Aucun write runtime non valide
- Toute sortie = DRAFT_ONLY
- Validation finale externe (modele fort / humain / Git diff)
- Seuls les modeles VERIFIED du registry sont autorises
- Stash branch_arbitration preserve
```

## 6_GARDE_FOUS_ADDITIONNELS (child)

```text
- Runner: timeout 120s par job
- Job packets: valides contre tasks.index.json avant execution
- Sorties: max 500 lignes par rapport
- Parallele: max 2 workers simultanes dans cette phase
- Rollback: aucun fichier source modifie (git status clean avant/apres)
- Ne pas modifier les index globaux (GO_INDEX, BRANCH_STATE, MACHINE_WORK_SPLIT)
```

## 7_CANONICAL_STATE

```text
- Branche: go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01
- Base: sot/mainline (merge parent 05f16f2)
- Machine: fantome
- Perimetre: doc/scripts/reports uniquement
- Statut initial: cadrage
```

## 8_DEPENDANCES

```text
- tasks.index.json (present, DRAFT_ONLY)
- models.registry.json (present, 13 VERIFIED)
- job packet READ_INVENTORY existant (smoke)
- OpenCode local operationnel
- Modeles VERIFIED accessibles via OpenCode
```

## 9_RISQUES

| Risque | Mitigation |
| --- | --- |
| Modele VERIFIED absent du endpoint courant | Fallback vers un autre VERIFIED du meme role |
| Runner ne peut pas isoler les commandes dangereuses | Bloquer et documenter comme BLOCKED |
| E2E: contamination croisee entre workers | Verifier git status entre chaque worker |
| Stash branch_arbitration modifie | Check git stash list avant/apres |

## 10_CRITERES_PASS

```text
Phase A PASS si :
- run_task.sh existe et est executable
- le runner charge le job packet, valide contre tasks.index.json
- le runner refuse un job packet invalide (test negatif)
- le runner execute le smoke READ_INVENTORY avec succes

Phase B PASS si :
- job packet PATCH_DRAFT cree
- le runner route vers glm-5.1
- le patch propose est DRAFT_ONLY
- aucun fichier source modifie

Phase C PASS si :
- 2 workers s'executent sans collision
- chaque worker respecte son scope
- sorties DRAFT_ONLY non contaminees

PASS global = A + B + C tous PASS.
```

## 11_NEXT_GO

Apres PASS : ouvrir un child d'extension du pool (nouveaux modeles, nouvelles taches autorisees, write gate si applicable).

Apres BLOCKED : documenter le blocage, proposer mitigation.

## 12_RESUME_POINT

```text
fantome
→ STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01
→ Branche: go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01
→ Phase A en premier (verrouiller le runner)
→ Ne pas passer a la Phase B sans validation de la Phase A
→ Garde-fous stricts sur chaque phase
```

## RISKS

- À qualifier.
