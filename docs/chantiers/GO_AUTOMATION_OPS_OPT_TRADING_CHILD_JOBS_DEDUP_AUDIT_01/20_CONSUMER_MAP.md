---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01_CONSUMER_MAP
doc_type: consumer_map
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01
updated_at: 2026-05-28
---

# 20_CONSUMER_MAP

## B01 — tasks.index.json

| Consommateur | Type | Référence |
|---|---|---|
| `scripts/ai/workers/run_task.sh` | shell entry point | routing des task_types |
| `.github/workflows/strict-workers-validate.yml` | GHA | valide via `_validate_job.py` |
| `.github/workflows/strict-workers-schedule.yml` | GHA schedule | audit contraintes |

**Preuve :** `grep -r "tasks.index" scripts/ai/` → référencé dans run_task.sh.  
**Verdict consommateur :** ACTIF — utilisé en production.

---

## B02 — job_packets DRAFT_ONLY

| Consommateur | Type | Référence |
|---|---|---|
| `scripts/ai/workers/run_task.sh` | shell | lit tout packet passé en argument |
| `scripts/ai/workers/_validate_job.py` | python validator | valide le JSON de chaque packet |
| `strict-workers-validate.yml` | GHA | déclenche _validate_job.py sur les packets |

**Preuve :** `strict-workers-validate.yml` → `_validate_job.py` → `job_packets/*.json`  
**Verdict consommateur :** VALIDÉS par CI — DRAFT_ONLY = statut schema, pas absence de consommateur.

---

## B03 — orchestration contrat

| Consommateur | Résultat |
|---|---|
| `git grep "external_apps_orchestration" scripts/ai/workers/*.py` | **0 résultats** |
| `git grep "orchestration_contract" -- "*.py" "*.sh"` | **0 résultats** |
| `cat scripts/ai/workers/orchestration/README.md` | README présent — spec forward |

**Preuve :** aucun consommateur actif. Forward-spec uniquement.  
**Verdict consommateur :** AUCUN — pas un problème de doublon, candidat futur.

---

## B06 — apply_desk_pro_*.sh

| Vérification | Résultat |
|---|---|
| `git grep "apply_desk_pro" -- "*.py" "*.sh"` (hors scripts eux-mêmes) | 0 résultat Python/shell externe |
| `grep "toolbox" modules/desk_pro/api/routes.py` | PRÉSENT — lignes 299, 300, 304, 313, 321, 322, 353, 354 |
| Commits de référence | `4e01dc4a` (toolbox + hard restart), `3ef76eb3` (inject toolbox) |
| `wc -l scripts/apply_desk_pro_*.sh` | 58 / 74 / 64 / 63 / 71 / 71 / 71 / 71 lignes |

**Preuve d'obsolescence :** `routes.py` contient déjà `/desk/toolbox` endpoint + injection UI.  
Les scripts ne peuvent pas être réappliqués sans écraser l'état actuel du fichier.  
**Verdict consommateur :** ZÉRO consommateur externe — LEGACY_REPLACED confirmé.
