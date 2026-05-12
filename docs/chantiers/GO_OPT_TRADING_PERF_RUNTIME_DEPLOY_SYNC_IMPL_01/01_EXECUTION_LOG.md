---
doc_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_IMPL_01_EXECUTION_LOG
doc_type: execution_log
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
  - sync-execution
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_IMPL_01/01_EXECUTION_LOG.md
point_de_reprise: "Log d'exécution du sync runtime /opt/trading."
updated_at: 2026-05-11
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_IMPL_01/00_CADRAGE.md
---

# 01_EXECUTION_LOG

## PRE-SYNC STATE

```text
branch  : go/GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
SHA     : f4aaa196cf17c41a93eb8344997e40eab9d9e25c
behind  : 232 commits vs origin/sot/mainline
dirty   : 8 fichiers (REPO_KG, non PERF)
```

## BACKUP

```text
branch backup : backup/pre-perf-sync-20260511_232839
SHA           : f4aaa196cf17c41a93eb8344997e40eab9d9e25c
```

## OPERATIONS

```text
1. git stash push des 8 fichiers sales
2. git checkout -b go/PERF-RUNTIME-SYNC-20260511_232938 origin/sot/mainline
3. git stash pop → conflit unique sur docs/index/BRANCH_STATE.md
4. git checkout --theirs docs/index/BRANCH_STATE.md → résolution
5. git stash drop
```

## POST-SYNC STATE

```text
branch  : go/PERF-RUNTIME-SYNC-20260511_232938
SHA     : 5fce30a (dernier origin/sot/mainline)
behind  : 0
dirty   : 8 fichiers (REPO_KG, inchangés vs pre-sync)
```

## PERF LAUNCHERS VERIFICATION

```text
scripts/desk_pro_ui_toolbox_fix_cmd.sh   → modules.perf.app:app ✓
scripts/desk_pro_ui_toolbox_final_cmd.sh → modules.perf.app:app ✓
modules/simex_bitget_bridge/cmd.sh       → modules.perf.app:app ✓
```

## DB PATHS POST-SYNC

```text
modules/perf/data/         → présent (README.md)
modules/perf/data/perf.db  → absent (à créer par relocate tool)
perf/perf.db               → présent (36864 bytes, mtime 2026-04-09)
```

## ROLLBACK COMMAND

```text
git checkout backup/pre-perf-sync-20260511_232839
```
