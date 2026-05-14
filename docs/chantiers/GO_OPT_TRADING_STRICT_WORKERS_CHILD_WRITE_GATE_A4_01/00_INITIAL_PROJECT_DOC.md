---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01
machine: fantome
status: cadrage
lifecycle_stage: opening
topic_keys:
  - strict_workers
  - child
  - write_gate
  - A4
  - gated_write
source_kind: canonical
point_de_reprise: "Promouvoir le runner vers A4 (WRITE_GATED) avec validation externe obligatoire"
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01/90_CLOSEOUT.md
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
  - scripts/ai/workers/run_task.sh
---

# GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01 — INITIAL PROJECT DOC

## 1_MASTER_TARGET

Promouvoir le runner strict_workers vers le niveau A4 (WRITE_GATED) : permettre des ecritures controlees, bornees, avec validation externe obligatoire, sans jamais basculer en write libre.

## 2_PARENT_HERITAGE

| Heritage | Source |
|----------|--------|
| Runner operationnel | `run_task.sh` (A1/A2, merge #355) |
| Pool valide | 15 VERIFIED/VERIFIED_FREE (merge #362, #364) |
| Garde-fous actifs | runner_lock, patch_draft_guard, denied_commands, denied_inputs |
| Parent | `GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01` (PASS) |

## 3_PRINCIPE_WRITE_GATED

```text
A4 (WRITE_GATED) ≠ write libre.

A4 = write autorise UNIQUEMENT si :
1. Le job packet contient explicit_write_approval = true
2. Le fichier cible est dans une allowlist de chemins
3. Le write est simule (dry-run) puis valide
4. Un validateur externe (modele fort / humain / Git diff) approuve
5. En cas de doute : refus par defaut

Regle cardinale :
"Toute ecriture sans approval explicite est refusee."
"Toute ecriture hors allowlist est refusee."
"Toute ecriture sur un index global est refusee sauf preuve."
```

## 4_PHASES

### Phase A — Cadrage WRITE_GATE_A4
- Documenter le concept, les regles, les garde-fous
- Definir les invariants A4

### Phase B — Policy gate
- Ajouter `WRITE_GATED` comme task type dans tasks.index.json
- Definir `explicit_write_approval` dans le schema job packet
- Definir `write_allowlist` pour les fichiers/chemins autorises
- Ajouter les regles de refus au runner (`_validate_job.py`)

### Phase C — Tests negatifs (en premier)
- Test 1 : WRITE_GATED sans explicit_write_approval → REFUSE
- Test 2 : WRITE_GATED hors allowlist → REFUSE
- Test 3 : WRITE_GATED avec input ressemblant a un secret → REFUSE
- Test 4 : WRITE_GATED sur un index global → REFUSE
- Test 5 : PATCH_DRAFT (A2) avec tentative write → REFUSE

### Phase D — Test positif borne
- Test 6 : WRITE_GATED avec approval, dans allowlist, doc-only → ACCEPTE (dry-run)
- Test 7 : WRITE_GATED simule sur BRANCH_STATE.md avec validation → ACCEPTE (write dry-run)

### Phase E — Verdict
- Produire 90_CLOSEOUT.md
- PASS si tous les tests negatifs refusent ET le test positif accepte
- BLOCKED si un test negatif laisse passer un write
- REMAINING_GAP si limitation documentee

## 5_INVARIANTS_A4

```text
- denied_commands conserve (git add, commit, push, rebase, merge)
- denied_inputs conserve (.env, secrets, tokens, keys)
- explicit_write_approval obligatoire pour tout write
- write_allowlist : docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_*, reports/ai/workers/*
- Aucun write sur scripts/ sans validation supplementaire
- Aucun write sur modules/ sans GO dedie
- Aucun write sur index globaux (GO_INDEX.md, BRANCH_STATE.md racine, MACHINE_WORK_SPLIT.md)
- Stash branch_arbitration preserve
- Dry-run systematique avant write reel
- Validation externe obligatoire (modele fort A2 + humain + Git diff)
```

## 6_RESUME_POINT

```text
fantome
→ sot/mainline @ 1a5dd9f
→ GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01
→ Promouvoir vers A4 sans write libre
→ Refus par defaut, approval obligatoire
→ Tests negatifs en premier
```
