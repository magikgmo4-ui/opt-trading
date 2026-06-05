---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_OLLAMA_LAB_BINDING
doc_type: ollama_lab_policy_binding
repo: opt-trading
project: opt-trading
module: governance_openclaw_mcp_policy_schema
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01
status: draft_canonical
lifecycle_stage: doc_only_spec
surface: docs/chantiers
source_kind: canonical_local
updated_at: 2026-05-13
---

# 07_OLLAMA_LAB_POLICY_BINDING

## 1_MASTER_TARGET

Definir le binding policy MCP pour Ollama Lab / student / OpenClaw gateway.

## 2_INITIAL_PROJECT_DOC

Sources :

- Reconciliation ChatGPT/OpenClaw/Ollama.
- MCP Boundary runtime/Ollama classes.
- Human Gates `GATE_RUNTIME`, `GATE_OLLAMA_INSTALL`, `GATE_MODEL_PULL`, `GATE_SERVICE_RESTART`.
- Trace/Evals runtime and no-secret profiles.

## 3_INITIAL_NEED

Borner Ollama Lab comme provider local non-production : health/read/smoke no-trade sous gates, sans install, pull, restart, provider switch ou runtime mutation implicite.

## 4_MASTER_PROJECT_PLAN

Classifier les capabilities Ollama Lab :

- `model_read`
- `ollama_health_check`
- `gateway_health_check`
- `smoke_test_no_trade`
- `model_pull`
- `provider_switch`
- `service_restart`
- `install`

## 6_FINAL_TARGET

Policy binding Ollama Lab sans runtime execution dans ce GO.

## 7_CANONICAL_STATE

| Capability | Class | Default status | Gate | Trace | Eval | Verdict path |
| --- | --- | --- | --- | --- | --- | --- |
| `model_read` | `READ_ONLY` | `ALLOW_IF_BOUNDED` for metadata artifact only | none unless live command | `TRACE_MCP_CALL` | `EVAL_TRACE_COMPLETENESS` | `PASS_DOC_ONLY` if source exists |
| `ollama_health_check` | `RUNTIME_GATED` | `NEEDS_GATE` | `GATE_RUNTIME` | `TRACE_RUNTIME_READ`, `TRACE_HUMAN_GATE` | `EVAL_NO_RUNTIME_TOUCH`, `EVAL_GATE_APPROVAL_VALID` | `PASS_RUNTIME_READ_ONLY` only after gate |
| `gateway_health_check` | `RUNTIME_GATED` | `NEEDS_GATE` | `GATE_RUNTIME` | `TRACE_RUNTIME_READ`, `TRACE_HUMAN_GATE` | `EVAL_NO_RUNTIME_TOUCH` | gate required |
| `smoke_test_no_trade` | `RUNTIME_GATED` | `NEEDS_GATE` | `GATE_RUNTIME` | `TRACE_RUNTIME_GATED_ACTION`, `TRACE_HUMAN_GATE` | `EVAL_GATE_APPROVAL_VALID`, `EVAL_NO_RUNTIME_TOUCH` | approved exact command only |
| `model_pull` | `HUMAN_APPROVAL_REQUIRED` | `NEEDS_GATE` | `GATE_MODEL_PULL` | `TRACE_HUMAN_GATE`, action trace | `EVAL_GATE_APPROVAL_VALID`, `EVAL_ROLLBACK_READY` | blocked until approved |
| `provider_switch` | `HUMAN_APPROVAL_REQUIRED` | `NEEDS_GATE` | `GATE_RUNTIME` or future provider gate | `TRACE_HUMAN_GATE`, config/action trace | `EVAL_GATE_APPROVAL_VALID`, `EVAL_ROLLBACK_READY` | blocked until approved |
| `service_restart` | `HUMAN_APPROVAL_REQUIRED` | `NEEDS_GATE` | `GATE_SERVICE_RESTART` | `TRACE_HUMAN_GATE`, `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID`, `EVAL_ROLLBACK_READY` | blocked until approved |
| `install` | `HUMAN_APPROVAL_REQUIRED` | `NEEDS_GATE` | `GATE_OLLAMA_INSTALL` | `TRACE_HUMAN_GATE`, install action trace | `EVAL_GATE_APPROVAL_VALID`, `EVAL_ROLLBACK_READY` | blocked until approved |

### No-secret rule

Ollama Lab outputs cannot contain :

- API keys ;
- tokens ;
- raw env values ;
- private endpoints beyond necessary sanitized metadata ;
- prompt content containing secret values.

### No-trade rule

Ollama Lab cannot execute or simulate a trade path that could be confused with broker/paper/live execution. A smoke test must prove `no_trade=true`.

## 8_VALIDATED_PLAN

Allowed doc-only representation :

```text
capability_id: model_read
class: READ_ONLY
source: existing doc/artifact
no_runtime_command: true
```

Blocked runtime representation :

```text
capability_id: model_pull
class: HUMAN_APPROVAL_REQUIRED
default_status: NEEDS_GATE
gate_id: GATE_MODEL_PULL
no_action_executed: true
```

## 9_SELECTED_SOLUTION

Ollama Lab remains a lab/provider surface, not an implicit runtime control plane.

## 12_INVARIANTS

- No install without `GATE_OLLAMA_INSTALL`.
- No model pull without `GATE_MODEL_PULL`.
- No provider switch without human gate.
- No service restart without `GATE_SERVICE_RESTART`.
- No secret.
- No trade.
- No shell libre.

## 13_ESTABLISHED

Ollama Lab is bounded by class, gate, trace, eval and no-trade policy.

## 14_HYPOTHESIS

A future `GO_OPENCLAW_GOVERNANCE_OLLAMA_LAB_GATEWAY_POLICY_01` can formalize gateway-specific allowlists.

## 15_REMAINING_GAP

No Ollama Lab executable policy exists in this GO.

## 16_TODO

Future GO should decide exact health-check command allowlist and provider-switch policy.

## 17_RESUME_POINT

Use this file before any Ollama Lab model, health, gateway or provider action.

## 18_TO_DOCUMENT

Future implementation must store health outputs as sanitized summaries, not raw logs.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
Ollama Lab policy permits bounded reads, gates live health/smoke, and blocks model pull, provider switch, restart and install until explicit human approval.
```

## RISKS

- À qualifier.
