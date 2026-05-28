---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02_REGISTRY_READ_SCOPE
doc_type: registry_read_scope
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02
status: open
created_at: 2026-05-28
---

# 10_REGISTRY_READ_SCOPE

## 1_FICHIER_SOURCE

```
docs/registry/JOBS_REGISTRY.md  (v1.1 — 195 lignes — 2026-05-28)
```

Lecture seule. Aucune modification.

## 2_SECTIONS_CIBLÉES

| Section | Titre | Entrées totales | Ciblées dans ce run |
|---------|-------|----------------:|:---|
| 1 | GHA workflows | 7 | non — toutes `active` |
| 2 | AI workers entry point | 4 | `ai_models_registry` (experimental) |
| 3 | job_packets | 30 | DRAFT_ONLY (17), TEST_NEGATIVE (5 — hors scope), WRITE_GATED (1 — hors scope) |
| 4 | AI workers Python | 24 | `candidate` + `add_test` |
| 5 | OpenClaw scripts | 7 | non — toutes `active` |
| 6 | Scripts legacy patch | 8 | non — toutes `deleted` |
| 7 | Scripts opérateurs racine | 6 | `op_deploy_wrappers` (candidate) |
| — | Anomalies B01-B05 | 6 | B01, B02, B03, B04, B05 |

## 3_ENTRÉES_CIBLÉES

### 3.1 — DRAFT_ONLY job_packets (17 analysables)

| job_id | next_action actuel | Question pour gate humain |
|--------|--------------------|--------------------------|
| `jp_strict_readonly_smoke` | formalize | Prêt pour validation ? Dépendances ok ? |
| `jp_strict_pool_smoke_*` (3) | blocked_review | Qu'est-ce qui bloque ? Dépendances manquantes ? |
| `jp_doc_ops_*` (8) | blocked_review | Lesquels sont réellement utilisables ? |
| `ai_tasks_index` | active (v1.1 promu) | Hors scope — déjà promu |

Note : les 5 `TEST_NEGATIVE` (`jp_strict_a4_negative_*`) sont du matériel de test — hors scope de promotion.

### 3.2 — experimental (1 restant)

| job_id | path | Question pour gate humain |
|--------|------|--------------------------|
| `ai_models_registry` | `scripts/ai/workers/models.registry.json` | Formaliser en `candidate` ? Périmètre défini ? |

### 3.3 — candidate + add_test (5 entrées)

| job_id | risque | next_action | Question pour gate humain |
|--------|--------|-------------|--------------------------|
| `aw_signal_processor` | high | add_test | GO dédié ADD_TEST ? |
| `aw_signal_stats` | medium | add_test | Couvrable dans même batch que signal_processor ? |
| `aw_oauth_audit` | high | add_test | GO dédié ADD_TEST ? |
| `aw_localcms_sync` | medium | keep (candidate) | Promouvoir active ? Smoke ok ? |
| `aw_openclaw_mobile` | medium | keep (candidate) | Promouvoir active ? Testé ? |
| `op_deploy_wrappers` | medium | keep (candidate) | Promouvoir active ? Smoke ok ? |

### 3.4 — Anomalies B01-B05

| anomalie_id | description | Lot requis selon registry | À valider |
|-------------|-------------|--------------------------|-----------|
| B01 | tasks.index.json DRAFT_ONLY | formaliser dans dedup audit | Intégrer B01 dans `JOBS_DEDUP_AUDIT_01` ? |
| B02 | 22 job_packets DRAFT_ONLY | `GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01` | Ce GO existe-t-il encore ? Ouvert ? |
| B03 | orchestration/ contrat non connecté | dedup audit | Même lot que B02 ? |
| B04 | signal_processor + oauth_scope_audit sans test | ADD_TEST batch dédié | Ouvrir GO ADD_TEST ? |
| B05 | gha_strict_workers_schedule sans test | ADD_TEST batch dédié | Même batch que B04 ? |

## 4_CRITÈRES_DE_LECTURE

- Entrée incluse si `status IN (DRAFT_ONLY, experimental, candidate)` ET `next_action != keep (active)`.
- Entrées `deleted`, `TEST_NEGATIVE`, `TEST_POSITIVE` exclues.
- `active` sans `add_test` exclues.

## 5_RÉSULTAT_ATTENDU

Le run pilote produit :
- Un handoff contract JSON avec les entrées analysées dans `actions_planned`.
- Une proof.json + proof_summary.md dans `artifacts/automation_ops/semiauto_pilot/pilot_<run_id>/`.
- Verdict `PASS_DRY_RUN`.
- Décisions pour le gate humain documentées dans `20_RUN_REPORT.md`.
