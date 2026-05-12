# 11_REMEDIATION_SANDBOX_CONFIG_AUDIT

## Objectif

Auditer en lecture seule les surfaces candidates de configuration sandbox/OpenClaw.

## Etat avant audit

| Gate | Status |
|:-----|:-------|
| identity | VALIDATED_PROVISIONING_READY |
| SSH alias | VALIDATED_NON_CONNECTIVE |
| sandbox | BLOCKED |

## Runtime lock

```text
RUNTIME_REMAINS_BLOCKED
READ_ONLY_AUDIT_ONLY
NO_CONFIG_MODIFICATION
NO_OPENCLAW_RUNTIME
```

## Git precheck
```text
## go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01...origin/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
?? docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/11_REMEDIATION_SANDBOX_CONFIG_AUDIT.md
7e94bc24 docs: record AI team remote exec remediation clearance execution
b7216b1f docs: add AI team remote exec remediation blocker clearance plan
735ff080 docs: update gate validation and record remediation blockers
7688137f docs: add AI team remote exec remediation gate validation
27b67b36 docs: add AI team remote exec remediation execution plan
5ae2a3dd docs: select AI team remote exec remediation options
7d8db742 docs: add AI team remote exec remediation decision matrix
c9118c6c docs: add AI team remote exec remediation audit fiches
81bf1c17 docs: open AI team db-layer remote exec remediation child
fb483203 Merge pull request #297 from magikgmo4-ui/go/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
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
 ..._REMEDIATION_BLOCKER_CLEARANCE_EXECUTION_LOG.md |  363 ++++
 12 files changed, 3712 insertions(+)
```

## Candidate tree — modules/openclaw_config_modulaire
```text
modules/openclaw_config_modulaire/docs/README.md
modules/openclaw_config_modulaire/README.md
modules/openclaw_config_modulaire/app/openclaw_root_template.json5
modules/openclaw_config_modulaire/app/tools.json5
modules/openclaw_config_modulaire/app/agents.json5
modules/openclaw_config_modulaire/scripts/rollback.sh
modules/openclaw_config_modulaire/scripts/install_shortcuts.sh
modules/openclaw_config_modulaire/scripts/cmd.sh
modules/openclaw_config_modulaire/scripts/menu.sh
modules/openclaw_config_modulaire/scripts/sanity.sh
modules/openclaw_config_modulaire/scripts/apply_safe.sh
```

## Candidate content scan — modules/openclaw_config_modulaire
```text
modules/openclaw_config_modulaire/README.md:13:- `scripts/cmd.sh` : `status`, `backup`, `apply`, `validate`, `health`, `probe`, `rollback`, `paths`
modules/openclaw_config_modulaire/app/openclaw_root_template.json5:35:  commands: {
modules/openclaw_config_modulaire/app/openclaw_root_template.json5:59:      denyCommands: [],
modules/openclaw_config_modulaire/app/tools.json5:4:  deny: [
modules/openclaw_config_modulaire/app/agents.json5:19:    sandbox: {
modules/openclaw_config_modulaire/app/agents.json5:22:      scope: "agent",
modules/openclaw_config_modulaire/app/agents.json5:42:        allow: [
modules/openclaw_config_modulaire/app/agents.json5:52:        allowAgents: ["builder", "reviewer", "lab"],
modules/openclaw_config_modulaire/app/agents.json5:64:        deny: [
modules/openclaw_config_modulaire/app/agents.json5:74:        allowAgents: [],
modules/openclaw_config_modulaire/app/agents.json5:86:        allow: [
modules/openclaw_config_modulaire/app/agents.json5:89:        deny: [
modules/openclaw_config_modulaire/app/agents.json5:98:        allowAgents: [],
modules/openclaw_config_modulaire/app/agents.json5:110:        deny: [
modules/openclaw_config_modulaire/app/agents.json5:120:        allowAgents: [],
modules/openclaw_config_modulaire/scripts/install_shortcuts.sh:7:exec "$BASE/scripts/menu.sh" "\$@"
modules/openclaw_config_modulaire/scripts/install_shortcuts.sh:11:exec "$BASE/scripts/cmd.sh" "\$@"
modules/openclaw_config_modulaire/scripts/cmd.sh:19:  cmd.sh paths
modules/openclaw_config_modulaire/scripts/cmd.sh:56:  paths)
modules/openclaw_config_modulaire/scripts/menu.sh:17:  echo "8) paths"
modules/openclaw_config_modulaire/scripts/menu.sh:28:    8) "$CMD" paths ;;
modules/openclaw_config_modulaire/scripts/sanity.sh:10:command -v openclaw >/dev/null 2>&1 || fail "openclaw non trouvé dans PATH"
modules/openclaw_config_modulaire/scripts/sanity.sh:17:import json, pathlib, sys
modules/openclaw_config_modulaire/scripts/sanity.sh:18:cfg = pathlib.Path.home()/'.openclaw'/'openclaw.json'
modules/openclaw_config_modulaire/scripts/apply_safe.sh:27:import json, pathlib
modules/openclaw_config_modulaire/scripts/apply_safe.sh:28:cfg = pathlib.Path.home()/'.openclaw'/'openclaw.json'
modules/openclaw_config_modulaire/scripts/apply_safe.sh:40:from pathlib import Path
```

## System candidates — /etc/openclaw
```text
(empty or absent)
(no matches)
```

## User candidates — /home/openclaw/.config/openclaw
```text
(empty or absent)
(no matches)
```

## Repo-wide focused scan — specific filenames
```text
### scripts
scripts/reseau_ssh/windows/firewall_allow_lan.ps1

### docs
docs/governance/WHY_ENFORCEMENT_POLICY_01.md
docs/governance/NAMING_CANON_POLICY_01.md
docs/governance/REPO_ROOT_POLICY.md
docs/governance/WHY_LINT_POLICY_01.md
docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_RESULT_V1.txt
docs/hermes/GO_HERMES_OPENCLAW_BRIDGE_05_EXEC_01.md
docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_RESULT_2026-04-09.txt
docs/hermes/03_bridge_openclaw.md
docs/hermes/GO_HERMES_OPENCLAW_BRIDGE_05.md
docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_RESULT_TEMPLATE.txt
docs/hermes/HERMES_OPENCLAW_BRIDGE_RUNBOOK_V1.md
docs/hermes/HERMES_OPENCLAW_BRIDGE_05_CLOSEOUT_2026-04-09.md
docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_PROMPT.txt
docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_V1.md
docs/ui_screenshots/02_archive_policy.md
docs/product_targets/OPENCLAW_TARGET_CANON.md
docs/index/inbox/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01.md
docs/index/inbox/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01.md
docs/index/inbox/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04_RETRY.md
docs/index/inbox/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01.md
docs/index/inbox/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01.md
docs/index/inbox/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01.md
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/06_DECISION_LAB_STUDENT_OPENCLAW_ORCHESTRATION.md
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/30_OPENCLAW_LAB_DEFERRED_BOUNDARY.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_SCORE_GENERATOR_01/60_WHY_SCORE_FALSE_CONFIDENCE_POLICY.md
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01/30_OPENCLAW_E2E_COMMAND_DISCOVERY.md
docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/17_step_05_family_plan_openclaw.md
docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/05_step_02_hygiene_documentaire_batch2_openclaw.md
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01.md
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_WORKER_AUDIT_01/70_WHY_WORKER_HUMAN_REVIEW_POLICY.md
docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/03_OPENCLAW_WORKER_ORCHESTRATION_RULES.md
docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/40_PHASE_4_OPENCLAW_SKILL_INTEGRATION.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_MARKDOWN_PARSER_01/60_WHY_PARSER_FALSE_POSITIVE_POLICY.md
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/10_CROSS_CHANTIERS_OPENCLAW_TMUX_AGENTS_REVIEW.md
docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/02_SANDBOX_AUDIT.md
docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/11_REMEDIATION_SANDBOX_CONFIG_AUDIT.md
docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/ide_bundle/02_PROMPT_IMPL_OPENCLAW_GATEWAY.md
docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/04_api_contract_openclaw_gateway.md
docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md
docs/ot/trae/05_RUNTIME_MCP_POLICY_V1.txt
docs/ot/trae/06_REPO_BOUNDARY_POLICY_V1.txt
docs/ot/trae/trae_pack_texts/trae_pack/TRAE_STATUS_POLICY_V1.1.txt
docs/ot/trae/OT_TRAE_MCP_POLICY_PRE_V1_GEL_DECISION_01.md
docs/ot/closings/OT_TRAE_MCP_POLICY_V1_01_CLOSING.txt
docs/ot/closings/PROJECT_CARD_OPENCLAW_01_CLOSING.txt
docs/product/guides/OPENCLAW_RUNTIME.md
docs/product/guides/OPENCLAW_DOCS_LIBRARY.md

### modules
modules/model_provider_openclaw/docs/GO_OPENCLAW_ALIGNMENT_EXCEPTION_08.md
modules/model_provider_openclaw/docs/GO_OPENCLAW_PROVIDER_POLICY_04.md
modules/model_provider_openclaw/docs/GO_OPENCLAW_ALIGNMENT_DECISION_07.md
modules/model_provider_openclaw/docs/GO_OPENCLAW_ALIGNMENT_READ_06.md
modules/model_provider_openclaw/docs/GO_OPENCLAW_POLICY_RUNTIME_ALIGNMENT_05.md
modules/model_provider_openclaw/docs/model_provider_openclaw.doc.md
modules/model_provider_openclaw/app/model_provider_openclaw.py
modules/model_provider_openclaw/config/providers_policy.yaml
modules/openclaw_config_modulaire/app/openclaw_root_template.json5
modules/evidence_openclaw/docs/GO_OPENCLAW_STATE_DIR_VIGILANCE_03.md
modules/evidence_openclaw/docs/GO_OPENCLAW_SYNC_02.md
modules/evidence_openclaw/docs/GO_OPENCLAW_EVIDENCE_01.md
modules/menu_openclaw/docs/GO_OPENCLAW_INFRA_BASELINE_01.md
modules/menu_openclaw/docs/GO_OPENCLAW_USAGE_EXAMPLES_09.md
modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md
modules/menu_openclaw/docs/GO_OPENCLAW_STATE_DIR_READ_09.md

```

## Repo-wide focused grep — sandbox/allow/deny/policy/jail/scope in modules
```text
modules/reseau_ssh/scripts/_reseau_ssh_transition.sh:61:  mkdir -p /etc/fail2ban/jail.d
modules/reseau_ssh/scripts/_reseau_ssh_transition.sh:62:  cat > /etc/fail2ban/jail.d/sshd.local <<'EOF'
```

## OpenClaw CLI config introspection
```text
config list unavailable
sandbox.mode not readable via CLI
sandbox not readable via CLI
Service: systemd (disabled)
File logs: /tmp/openclaw/openclaw-2026-05-12.log

Config (cli): ~/.openclaw/openclaw.json
Config (service): ~/.openclaw/openclaw.json

Gateway: bind=loopback (127.0.0.1), port=18789 (env/config)
Probe target: ws://127.0.0.1:18789
Dashboard: http://127.0.0.1:18789/
Probe note: Loopback-only gateway; only local clients can connect.

Runtime: unknown (systemctl --user unavailable: Failed to connect to bus: Permission denied
Failed to read server status: Noeud final de transport n'est pas connecté)


Troubles: run openclaw status
Troubleshooting: https://docs.openclaw.ai/troubleshooting
```

## OpenClaw config files via CLI
```text
config path unavailable
config show unavailable
```

## Audit verdict

| Question | Verdict | Evidence |
|:--|:--|:--|
| Config sandbox surface found? | **YES** — `modules/openclaw_config_modulaire/app/agents.json5` contient `sandbox { enforce: true, scope: "agent", allow/deny rules }` | `modules/openclaw_config_modulaire/app/agents.json5` ligne 19-22, config runtime `~/.openclaw/openclaw.json` |
| Global sandbox relaxation required? | **NO** — la configuration sandbox est deja locale et bornee a l'agent | `scope: "agent"` dans agents.json5 |
| Runtime still blocked? | YES | Audit read-only uniquement |
