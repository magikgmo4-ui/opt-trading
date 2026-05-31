---
doc_id: STRICT_WORKERS_BILAN_2026_05_31
doc_type: bilan
repo: opt-trading
go_id: GO_STRICT_WORKERS_BILAN_01
status: canonical
produced_at: 2026-05-31
scope: strict_workers framework — bilan complet au 2026-05-31
---

# STRICT_WORKERS — Bilan au 2026-05-31

## Résumé exécutif

```text
Cadre strict_workers = OPÉRATIONNEL
Runners              = 2 (runner_readonly.py + runner_writegated.py)
Task types prouvés   = READ_INVENTORY, PATCH_DRAFT, REVIEW_DRAFT, WRITE_GATED
Pipeline E2E         = PASS (chaînage 2 workers prouvé)
PRs mergées          = 34 (PR #995 → #1028, dont 22 retrofix FILE_SCOPE)
GOs fermés           = 4 parents + 6 children
```

---

## GOs fermés

### Parents

| GO | Statut | PR(s) clé |
| --- | --- | --- |
| GO_OPT_TRADING_STRICT_WORKERS_PARENT_01 | PASS | #1018 (retrofix) + #1019 (promotion) |
| GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01 | PASS | #995 |
| GO_STRICT_WORKERS_WRITE_GATED_PARENT_01 | PASS | #1023 (cadrage) + #1025 (closeout) |
| GO_STRICT_WORKERS_E2E_MULTI_WORKERS_PARENT_01 | PASS | #1026 (cadrage) + #1028 (closeout) |

### Children

| GO | Task type | Statut | PR |
| --- | --- | --- | --- |
| GO_STRICT_WORKERS_CHILD_PATCH_DRAFT_RUNNER_PROVEN_01 | PATCH_DRAFT | PASS | #1021 |
| GO_STRICT_WORKERS_CHILD_PATCH_APPLY_RUNNER_PROVEN_01 | PATCH_APPLY | PASS | #1022 |
| GO_STRICT_WORKERS_CHILD_RUNNER_WRITEGATED_01 | WRITE_GATED | PASS | #1024 |
| GO_STRICT_WORKERS_CHILD_E2E_PIPELINE_01 | E2E_PIPELINE | PASS | #1027 |

### Retrofix FILE_SCOPE.txt

22 GOs rétrofixés (PRs #996–#1018, hors #1012) — `FILE_SCOPE.txt` ajouté sur
l'ensemble des chantiers strict workers existants.

---

## Runners opérationnels

### runner_readonly.py

```text
path        : scripts/ai/workers/runner_readonly.py
mode        : lecture seule — no-write guard permanent
smoke       : GO_STRICT_WORKERS_READONLY_SMOKE_01 — 5 reads, 0 writes
dry-run     : --dry-run
preuve      : PR #995
```

### runner_writegated.py

```text
path        : scripts/ai/workers/runner_writegated.py
modes       : reads-only (default) | --dry-run | --gate-approved
gardes      : BLOCKED_NO_GATE, max_lines_per_write=50, write_allowlist, forbidden_targets
smoke       : GO_STRICT_WORKERS_WRITE_GATED_SMOKE_01 — 1 read, 1 write (gate APPROVE)
preuve      : PR #1024
```

---

## Cycles prouvés

### Cycle PATCH_DRAFT → PATCH_APPLY

```text
1. runner_readonly exécute PATCH_DRAFT → rapport DRAFT_ONLY (PR #1021)
2. Revue humaine → gate APPROVE
3. Patch appliqué sur fichier cible (PR #1022)
Résultat : section '## Runner validé' insérée dans STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
```

### Cycle WRITE_GATED

```text
1. runner_writegated --dry-run → DRY_RUN_WOULD_WRITE
2. Garde max_lines_per_write testée → BLOCKED (65 > 50)
3. runner_writegated (sans flag) → READS_ONLY_PASS, BLOCKED_NO_GATE
4. runner_writegated --gate-approved → PASS, 1 write exécuté
Résultat : reports/ai/workers/GO_STRICT_WORKERS_WRITE_GATED_SMOKE_01.md créé
```

### Cycle E2E 2 workers (chaînage)

```text
Step 1 — big-pickle (READ_INVENTORY)
  reads : STRICT_WORKERS_AUTONOMIE_ETROITE_01.md (3269 B)
  output: GO_STRICT_WORKERS_E2E_STEP1_READ_INVENTORY_01.md

Step 2 — glm-5.1 (REVIEW_DRAFT)
  reads : source (3269 B) + rapport Step 1 (2325 B)  ← chaîné
  output: GO_STRICT_WORKERS_E2E_STEP2_REVIEW_DRAFT_01.md

Preuve : read_operations Step 2 inclut explicitement le rapport Step 1
```

---

## État du framework

### Infrastructure

| Composant | Fichier | Statut |
| --- | --- | --- |
| Doctrine | `docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` | canonical |
| Index des tâches | `scripts/ai/workers/tasks.index.json` | 10 task types |
| Registry modèles | `scripts/ai/workers/models.registry.json` | 13 VERIFIED, 4 RETIRED/ABSENT |
| Runner read-only | `scripts/ai/workers/runner_readonly.py` | PASS |
| Runner write-gated | `scripts/ai/workers/runner_writegated.py` | PASS |
| Validateur | `scripts/ai/workers/_validate_job.py` | PASS |
| Job packets smoke | `scripts/ai/workers/job_packets/` | 5 packets |
| Rapports workers | `reports/ai/workers/` | 10 rapports |
| Logs jobs | `data/runtime_health/job_logs/` | 5 logs |

### Task types (tasks.index.json)

| Task type | Autonomy | Writes | Prouvé |
| --- | --- | --- | --- |
| READ_INVENTORY | A1 | non | ✓ (E2E Step 1) |
| PATCH_DRAFT | A2 | non | ✓ (PR #1021) |
| DOC_DRAFT | A2 | non | — |
| TESTPLAN | A2 | non | — |
| REVIEW_DRAFT | A2 | non | ✓ (E2E Step 2) |
| CLOSEOUT_DRAFT | A2 | non | — |
| CHERRY_PICK_INVENTORY | A2 | non | — |
| FAST_TRIAGE | A1 | non | — |
| ENDPOINT_AUDIT | A1 | non | — |
| WRITE_GATED | A4 | oui (gate) | ✓ (PR #1024) |

### Modèles workers (actifs VERIFIED)

| Modèle | Rôles | Utilisé dans |
| --- | --- | --- |
| big-pickle | READ_INVENTORY, PATCH_DRAFT, DOC_DRAFT, TESTPLAN | E2E Step 1 |
| glm-5.1 | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, REVIEW_DRAFT | PATCH_DRAFT + E2E Step 2 |
| kimi-k2.6 | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY | — |
| qwen3.6-plus | DOC_DRAFT, TESTPLAN, PATCH_DRAFT, REVIEW_DRAFT | — |
| qwen3.5-plus | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | — |
| minimax-m2.5 | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | — |
| minimax-m2.7 | READ_INVENTORY, DOC_DRAFT, PATCH_DRAFT, TESTPLAN | — |

---

## Invariants permanents (rappel)

```text
✓ Un worker ne peut agir que si la tâche est dans tasks.index.json
✓ Aucun write durable sans gate explicite (--gate-approved ou humain)
✓ Secrets / .env / tokens = interdits permanents
✓ Consolidation externe obligatoire avant effet repo durable
✓ FILE_SCOPE.txt présent sur tous les GOs (22 rétrofixés + nouveaux)
✓ Chaque write validé contre write_allowlist + forbidden_targets
```

---

## Prochaines étapes possibles

```text
- Prouver DOC_DRAFT, TESTPLAN, CLOSEOUT_DRAFT via runner_readonly
- Prouver WRITE_GATED sur cible docs/chantiers/** (actuellement allowlist restreinte)
- Matrice multi-worker (models.matrix.md) — référencée comme gap dans STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
- Mettre à jour le doc source pour référencer runner_writegated.py et les 4 modes manquants
- Pipeline 3 workers (READ → PATCH_DRAFT → REVIEW)
```
