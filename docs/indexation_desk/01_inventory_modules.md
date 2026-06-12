# 01 — Inventory Modules (first pass)

## Scope
First-pass module inventory derived from:
- `/opt/trading/_work/indexation_desk/raw_inventory_20260307_054013.log`
- current `admin-trading` repo state

This file is a structured synthesis, not the final exhaustive module-by-module catalog.

## Core Desk Pro chain already present
The following business modules are present in the repo and form the current Desk Pro core chain:
- `modules/derivatives_collector`
- `modules/derivatives_analyzer`
- `modules/liquidation_analyzer`
- `modules/probability_engine`
- `modules/decision_engine`
- `modules/risk_engine`
- `modules/execution_engine`
- `modules/position_engine`
- `modules/portfolio_engine`
- `modules/journal_engine`
- `modules/market_scanner`
- `modules/opportunity_ranker`
- `modules/desk_pro_dashboard`
- `modules/desk_pro_orchestrator`
- `modules/desk_pro_runner`

## Desk / state / ingestion support layer
- `modules/desk_analyze`
- `modules/desk_capture_inputs`
- `modules/desk_common`
- `modules/desk_retention`
- `modules/desk_snapshot_ingest`
- `modules/desk_state`
- `modules/desk_pro`

## Vision / webhook / runtime support
- `modules/bot_vision`
- `modules/bot_vision_step2`
- `modules/webhook`
- `modules/perf`
- `modules/perf_engine`
- `modules/router`
- `modules/marketdata`

## Ops / wrappers / workflow support
- `modules/ops_menu_hub`
- `modules/ops_super_menu`
- `modules/ops_wrappers`
- `modules/install_module`
- `modules/env`
- `modules/repo_hygiene`
- `modules/repo_local_artifacts`
- `modules/repo_ownership_guard`
- `modules/workflow_post_change_v2` (ACTIVE/PATCHED - Canonique)
- `modules/workflow_post_change_v2_fix1` (DEPRECATED/OBSOLETE)
- `modules/workflow_post_change_v2_fix2` (DEPRECATED/OBSOLETE)
- `modules/workflow_post_change_v2_fix3` (DEPRECATED/MERGED into v2)

## Network / shared / infra modules
- `modules/shared_files_sftp`
- `modules/shared_sshfs_permanent`
- `modules/reseau_ssh`
- `modules/reseau_ssh_step1b`
- `modules/reseau_ssh_step2`
- `modules/winscp_transfer`

## Student / DeepSeek line
Stable reference remains separate and should not be reopened except regression:
- `modules/deepseek_hub`
- `modules/deepseek_response`
- `modules/deepseek_student`
- `modules/deepseek_thinking`
- `modules/perm_fix_student`

## First-pass status classification
### Stable / recently advanced
- `derivatives_analyzer`
- `probability_engine`
- `desk_pro_dashboard`
- `desk_pro_orchestrator`
- `desk_pro_runner`
- `shared_sshfs_permanent`
- student DeepSeek pack (`ee19c7e` reference)

### Active core chain (needs operator packaging review)
- `decision_engine`
- `risk_engine`
- `execution_engine`
- `position_engine`
- `portfolio_engine`
- `journal_engine`
- `market_scanner`
- `opportunity_ranker`
- `liquidation_analyzer`
- `derivatives_collector`

### Historical / transitional / cleanup-later candidates
- `workflow_post_change_v2_fix1`
- `workflow_post_change_v2_fix2`
- `workflow_post_change_v2_fix3`
- nested step modules under `reseau_ssh_step1b` and `reseau_ssh_step2`
- `modules/scripts`

## Key finding
The repo already contains most of the Desk Pro building blocks. The primary issue is not missing engines, but uneven operator exposure, naming consistency, and packaging across wrappers / menus / sanity entrypoints.

## RISKS

- À qualifier.
