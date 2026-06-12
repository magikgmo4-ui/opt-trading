---
doc_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01_ROLLBACK_PLAN
doc_type: rollback_plan
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01
status: draft_for_review
lifecycle_stage: child_rollback_plan
parent_go_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01
topic_keys:
  - opt-trading
  - perf
  - runtime
  - rollback
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01/04_ROLLBACK_PLAN.md
point_de_reprise: "Définir le rollback documentaire avant tout sync runtime futur."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01/03_SYNC_PLAN_AND_RISKS.md
---

# 04_ROLLBACK_PLAN

## 1_PRÉ-ROLLBACK À PRÉSERVER

```text
- branche runtime actuelle de /opt/trading
- liste exacte des fichiers sales
- SHA courant
- scripts launcher PERF actuels
- stat de perf/perf.db
```

## 2_ROLLBACK SI LE FUTUR SYNC TOURNE MAL

```text
- revenir au SHA initial observé
- restaurer les fichiers sales préexistants
- revalider les launchers PERF historiques
- vérifier que perf/perf.db est toujours intacte
```

## 3_NOTE CRITIQUE

```text
Le rollback doit être préparé avant toute mutation runtime,
car /opt/trading n'est pas un simple clone jetable : c'est la surface réelle.
```

## RISKS

- À qualifier.
