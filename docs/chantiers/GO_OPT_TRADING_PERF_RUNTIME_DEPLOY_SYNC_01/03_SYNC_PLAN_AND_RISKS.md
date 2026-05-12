---
doc_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01_SYNC_PLAN_AND_RISKS
doc_type: sync_plan
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01
status: draft_for_review
lifecycle_stage: child_sync_plan
parent_go_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01
topic_keys:
  - opt-trading
  - perf
  - runtime
  - sync-plan
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01/03_SYNC_PLAN_AND_RISKS.md
point_de_reprise: "Définir un plan de sync runtime contrôlé sans mutation dans ce lot."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01/01_RUNTIME_GIT_DRIFT_AUDIT.md
  - docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01/02_PERF_RUNTIME_CURRENT_STATE.md
---

# 03_SYNC_PLAN_AND_RISKS

## 1_PLAN DE SYNC CONTRÔLÉ

```text
Phase 1 : figer l'état runtime actuel (présent GO)
Phase 2 : validation humaine explicite
Phase 3 : GO séparé de sync runtime avec commandes exactes
Phase 4 : après sync seulement, reprendre la preuve DB canonique runtime
```

## 2_COMMANDES QUI RESTENT INTERDITES DANS CE LOT

```text
git reset --hard
git pull
git rebase
git checkout sot/mainline
systemctl restart ...
suppression de perf/perf.db
```

## 3_RISQUES MAJEURS

| Risque | Impact |
|---|---|
| reset brutal de /opt/trading | perte de travail local non relié à PERF |
| sync aveugle sur branche sale | conflit ou état incohérent |
| relance runtime sans vérifier les launchers | preuve fausse / régression PERF |
| retrait legacy DB avant sync | casse silencieuse de l'environnement réel |

## 4_VERDICT DE PLAN

```text
PASS_PLAN
```

Le plan est clair et sûr, mais il exige une validation humaine avant toute mutation.
