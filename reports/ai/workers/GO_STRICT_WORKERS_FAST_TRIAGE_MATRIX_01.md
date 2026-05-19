# STRICT WORKER REPORT — FAST_TRIAGE

## RESUME

Tri des actifs strict workers dans opt-trading apres PR #606 (promotion 8 job packets) et run READ_INVENTORY.

Decoupage en 3 axes: job packets, modeles workers, chantiers GO.

## CLASSEMENT

### Axe 1: Job Packets par priorite d execution

| Priorite | Packet | Task type | Autonomy | Raison |
|---|---|---|---|---|
| P0 | READ_INVENTORY_MATRIX_01 | READ_INVENTORY | A1 | DEJA RUN (PASS) |
| P1 | FAST_TRIAGE_MATRIX_01 | FAST_TRIAGE | A1 | EN COURS (ce run) |
| P2 | ENDPOINT_AUDIT_MATRIX_01 | ENDPOINT_AUDIT | A1 | Read-only, verify registry |
| P3 | DOC_DRAFT_MATRIX_01 | DOC_DRAFT | A2 | Read-only, doc output |
| P4 | TESTPLAN_MATRIX_01 | TESTPLAN | A2 | Read-only, plan output |
| P5 | CHERRY_PICK_INVENTORY_MATRIX_01 | CHERRY_PICK_INVENTORY | A2 | Read-only git history |
| P6 | PATCH_DRAFT_MATRIX_01 | PATCH_DRAFT | A2 | Dry-run diff |
| P7 | WRITE_GATED_DRYRUN_MATRIX_01 | WRITE_GATED | A4 | Dry-run write gated |

### Axe 2: Job Packets EXISTANTS (non-MATRIX) par type

| Categorie | Packets | Usage |
|---|---|---|
| SMOKE | READONLY_SMOKE_01, POOL_SMOKE_* (3) | Tests CI/CD read-only |
| E2E | E2E_READ_INVENTORY_A, E2E_FAST_TRIAGE_B | Tests E2E |
| A4 NEGATIVE | N1_NO_APPROVAL..N5_PATCH_DRAFT_WRITE | Tests de refus WRITE_GATED |
| A4 POSITIVE | P6_GATED_WRITE | Test d approbation WRITE_GATED |
| A4 REEL | WRITE_REEL_TEST | Test write reel |
| IMPL | PATCH_DRAFT_IMPL_01 | Implementation patch |

### Axe 3: Modeles Workers par capacite

| Classe | Modeles | Autonomy max | Roles |
|---|---|---|---|
| VERIFIED A2 | glm-5.1, kimi-k2.5/6, qwen3.5/6-plus, minimax-m2.5/7, big-pickle | A2 | Tous types (read, patch, doc, test, cherry-pick, review) |
| VERIFIED A1 | gpt-5-nano | A1 | FAST_TRIAGE, READ_INVENTORY |
| VERIFIED_FREE A1 | nemotron-3-super-free, deepseek-v4-flash-free, ring-2.6-1t-free, trinity-large-preview-free, minimax-m2.5-free | A1 | READ_INVENTORY, FAST_TRIAGE, DOC_DRAFT |
| RETIRED | hy3-preview-free, ling-2.6-flash-free | A0 | Plus dans l endpoint |
| ABSENT | mimo-v2*, deepseek-v4-pro, deepseek-v4-flash | A0 | Non disponibles |

### Axe 4: Chantiers Strict Workers par statut

| Statut | Chantiers | Count |
|---|---|---|
| MERGED | WORKER_POOL_EXTENSION_01, AIRTABLE_INTEGRATION_01, CI_CD_01, CI_CD_IMPLEMENTATION_01, CI_CD_FIRST_SMOKE_RUN_01, CLICKUP_TASK_TRACKER_01, JOB_PACKETS_PROMOTION_01 | 7 |
| DONE (local) | JOB_PACKET_FIRST_REAL_RUN_01 (READ_INVENTORY) | 1 |
| NOT_STARTED | — | 0 |

## RISQUES

1. Le runner lock bloque sur untracked files — impossible de lancer 2 packets consecutifs sans commit ou stash intermediaire
2. Seuls 3 modeles VERIFIED sont eligibles pour FAST_TRIAGE (gpt-5-nano, minimax-m2.5, qwen3.5-plus) — les VERIFIED_FREE sont ignores par le validateur
3. Aucun mecanisme de retry si le worker produit un rapport invalide (sections manquantes, verdict absent)
4. Les globs larges (docs/**, scripts/**, modules/**) en allowed_inputs donnent acces a ~200 modules et ~1000+ fichiers — risque de surcharge pour le worker

## TODO

1. [P0] Runner ce rapport FAST_TRIAGE (en cours)
2. [P1] Lancer ENDPOINT_AUDIT_MATRIX_01 (A1, read-only)
3. [P2] Lancer DOC_DRAFT_MATRIX_01 (A2)
4. [P3] Lancer TESTPLAN_MATRIX_01 (A2)
5. [P4] Lancer CHERRY_PICK_INVENTORY_MATRIX_01 (A2)
6. [P5] Lancer PATCH_DRAFT_MATRIX_01 (A2)
7. [P6] Lancer WRITE_GATED_DRYRUN_MATRIX_01 (A4)
8. [BACKLOG] Decider si les VERIFIED_FREE doivent etre inclus dans valid_workers par _validate_job.py

## VERDICT_DRAFT_ONLY
