# 02 — Inventory Menus / Cmd / Sanity (first pass)

## Source
Derived from `find modules -type f \( -name 'menu.sh' -o -name 'cmd.sh' -o -name 'sanity_check.sh' \)` in the raw inventory log.

## Main finding
A large number of modules already follow the standard internal structure:
- `scripts/cmd.sh`
- `scripts/menu.sh`
- `scripts/sanity_check.sh`

This is true for most Desk Pro business modules, including:
- `decision_engine`
- `derivatives_analyzer`
- `derivatives_collector`
- `desk_pro_dashboard`
- `desk_pro_orchestrator`
- `desk_pro_runner`
- `execution_engine`
- `journal_engine`
- `liquidation_analyzer`
- `market_scanner`
- `opportunity_ranker`
- `portfolio_engine`
- `position_engine`
- `probability_engine`
- `risk_engine`

## Operational implication
The internal module structure exists for most core components. The current bottleneck is therefore not script absence inside modules, but missing or inconsistent global exposure for operators.

## Notable anomalies to review later
- `modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/sanity_check.sh`
- `modules/reseau_ssh_step2/modules/reseau_ssh/reseau_ssh_step2/scripts/sanity_check.sh`
- `modules/scripts/scripts/...`
- standalone top-level `sanity_check.sh` files inside some repo hygiene modules in addition to `scripts/sanity_check.sh`

These do not need cleanup in this phase, but they confirm structural debt / historical layering.

## First-pass menu classification
### Operator-facing candidates
- `desk_pro_dashboard`
- `desk_pro_orchestrator`
- `desk_pro_runner`
- `desk_analyze`
- `desk_capture_inputs`
- `desk_state`
- `market_scanner`
- `probability_engine`
- `risk_engine`
- `position_engine`
- `portfolio_engine`

### Dev / engine-facing candidates
- `decision_engine`
- `execution_engine`
- `derivatives_collector`
- `derivatives_analyzer`
- `liquidation_analyzer`
- `opportunity_ranker`
- `journal_engine`

### Maintenance / infra-facing candidates
- `install_module`
- `ops_menu_hub`
- `ops_super_menu`
- `ops_wrappers`
- `repo_hygiene`
- `repo_local_artifacts`
- `repo_ownership_guard`
- `shared_files_sftp`
- `shared_sshfs_permanent`
- `reseau_ssh*`
- `winscp_transfer`

## Key finding
Most core modules already meet the internal menu/cmd/sanity standard. The next packaging task should target the operator surface in `/usr/local/bin`, not module-internal script creation.
