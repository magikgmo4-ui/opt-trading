---
report_id: GO_STRICT_WORKERS_3W_STEP1_READ_INVENTORY_01
go_id: GO_STRICT_WORKERS_CHILD_E2E_PIPELINE_3W_01
task_type: READ_INVENTORY
pipeline_step: 1/3
worker: big-pickle
status: DRAFT_ONLY
produced_at: 2026-05-31
---

# READ_INVENTORY — Step 1/3 — Pipeline 3 workers

## FICHIERS_LUS

| Fichier | Taille |
| --- | --- |
| `docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` | 3269 B |

---

## 13_ESTABLISHED

| Élément | Statut |
| --- | --- |
| Définition strict worker | ETABLI |
| Architecture 5 couches | ETABLI |
| 6 modes autorisés dans le doc : READ_INVENTORY, PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, CLOSEOUT_DRAFT | ETABLI |
| Interdits permanents (git write, secrets, rm -rf…) | ETABLI |
| Format de sortie obligatoire (9 sections) | ETABLI |
| Règle de consolidation (3 conditions) | ETABLI |
| Premier worker pilote : big-pickle-worker | ETABLI |
| Section `## Runner validé` : runner_readonly.py, 2026-05-31 | ETABLI |

## 14_HYPOTHESIS

| Élément | Statut |
| --- | --- |
| `status: draft_canonical` — stable mais non encore promu canonical | HYPOTHESE |

## 15_REMAINING_GAP

| Gap | Fichier cible | Détail |
| --- | --- | --- |
| `runner_writegated.py` absent de la section `## Runner validé` | STRICT_WORKERS_AUTONOMIE_ETROITE_01.md | Ajouté en PR #1024, doc non mis à jour |
| 4 modes manquants dans `## Modes initiaux autorisés` | STRICT_WORKERS_AUTONOMIE_ETROITE_01.md | REVIEW_DRAFT, FAST_TRIAGE, ENDPOINT_AUDIT, WRITE_GATED absents |
| `updated_at: 2026-05-31` — déjà à jour | — | OK |

## 16_TODO

```text
- PATCH_DRAFT (Step 2) : ajouter runner_writegated.py dans ## Runner validé
- PATCH_DRAFT (Step 2) : ajouter les 4 modes manquants dans ## Modes initiaux autorisés
- Après patch validé : envisager promotion status → canonical
```

## RISQUES

```text
- Deux blocs à patcher sur le même fichier → patch séquentiel recommandé
- Section ## Modes initiaux autorisés est un tableau markdown — format à préserver
```

## VERDICT_DRAFT_ONLY

```
VERDICT   = DRAFT_ONLY
worker    = big-pickle
reads     = 1
writes    = 0
pipeline  = Step 1/3 — 2 GAPs identifiés pour Step 2 (PATCH_DRAFT / kimi-k2.6)
```
