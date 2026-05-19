# 10_REMEDIATION_BLOCKER_CLEARANCE_EXECUTION_LOG

## Objectif

Executer uniquement les commandes de clearance non-runtime prevues dans `09_REMEDIATION_BLOCKER_CLEARANCE_PLAN.md`.

## Runtime lock

```text
RUNTIME_REMAINS_BLOCKED
NO_SSH_CONNECTION_ATTEMPTED
NO_OPENCLAW_RUNTIME_EXECUTED
```

## Git precheck
```text
## go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01...origin/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
?? docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/10_REMEDIATION_BLOCKER_CLEARANCE_EXECUTION_LOG.md
b7216b1f docs: add AI team remote exec remediation blocker clearance plan
735ff080 docs: update gate validation and record remediation blockers
7688137f docs: add AI team remote exec remediation gate validation
27b67b36 docs: add AI team remote exec remediation execution plan
5ae2a3dd docs: select AI team remote exec remediation options
7d8db742 docs: add AI team remote exec remediation decision matrix
c9118c6c docs: add AI team remote exec remediation audit fiches
81bf1c17 docs: open AI team db-layer remote exec remediation child
 .../00_INITIAL_PROJECT_DOC.md                      |  160 ++
 .../01_IDENTITY_AUDIT.md                           |   43 +
 .../02_SANDBOX_AUDIT.md                            |   43 +
 .../03_SSH_ALIAS_AUDIT.md                          |   43 +
 .../04_REMEDIATION_DECISION_MATRIX.md              |   63 +
 .../05_REMEDIATION_SELECTED_OPTIONS.md             |   90 +
 .../06_REMEDIATION_EXECUTION_PLAN.md               |  253 +++
 .../07_GATE_PROOF_LOCAL_OUTPUT.txt                 | 2165 ++++++++++++++++++++
 .../07_REMEDIATION_GATE_VALIDATION.md              |  157 ++
 .../08_REMEDIATION_BLOCKER_REPORT.md               |  126 ++
 .../09_REMEDIATION_BLOCKER_CLEARANCE_PLAN.md       |  206 ++
 11 files changed, 3349 insertions(+)
```

## Identity clearance — before
```text
uid=1001(openclaw) gid=1001(openclaw) groupes=1001(openclaw),125(docker)
openclaw:x:1001:1001::/home/openclaw:/bin/bash
drwxrwxrwx 23 openclaw docker 4096 Mar 14 08:22 /home/openclaw
```

## Identity clearance — action
```text
Creating /home/openclaw/.ssh if absent, no key copied, no secret written.
```

## Identity clearance — after
```text
drwxrwxrwx 24 openclaw docker   4096 May 12 00:20 /home/openclaw
drwx------  2 openclaw openclaw 4096 May 12 00:20 /home/openclaw/.ssh
-rw------- 1 openclaw openclaw 0 May 12 00:20 /home/openclaw/.ssh/config
```

## Sandbox clearance — config discovery
```text
./docs/governance/WHY_ENFORCEMENT_POLICY_01.md
./docs/governance/NAMING_CANON_POLICY_01.md
./docs/governance/REPO_ROOT_POLICY.md
./docs/governance/WHY_LINT_POLICY_01.md
./docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_RESULT_V1.txt
./docs/hermes/GO_HERMES_OPENCLAW_BRIDGE_05_EXEC_01.md
./docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_RESULT_2026-04-09.txt
./docs/hermes/03_bridge_openclaw.md
./docs/hermes/GO_HERMES_OPENCLAW_BRIDGE_05.md
./docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_RESULT_TEMPLATE.txt
./docs/hermes/HERMES_OPENCLAW_BRIDGE_RUNBOOK_V1.md
./docs/hermes/HERMES_OPENCLAW_BRIDGE_05_CLOSEOUT_2026-04-09.md
./docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_PROMPT.txt
./docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_V1.md
./docs/ui_screenshots/02_archive_policy.md
./docs/product_targets/OPENCLAW_TARGET_CANON.md
./docs/index/inbox/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01.md
./docs/index/inbox/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01.md
./docs/index/inbox/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04_RETRY.md
./docs/index/inbox/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01.md
./docs/index/inbox/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01.md
./docs/index/inbox/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01.md
./docs/chantiers/GO_GIT_OPENCLAW_STATE_DIR_REPAIR_10_CLASSIFICATION_01
./docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/06_DECISION_LAB_STUDENT_OPENCLAW_ORCHESTRATION.md
./docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/30_OPENCLAW_LAB_DEFERRED_BOUNDARY.md
./docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01
./docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_SCORE_GENERATOR_01/60_WHY_SCORE_FALSE_CONFIDENCE_POLICY.md
./docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01
./docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01
./docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01
./docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01
./docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01/30_OPENCLAW_E2E_COMMAND_DISCOVERY.md
./docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01
./docs/chantiers/GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01
./docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/17_step_05_family_plan_openclaw.md
./docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/05_step_02_hygiene_documentaire_batch2_openclaw.md
./docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
./docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01
./docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
./docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01.md
./docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01.md
./docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_REALIGN_01
./docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_WORKER_AUDIT_01/70_WHY_WORKER_HUMAN_REVIEW_POLICY.md
./docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01
./docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/03_OPENCLAW_WORKER_ORCHESTRATION_RULES.md
./docs/chantiers/GO_GIT_OPENCLAW_STATE_DIR_READ_09_CLASSIFICATION_01
./docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04_RETRY
./docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/40_PHASE_4_OPENCLAW_SKILL_INTEGRATION.md
./docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
./docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01
./docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_MARKDOWN_PARSER_01/60_WHY_PARSER_FALSE_POSITIVE_POLICY.md
./docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/10_CROSS_CHANTIERS_OPENCLAW_TMUX_AGENTS_REVIEW.md
./docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
./docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/02_SANDBOX_AUDIT.md
./docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01
./docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/ide_bundle/02_PROMPT_IMPL_OPENCLAW_GATEWAY.md
./docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/04_api_contract_openclaw_gateway.md
./docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01
./docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md
./docs/ot/trae/05_RUNTIME_MCP_POLICY_V1.txt
./docs/ot/trae/06_REPO_BOUNDARY_POLICY_V1.txt
./docs/ot/trae/trae_pack_texts/trae_pack/TRAE_STATUS_POLICY_V1.1.txt
./docs/ot/trae/OT_TRAE_MCP_POLICY_PRE_V1_GEL_DECISION_01.md
./docs/ot/closings/OT_TRAE_MCP_POLICY_V1_01_CLOSING.txt
./docs/ot/closings/PROJECT_CARD_OPENCLAW_01_CLOSING.txt
./docs/product/guides/OPENCLAW_RUNTIME.md
./docs/product/guides/OPENCLAW_DOCS_LIBRARY.md
./adapter_botpress_openclaw.py
./.git/refs/heads/fix/openclaw-script-modes-01
./.git/refs/heads/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01
./.git/refs/heads/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01
./.git/refs/heads/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01
./.git/refs/heads/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01
./.git/refs/heads/go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_DOC_REALIGN_01
./.git/refs/heads/go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
./.git/refs/heads/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
./.git/refs/heads/doc/GO_OPENCLAW_STATE_DIR_READ_09
./.git/refs/heads/doc/GO_OPENCLAW_USAGE_EXAMPLES_09
./.git/refs/heads/doc/GO_OPENCLAW_STATE_DIR_REPAIR_10
./.git/refs/heads/doc/GO_OPENCLAW_INFRA_BASELINE_01
./.git/refs/remotes/origin/docs/tmux-opencode-openclaw-runtime-01
./.git/refs/remotes/origin/feat/project-card-openclaw-01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_NETWORK_DIAG_01
./.git/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01
./.git/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01
./.git/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_03
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_LOCAL_OLLAMA_BINDING_SMOKE_01
./.git/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_DOC_REALIGN_01
./.git/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_SWITCH_DRYRUN_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_SCOPE_VALIDATION_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_DRYRUN_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_AUTHORIZATION_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_TIMEOUT_TUNING_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_ROUTING_AUDIT_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LIVE_ARTIFACTS_01
./.git/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
./.git/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
./.git/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_SOURCE_PROOF_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_GATEWAY_SESSION_FIX_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_01_RETRY
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04_RETRY
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_CLOSEOUT_01
./.git/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_SWITCH_APPLY_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_MODEL_EVALUATION_01
./.git/refs/remotes/origin/go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
./.git/refs/remotes/origin/go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_APPLY_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01
./.git/refs/remotes/origin/go/GO_OPENCLAW_STATE_DIR_REPAIR_10
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01
./.git/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_DISK_FIX_01
./.git/refs/remotes/origin/doc/GO_OPENCLAW_INFRA_BASELINE_01
./.git/logs/refs/heads/fix/openclaw-script-modes-01
./.git/logs/refs/heads/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01
./.git/logs/refs/heads/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01
./.git/logs/refs/heads/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01
./.git/logs/refs/heads/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01
./.git/logs/refs/heads/go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_DOC_REALIGN_01
./.git/logs/refs/heads/go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
./.git/logs/refs/heads/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
./.git/logs/refs/heads/doc/GO_OPENCLAW_STATE_DIR_READ_09
./.git/logs/refs/heads/doc/GO_OPENCLAW_USAGE_EXAMPLES_09
./.git/logs/refs/heads/doc/GO_OPENCLAW_STATE_DIR_REPAIR_10
./.git/logs/refs/heads/doc/GO_OPENCLAW_INFRA_BASELINE_01
./.git/logs/refs/remotes/origin/docs/tmux-opencode-openclaw-runtime-01
./.git/logs/refs/remotes/origin/feat/project-card-openclaw-01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_NETWORK_DIAG_01
./.git/logs/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01
./.git/logs/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01
./.git/logs/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_03
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_LOCAL_OLLAMA_BINDING_SMOKE_01
./.git/logs/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_DOC_REALIGN_01
./.git/logs/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_SWITCH_DRYRUN_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_SCOPE_VALIDATION_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_DRYRUN_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_AUTHORIZATION_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_TIMEOUT_TUNING_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_ROUTING_AUDIT_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LIVE_ARTIFACTS_01
./.git/logs/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
./.git/logs/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
./.git/logs/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_SOURCE_PROOF_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_GATEWAY_SESSION_FIX_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_01_RETRY
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04_RETRY
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_CLOSEOUT_01
./.git/logs/refs/remotes/origin/go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_SWITCH_APPLY_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_MODEL_EVALUATION_01
./.git/logs/refs/remotes/origin/go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
./.git/logs/refs/remotes/origin/go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_APPLY_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01
./.git/logs/refs/remotes/origin/go/GO_OPENCLAW_STATE_DIR_REPAIR_10
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01
./.git/logs/refs/remotes/origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_DISK_FIX_01
./.git/logs/refs/remotes/origin/doc/GO_OPENCLAW_INFRA_BASELINE_01
./scripts/reseau_ssh/windows/firewall_allow_lan.ps1
./modules/model_provider_openclaw
./modules/model_provider_openclaw/docs/GO_OPENCLAW_ALIGNMENT_EXCEPTION_08.md
./modules/model_provider_openclaw/docs/GO_OPENCLAW_PROVIDER_POLICY_04.md
./modules/model_provider_openclaw/docs/GO_OPENCLAW_ALIGNMENT_DECISION_07.md
./modules/model_provider_openclaw/docs/GO_OPENCLAW_ALIGNMENT_READ_06.md
./modules/model_provider_openclaw/docs/GO_OPENCLAW_POLICY_RUNTIME_ALIGNMENT_05.md
./modules/model_provider_openclaw/docs/model_provider_openclaw.doc.md
./modules/model_provider_openclaw/app/model_provider_openclaw.py
./modules/model_provider_openclaw/config/providers_policy.yaml
./modules/openclaw_config_modulaire
./modules/openclaw_config_modulaire/app/openclaw_root_template.json5
./modules/evidence_openclaw
./modules/evidence_openclaw/docs/GO_OPENCLAW_STATE_DIR_VIGILANCE_03.md
./modules/evidence_openclaw/docs/GO_OPENCLAW_SYNC_02.md
./modules/evidence_openclaw/docs/GO_OPENCLAW_EVIDENCE_01.md
./modules/doctor_openclaw
./modules/install_module_openclaw.bak_20260314
./modules/tradingview_observer_openclaw
./modules/gateway_openclaw
./modules/install_module_openclaw
./modules/configure_openclaw
./modules/menu_openclaw
./modules/menu_openclaw/docs/GO_OPENCLAW_INFRA_BASELINE_01.md
./modules/menu_openclaw/docs/GO_OPENCLAW_USAGE_EXAMPLES_09.md
./modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md
./modules/menu_openclaw/docs/GO_OPENCLAW_STATE_DIR_READ_09.md
./modules/menu_openclaw/docs/GO_OPENCLAW_STATE_DIR_REPAIR_10
./bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01
./bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/prompts/GO_PROMPT_04_OPENAI_COMPAT_OPENCLAW.md
```

## SSH alias clearance — non-connective resolution
```text
host fantome
user fantome
hostname 192.168.0.191
port 22
addressfamily any
batchmode no
canonicalizefallbacklocal yes
canonicalizehostname false
checkhostip no
compression no
controlmaster false
enablesshkeysign no
clearallforwardings no
exitonforwardfailure no
fingerprinthash SHA256
forwardx11 no
forwardx11trusted yes
gatewayports no
gssapiauthentication yes
gssapikeyexchange no
gssapidelegatecredentials no
gssapitrustdns no
gssapirenewalforcesrekey no
gssapikexalgorithms gss-group14-sha256-,gss-group16-sha512-,gss-nistp256-sha256-,gss-curve25519-sha256-,gss-group14-sha1-,gss-gex-sha1-
hashknownhosts yes
hostbasedauthentication no
identitiesonly yes
kbdinteractiveauthentication yes
nohostauthenticationforlocalhost no
passwordauthentication yes
permitlocalcommand no
proxyusefdpass no
pubkeyauthentication true
requesttty auto
sessiontype default
stdinnull no
forkafterauthentication no
streamlocalbindunlink no
stricthostkeychecking ask
tcpkeepalive yes
tunnel false
verifyhostkeydns false
visualhostkey no
updatehostkeys true
enableescapecommandline no
canonicalizemaxdots 1
connectionattempts 1
forwardx11timeout 1200
numberofpasswordprompts 3
serveralivecountmax 3
serveraliveinterval 30
requiredrsasize 1024
obscurekeystroketiming yes
ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com
hostkeyalgorithms ssh-ed25519-cert-v01@openssh.com,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
hostbasedacceptedalgorithms ssh-ed25519-cert-v01@openssh.com,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
kexalgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,diffie-hellman-group14-sha256
casignaturealgorithms ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
loglevel INFO
macs umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1
securitykeyprovider internal
pubkeyacceptedalgorithms ssh-ed25519-cert-v01@openssh.com,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,sk-ecdsa-sha2-nistp256-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256
xauthlocation /usr/bin/xauth
identityfile ~/.ssh/id_ed25519
identityfile ~/.ssh/id_ed25519_fantome
canonicaldomains none
globalknownhostsfile /etc/ssh/ssh_known_hosts /etc/ssh/ssh_known_hosts2
userknownhostsfile /home/ghost/.ssh/known_hosts /home/ghost/.ssh/known_hosts2
sendenv LANG
sendenv LC_*
logverbose none
channeltimeout none
permitremoteopen any
addkeystoagent false
forwardagent no
connecttimeout none
tunneldevice any:any
canonicalizePermittedcnames none
controlpersist no
escapechar ~
ipqos lowdelay throughput
rekeylimit 0 0
streamlocalbindmask 0177
syslogfacility USER
```

## Runtime status
```text
No OpenClaw runtime executed.
No SSH connection attempted.
Only ssh -G local config expansion executed.
```
