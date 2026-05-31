---
report_id: GO_STRICT_WORKERS_3W_STEP2_PATCH_DRAFT_01
go_id: GO_STRICT_WORKERS_CHILD_E2E_PIPELINE_3W_01
task_type: PATCH_DRAFT
pipeline_step: 2/3
worker: kimi-k2.6
chained_from: GO_STRICT_WORKERS_3W_STEP1_READ_INVENTORY_01
status: DRAFT_ONLY
produced_at: 2026-05-31
---

# PATCH_DRAFT — Step 2/3 — Pipeline 3 workers

## FICHIERS_LUS

| Fichier | Source | Taille |
| --- | --- | --- |
| `docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` | doc cible | 3269 B |
| `reports/ai/workers/GO_STRICT_WORKERS_3W_STEP1_READ_INVENTORY_01.md` | Step 1 big-pickle | 2163 B |

---

## OBJECTIF_PATCH

Adresser les 2 GAPs identifiés par big-pickle au Step 1 :
1. Ajouter `runner_writegated.py` dans `## Runner validé`
2. Ajouter les 4 modes manquants dans `## Modes initiaux autorisés`

## FICHIERS_TOUCHES

| Fichier | Action |
| --- | --- |
| `docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` | 2 blocs modifiés — non appliqué |

## DIFF_ATTENDU

### Bloc 1 — Ajout modes manquants dans `## Modes initiaux autorisés`

```diff
--- a/docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
+++ b/docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
@@ -57,6 +57,10 @@
 | TESTPLAN | lister tests et critères PASS/FAIL | non |
 | CHERRY_PICK_INVENTORY | classer commits et dépendances | non |
 | CLOSEOUT_DRAFT | préparer un closeout sans verdict final | non |
+| REVIEW_DRAFT | réviser un rapport ou un patch produit par un worker | non |
+| FAST_TRIAGE | classer rapidement un lot de fichiers ou tickets | non |
+| ENDPOINT_AUDIT | auditer les modèles disponibles sur un endpoint | non |
+| WRITE_GATED | écrire sur cible autorisée après gate explicite | oui (gate) |
```

### Bloc 2 — Ajout `runner_writegated.py` dans `## Runner validé`

```diff
--- a/docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
+++ b/docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
@@ -122,6 +122,7 @@
 runner          : scripts/ai/workers/runner_readonly.py
 validation_date : 2026-05-31
 preuve          : 5 reads, 0 writes
 no-write guard  : actif et testé
 source          : GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01 — PASS (PR #995)
 ```
+
+```text
+runner          : scripts/ai/workers/runner_writegated.py
+validation_date : 2026-05-31
+preuve          : 1 read, 1 write (gate --gate-approved)
+gardes          : BLOCKED_NO_GATE, max_lines=50, write_allowlist
+source          : GO_STRICT_WORKERS_CHILD_RUNNER_WRITEGATED_01 — PASS (PR #1024)
+```
```

## RISQUES

| Risque | Niveau |
| --- | --- |
| Les deux blocs sont distants dans le fichier — risque de conflit faible | FAIBLE |
| Tableau markdown Bloc 1 — préserver alignement `\|` | FAIBLE |
| Ajout consécutif de 4 lignes dans un tableau existant — patch propre | NEGLIGEABLE |

## TESTS_A_EXECUTER

```text
- git apply --check <patch> avant application
- grep "REVIEW_DRAFT\|FAST_TRIAGE\|ENDPOINT_AUDIT\|WRITE_GATED" doc → 4 lignes trouvées
- grep "runner_writegated.py" doc → présent dans ## Runner validé
- python3 -m pytest tests/governance/ → PASS
```

## VERDICT_DRAFT_ONLY

```
VERDICT   = DRAFT_ONLY
worker    = kimi-k2.6
reads     = 2 (source + Step1 output)
writes    = 0
pipeline  = Step 2/3 — patch proposé pour Step 3 (REVIEW_DRAFT / qwen3.6-plus)
gaps      = 2 adressés (runner_writegated + 4 modes manquants)
```
