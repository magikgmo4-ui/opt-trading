---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01_DECISIONS
doc_type: decision_table
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01
updated_at: 2026-05-28
---

# 30_DECISION_TABLE

## Table de décision

| anomalie_id | cible | classification | verdict | action | next_go |
|---|---|---|---|---|---|
| B01 | `tasks.index.json` | FALSE_POSITIVE | KEEP | FORMALIZE_STATUS — passer `status: active` après review schema | — (mise à jour JOBS_REGISTRY) |
| B02 | 22 job_packets DRAFT_ONLY | FALSE_POSITIVE | KEEP | FORMALIZE_SCHEMA — les DRAFT_ONLY sont des candidats en attente d'un GO dédié | GO_SEMIAUTO_LOOP_PROTOCOL_01 ou batch dédié |
| B03 | orchestration contrat | FALSE_POSITIVE | KEEP_CANDIDATE | Aucun consommateur — forward-spec. Revisiter quand intégration externe prouvée | — |
| B04 | signal_processor + oauth | NOT_DEDUP | ADD_TEST | ADD_TEST batch dédié hors scope | batch test lock automation |
| B05 | gha_strict_workers_schedule | NOT_DEDUP | ADD_TEST | ADD_TEST batch dédié hors scope | batch test lock automation |
| B06 | 8 scripts apply_desk_pro_*.sh | LEGACY_REPLACED | DELETE_AFTER_PROOF | Preuve établie : routes.py déjà patché. Suppression dans batch dédié. | GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01 |

---

## Détail B06 — plan de suppression

**Preuve établie :**
- `modules/desk_pro/api/routes.py:299-354` contient déjà le toolbox endpoint + injection UI
- 0 consommateur externe des 8 scripts
- Commits d'application documentés : `4e01dc4a`, `3ef76eb3`

**Scripts à supprimer (batch dédié) :**
```text
scripts/apply_desk_pro_toolbox_patch.sh
scripts/apply_desk_pro_ui_inject_patch.sh
scripts/apply_desk_pro_ui_plus_patch.sh
scripts/apply_desk_pro_ui_toolbox_fix.sh
scripts/apply_desk_pro_ui_toolbox_fix_v2.sh
scripts/apply_desk_pro_ui_toolbox_fix_v3.sh
scripts/apply_desk_pro_ui_toolbox_fix_v4.sh
scripts/apply_desk_pro_ui_toolbox_final.sh
```

**Rollback :** `git revert <commit>` — les scripts seront restaurés, mais inutiles car routes.py est déjà patché.

---

## Mise à jour JOBS_REGISTRY requise

Après ce GO, mettre à jour `docs/registry/JOBS_REGISTRY.md` :

| Entrée | Changement |
|---|---|
| `ai_tasks_index` | statut `experimental` → `active` (après revue formelle) |
| `jp_*` (22 DRAFT) | clarifier `experimental` dans registry avec note "pending formal GO" |
| B06 scripts | ajouter 8 entrées avec `status: deprecated`, `next_action: delete_after_proof` |

---

## Verdict global

```text
B01-B05 : FALSE_POSITIVE ou NOT_DEDUP — aucune suppression.
B06 : LEGACY_REPLACED — 8 scripts prêts à supprimer dans batch dédié.
JOBS_REGISTRY_UPDATE requis.
```
