---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02_RUN_REPORT
doc_type: run_report
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02
run_id: pilot_634561cf
verdict: PASS_DRY_RUN
status: GATE_HUMAIN_REQUIS
created_at: 2026-05-28
---

# 20_RUN_REPORT

## 1_VERDICT_RUN

```
run_id  : pilot_634561cf
verdict : PASS_DRY_RUN
mode    : dry_run
gate    : human_gate_required = true
```

## 2_ACTIONS_EXÉCUTÉES_VS_PLANIFIÉES

| Action planifiée | Exécutée par pilot_runner | Note |
|-----------------|:-------------------------:|------|
| read docs/registry/JOBS_REGISTRY.md | non | gap G02 — délégation opérateur |
| identify DRAFT_ONLY job_packets | non | gap G02 |
| identify experimental entries | non | gap G02 |
| identify candidate+add_test entries | non | gap G02 |
| analyse anomalies B01-B05 | non | gap G02 |
| propose next_action par entrée | non | gap G02 |
| write proof artifacts | oui | proof_634561cf présente |
| submit to human gate | oui | ce document |

> Gap G02 (REAL_CASE_01) confirmé : le pilot_runner ne sait pas encore exécuter les actions
> planifiées. Les actions de lecture et d'analyse sont réalisées par l'opérateur et documentées
> ci-dessous.

## 3_ANALYSE_REGISTRY — RÉSULTATS_OPÉRATEUR

### 3.1 — DRAFT_ONLY job_packets (17 analysables)

| job_id | next_action actuel | Décision proposée |
|--------|--------------------|-------------------|
| `jp_strict_readonly_smoke` | formalize | Intégrer dans `JOBS_DEDUP_AUDIT_01` — vérifier dépendances et formaliser |
| `jp_strict_pool_smoke_*` (3) | blocked_review | Intégrer dans `JOBS_DEDUP_AUDIT_01` — identifier le blocage |
| `jp_doc_ops_*` (8) | blocked_review | Intégrer dans `JOBS_DEDUP_AUDIT_01` — qualifier utilisable vs deprecated |

Les 5 `TEST_NEGATIVE` (`jp_strict_a4_negative_*`) sont du matériel de test — hors scope.

### 3.2 — experimental (1)

| job_id | Décision proposée |
|--------|-------------------|
| `ai_models_registry` | Ouvrir un GO court pour formaliser le périmètre et promouvoir `candidate` |

### 3.3 — candidate + add_test (6)

| job_id | risque | Décision proposée |
|--------|--------|-------------------|
| `aw_signal_processor` | high | Inclure dans ADD_TEST batch — ne pas promouvoir `active` sans tests |
| `aw_signal_stats` | medium | Même batch ADD_TEST que signal_processor |
| `aw_oauth_audit` | high | GO ADD_TEST séparé (risque high — traiter seul) |
| `aw_localcms_sync` | medium | Smoke test puis promouvoir `active` si PASS |
| `aw_openclaw_mobile` | medium | Smoke test puis promouvoir `active` si PASS |
| `op_deploy_wrappers` | medium | Smoke test puis promouvoir `active` si PASS |

### 3.4 — Anomalies B01-B05

| anomalie_id | Décision proposée |
|-------------|-------------------|
| B01 | Bundler dans `JOBS_DEDUP_AUDIT_01` |
| B02 | `JOBS_DEDUP_AUDIT_01` — lot principal (22 packets) |
| B03 | `JOBS_DEDUP_AUDIT_01` — qualifier connexion orchestration |
| B04 | GO ADD_TEST batch : `aw_signal_processor` + `aw_signal_stats` + `gha_strict_workers_schedule` |
| B05 | Même batch ADD_TEST que B04 |

## 4_GATE_HUMAIN — DÉCISIONS_REQUISES

```
STATUS : EN_ATTENTE_OPÉRATEUR
```

| # | Question | Décision opérateur |
|---|----------|--------------------|
| D1 | Confirmer lancement `JOBS_DEDUP_AUDIT_01` pour B01-B03 + DRAFT_ONLY (17 packets) ? | [ ] OUI / [ ] NON |
| D2 | Ouvrir GO ADD_TEST batch pour B04+B05 (`signal_processor`, `signal_stats`, `gha_schedule`) ? | [ ] OUI / [ ] NON |
| D3 | Ouvrir GO séparé pour `aw_oauth_audit` (high risk) ? | [ ] OUI / [ ] NON |
| D4 | Formaliser `ai_models_registry` dans un GO court ? | [ ] OUI / [ ] NON |
| D5 | Smoke + promouvoir `aw_localcms_sync`, `aw_openclaw_mobile`, `op_deploy_wrappers` ? | [ ] OUI / [ ] NON |

## 5_DIFF_CHECK

```bash
# Vérification : JOBS_REGISTRY.md non modifié
git diff docs/registry/JOBS_REGISTRY.md
# Attendu : aucune sortie (diff vide)
```
