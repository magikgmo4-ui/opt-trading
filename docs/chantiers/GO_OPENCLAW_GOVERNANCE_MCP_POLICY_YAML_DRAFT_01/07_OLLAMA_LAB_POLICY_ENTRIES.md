---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_OLLAMA_LAB
doc_type: ollama_lab_policy_entries
status: draft_doc_only
module: governance_openclaw_mcp_policy_yaml_draft
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
runtime_binding: false
validator_created: false
---

# 07_OLLAMA_LAB_POLICY_ENTRIES

## 1_MASTER_TARGET

Borner Ollama Lab comme surface locale non-production, sans secret, sans trade, sans shell libre et sans mutation runtime non gatee.

## 2_INITIAL_PROJECT_DOC

Sources :

- ChatGPT Orchestration Reconciliation : Ollama Lab comme provider local lab.
- MCP Boundary : model/health/logs read-only ou runtime-gated.
- Human Gates : `GATE_RUNTIME`, `GATE_MODEL_PULL`, `GATE_OLLAMA_INSTALL`, `GATE_SERVICE_RESTART`.
- Trace/Evals : runtime read/gated action traces.

## 3_INITIAL_NEED

Les actions Ollama semblent proches d'un lab read-only, mais plusieurs operations sont en realite runtime ou reseau/disque. La policy doit separer read metadata, health checks, smoke tests, model pulls, provider switch, service restart et install.

## 4_MASTER_PROJECT_PLAN

Classer les entrees Ollama Lab :

- reads metadata ;
- health checks ;
- smoke tests no trade ;
- model pull gated ;
- provider switch gated ;
- service restart gated ;
- install gated ;
- no secret ;
- no trade ;
- no unrestricted shell.

## 6_FINAL_TARGET

Une table de policy Ollama Lab prete a etre reprise dans un futur manifest, sans execution.

## 7_CANONICAL_STATE

Ollama Lab status :

```text
lab_status: local_non_production
runtime_binding: false
trade_allowed: false
secret_allowed: false
unrestricted_shell_allowed: false
install_allowed_by_default: false
model_pull_allowed_by_default: false
service_restart_allowed_by_default: false
provider_switch_allowed_by_default: false
```

## 8_VALIDATED_PLAN

Entries demandees :

- `ollama_models_read`
- `ollama_health_check`
- `gateway_health_check`
- `smoke_test_no_trade`
- `provider_routing_read`
- `model_pull`
- `provider_switch`
- `service_restart`
- `install`

## 9_SELECTED_SOLUTION

| entry | class | default status | gate | trace | eval | allowed output | blocked |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ollama_models_read` | `READ_ONLY` | `ALLOWED_IF_METADATA_ONLY` | none | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | model metadata summary from existing artifact or doc | live pull, license bypass, raw config secrets |
| `ollama_health_check` | `RUNTIME_GATED` | `BLOCKED_UNTIL_GATE` | `GATE_RUNTIME` | `TRACE_RUNTIME_READ` | `EVAL_NO_RUNTIME_TOUCH` | sanitized health report | install, model pull, service restart, secret output |
| `gateway_health_check` | `RUNTIME_GATED` | `BLOCKED_UNTIL_GATE` | `GATE_RUNTIME` | `TRACE_RUNTIME_READ` | `EVAL_NO_RUNTIME_TOUCH` | sanitized gateway status | config mutation, network exposure, secret output |
| `smoke_test_no_trade` | `RUNTIME_GATED` | `BLOCKED_UNTIL_GATE` | `GATE_RUNTIME` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` | smoke result with no-trade proof | broker path, order path, secret output |
| `provider_routing_read` | `READ_ONLY` | `ALLOWED_IF_DOC_OR_CONFIG_SUMMARY_ONLY` | none | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | provider routing summary | provider switch, credential display |
| `model_pull` | `RUNTIME_GATED` | `BLOCKED_UNTIL_GATE` | `GATE_MODEL_PULL` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` | pull plan/result only after gate | implicit download, unlicensed model, no rollback |
| `provider_switch` | `RUNTIME_GATED` | `BLOCKED_UNTIL_GATE` | `GATE_MCP_WRITE` + `GATE_RUNTIME` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` | switch plan/result only after gate | silent routing mutation, production change |
| `service_restart` | `RUNTIME_GATED` | `BLOCKED_UNTIL_GATE` | `GATE_SERVICE_RESTART` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` | restart plan/result only after gate | stop/start without rollback or window |
| `install` | `RUNTIME_GATED` | `BLOCKED_UNTIL_GATE` | `GATE_OLLAMA_INSTALL` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` | install plan/result only after gate | package operation without source/version/rollback |

No-go entries :

| rule | decision |
| --- | --- |
| no secret | values never displayed, exported or stored |
| no trade | no order path, no broker mutation, no alert-to-trade bridge |
| no unrestricted shell | only named tools in future policy, never shell libre |
| no sudo | no privileged operation inside MCP policy |
| no runtime in this GO | all live checks remain documentary and blocked |

## 12_INVARIANTS

- Ollama Lab is local lab, not production authority.
- Model pull is gated, not read-only.
- Provider switch is a mutation and gated.
- Service restart is runtime and gated.
- Install is gated and requires rollback.
- Smoke test must prove no trade.
- Secret values are never output.

## 13_ESTABLISHED

Ollama Lab entries are bound to the same gate/trace/eval rules as the rest of MCP policy.

## 14_HYPOTHESIS

A future lab gateway can expose separate read-only and gated tools, but no gateway change is made here.

## 15_REMAINING_GAP

- No Ollama command allowlist.
- No model license policy.
- No provider routing validator.
- No runtime gateway implementation.

## 16_TODO

- Future GO should define `GO_OPENCLAW_GOVERNANCE_OLLAMA_LAB_GATEWAY_POLICY_01` or equivalent implementation policy.
- Future GO should decide whether health checks can become read-only through a brokered non-mutating endpoint.

## 17_RESUME_POINT

When in doubt, classify Ollama Lab action as `RUNTIME_GATED` unless it is a doc/artifact metadata read.

## 18_TO_DOCUMENT

Future docs should include negative examples for model pull, provider switch and service restart without gates.

## 19_TO_REMEMBER

Ollama Lab convenience does not override MCP safety. Local lab actions can still mutate disk, process state or routing.

## RISKS

- À qualifier.
