---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
machine: fantome
status: draft_canonical
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - strict_workers
  - clickup
  - task_tracker
  - worker
  - job_packets
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Definir le worker ClickUp task tracker : job packets READ_INVENTORY + PATCH_DRAFT, mapping API ClickUp"
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/CLICKUP_IMPLEMENTATION_BUNDLE_V1/01_SCHEMA.txt
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/execute_clickup.py
  - docs/product/guides/CLICKUP_COCKPIT.md
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
---

# GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01 — 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Definir un worker strict pour le suivi de taches GO dans ClickUp : job packets READ_INVENTORY pour lire l'etat des taches depuis ClickUp, et PATCH_DRAFT pour proposer des mises a jour de statut — via l'API ClickUp existante.

## 2_CONTEXTE

Le cockpit ClickUp existe deja (GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01, status PARTIAL) avec :
- Workspace, 4/6 Spaces crees, List GO_ACTIVE, 2 taches GO
- Script Python `execute_clickup.py` pour l'API ClickUp v2
- Schema complet (15 custom fields, 10 statuses, 5 dashboards — partiellement manuels UI)
- Guide utilisateur `CLICKUP_COCKPIT.md`

Ce worker strict vient automatiser la lecture et la proposition de mise a jour des taches GO via le runner strict_workers.

## 3_BORNES_DU_CHILD

1. **Job packets ClickUp** — 2 job packets (READ_INVENTORY, PATCH_DRAFT)
2. **Mapping runner** — le runner appelle l'API ClickUp via le script existant ou directement
3. **READ_INVENTORY** — lire les taches GO_ACTIVE depuis ClickUp, produire un rapport
4. **PATCH_DRAFT** — proposer mise a jour de statut/tache sans ecriture reelle
5. **Doc-only** — aucun write ClickUp reel sans approbation

## 4_JOB_PACKETS_PROJETES

### Job Packet 1: READ_INVENTORY — ClickUp

| Champ | Valeur |
| --- | --- |
| `job_packet_id` | `GO_STRICT_WORKERS_CLICKUP_READ_INVENTORY_01` |
| `task_type` | `READ_INVENTORY` |
| `autonomy_max` | A1 |
| `modele_prefere` | `qwen3.5-plus` (VERIFIED, A1) |
| `dry_run` | true |

**inputs :** `list_id` (defaut: GO_ACTIVE), `max_tasks` (defaut: 50)
**denied :** `write`, `delete`, `update`, `clickup:post`
**output :** `reports/ai/workers/clickup_inventory_<ts>.md`
**required_sections :** `TACHES_CLICKUP`, `STATUTS`, `VERDICT_INVENTORY`

### Job Packet 2: PATCH_DRAFT — ClickUp

| Champ | Valeur |
| --- | --- |
| `job_packet_id` | `GO_STRICT_WORKERS_CLICKUP_PATCH_DRAFT_01` |
| `task_type` | `PATCH_DRAFT` |
| `autonomy_max` | A2 |
| `modele_prefere` | `glm-5.1` (VERIFIED, A2) |
| `dry_run` | true |

**inputs :** `task_id`, `champ`, `nouvelle_valeur`, `justification`
**denied :** `clickup:write`, `clickup:delete`
**output :** `reports/ai/workers/clickup_patch_draft_<ts>.md`
**required_sections :** `TACHE_CIBLE`, `PATCH_PROPOSE`, `DIFF_ATTENDU`, `VALIDATION_EXTERNE`

## 5_INVARIANTS

```text
- Aucun token ClickUp expose
- Aucune modification du script execute_clickup.py existant
- Aucune modification de tasks.index.json ou models.registry.json
- Aucun write ClickUp reel sans approbation
- Toute sortie = DRAFT_ONLY
```

## 6_CANONICAL_STATE

```text
- Branche: go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01
- Base: sot/mainline
- Machine: fantome
- Perimetre: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01/
- Cockpit ClickUp existant: PARTIAL, etapes UI manuelles restantes
```

## 7_NEXT_GO

```text
Apres PASS: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01
- Pipeline CI/CD pour les workers stricts
```

## 8_RESUME_POINT

```text
fantome
→ STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01
→ Branche: go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01
→ Creer les job packets ClickUp (2), mapping runner, closeout
→ Doc-only, aucun write reel
```
