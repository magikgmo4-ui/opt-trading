---
doc_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_IMPL_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_IMPL_01
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01
topic_keys:
  - opt-trading
  - perf
  - runtime
  - deploy-sync
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_IMPL_01/00_CADRAGE.md
point_de_reprise: "Exécuter le réalignement contrôlé de /opt/trading avec backup et rollback."
updated_at: 2026-05-11
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/90_CLOSEOUT.md
---

# 00_CADRAGE — PERF_RUNTIME_DEPLOY_SYNC_IMPL_01

## 1_MASTER_TARGET

Exécuter le réalignement contrôlé de `/opt/trading` avec `origin/sot/mainline`, avec backup, stash, et vérification post-sync.

## 2_OPERATIONS EFFECTUEES

```text
1. backup branche pre-mutation
2. stash des fichiers sales
3. checkout origin/sot/mainline sur nouvelle branche
4. pop stash (restauration fichiers sales)
5. résolution conflit unique sur BRANCH_STATE.md (version mainline gardée)
6. vérification post-sync des launchers PERF
```

## 3_GARANTIES

```text
- backup branche conservée
- aucun reset destructif
- aucun pull/rebase aveugle
- legacy perf/perf.db non touchée
- aucun restart service
```

## RISKS

- À qualifier.
