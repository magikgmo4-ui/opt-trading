---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01_CANDIDATES
doc_type: duplicate_candidates
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01
updated_at: 2026-05-28
---

# 10_DUPLICATE_CANDIDATES

## B01 — tasks.index.json — statut DRAFT_ONLY

**Fichier :** `scripts/ai/workers/tasks.index.json`  
**Motif d'examen :** schema_version `0.3-draft`, status `DRAFT_ONLY`  
**Nature réelle :**
- Ce fichier est un registre de contraintes globales (not juste un index de tâches)
- Contient : `denied_inputs` (9 règles), `denied_commands` (8 règles), `global_invariants`, 10 task_types définis
- Référencé comme source d'autorité par `run_task.sh` et strict-workers
- DRAFT_ONLY = schema en cours de stabilisation, pas un fichier obsolète

**Suspect de doublon avec :** rien — unique en son genre.

---

## B02 — 22 job_packets DRAFT_ONLY

**Dossier :** `scripts/ai/workers/job_packets/`  
**Motif d'examen :** 22/30 packets en statut DRAFT_ONLY  
**Répartition réelle :**

| Groupe | Count | Statuts réels | Nature |
|---|---|---|---|
| `GO_STRICT_WORKERS_A4_NEGATIVE_*` | 5 | TEST_NEGATIVE | Tests contraintes intentionnels |
| `GO_STRICT_WORKERS_A4_POSITIVE_P6_*` | 1 | TEST_POSITIVE | Test positif intentionnel |
| `GO_STRICT_WORKERS_A4_WRITE_REEL_TEST` | 1 | WRITE_GATED | Test réel gated |
| `GO_STRICT_WORKERS_POOL_SMOKE_*` | 3 | DRAFT_ONLY | Smoke tests modèles |
| `GO_STRICT_WORKERS_*_MATRIX_01` | 6 | DRAFT_ONLY | Matrix tasks par type |
| `GO_OPT_TRADING_DOC_OPS_*` | 8 | DRAFT_ONLY | Workflow doc ops |
| `GO_DRIVE_CANARY_PACKET_01` | 1 | WRITE_GATED | Canary actif |
| `GO_STRICT_WORKERS_CHERRY_PICK_*` | 1 | DRAFT_ONLY | Cherry pick inventory |
| `GO_STRICT_WORKERS_E2E_*` | 2 | DRY_RUN / DRAFT | E2E tests |

Aucun groupe n'est un doublon d'un autre — task_types distincts, scopes distincts.

**Suspect de doublon avec :** aucun — groupes fonctionnellement distincts.

---

## B03 — orchestration contrat non connecté

**Fichier :** `scripts/ai/workers/orchestration/external_apps_orchestration_contract.json`  
**Motif d'examen :** présent mais non référencé par les workers  
**Nature réelle :**
- contract_version `0.1-draft`
- Définit input/output pour intégration apps externes
- Aucun worker Python ne l'importe (grep négatif)
- C'est un contrat forward-spec pour un GO futur

**Suspect de doublon avec :** rien — forward-spec unique.

---

## B04 — signal_processor + oauth_scope_audit sans test

**Fichiers :** `scripts/ai/workers/signal_processor.py`, `oauth_scope_audit.py`  
**Motif d'examen :** workers actifs/candidate sans test unitaire  
**Nature :** pas un problème de doublon — problème de couverture test.  
→ Hors scope dedup. Traitement : ADD_TEST batch dédié.

---

## B05 — gha_strict_workers_schedule sans test

**Fichier :** `.github/workflows/strict-workers-schedule.yml`  
**Motif d'examen :** workflow schedule sans test unitaire  
**Nature :** pas un doublon — cron audit planifié unique.  
→ Hors scope dedup. Traitement : ADD_TEST batch dédié.

---

## B06 — 8 scripts apply_desk_pro_*.sh — LEGACY PATCH

**Fichiers :**
```
scripts/apply_desk_pro_toolbox_patch.sh
scripts/apply_desk_pro_ui_inject_patch.sh
scripts/apply_desk_pro_ui_plus_patch.sh
scripts/apply_desk_pro_ui_toolbox_fix.sh
scripts/apply_desk_pro_ui_toolbox_fix_v2.sh
scripts/apply_desk_pro_ui_toolbox_fix_v3.sh
scripts/apply_desk_pro_ui_toolbox_fix_v4.sh
scripts/apply_desk_pro_ui_toolbox_final.sh
```

**Motif d'examen :** 8 scripts ciblent tous `modules/desk_pro/api/routes.py`, sans registre.  
**Nature réelle :**
- Scripts one-shot de patching UI (injection toolbox, diagnostics, logs)
- Série évolutive (fix → fix_v2 → fix_v3 → fix_v4 → final)
- La cible `routes.py` contient **déjà** le résultat (lignes 299-354 : `/desk/toolbox` présent)
- 2 commits git documentent l'application (`4e01dc4a`, `3ef76eb3`)
- Aucun consommateur Python ni Bash externe

**Classification :** LEGACY_REPLACED — patches déjà appliqués, scripts obsolètes.
