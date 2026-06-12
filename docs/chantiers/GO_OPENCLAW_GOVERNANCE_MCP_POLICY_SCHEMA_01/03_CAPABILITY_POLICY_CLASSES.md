---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_CLASSES
doc_type: capability_policy_classes
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

# 03_CAPABILITY_POLICY_CLASSES

## 1_MASTER_TARGET

Definir les classes de capability policy.

## 2_INITIAL_PROJECT_DOC

Source directe : `GO_OPENCLAW_GOVERNANCE_MCP_BOUNDARY_SPEC_01/02_CAPABILITY_CLASSIFICATION_MATRIX.md`.

## 3_INITIAL_NEED

Transformer les classes MCP Boundary en classes de schema opposables.

## 4_MASTER_PROJECT_PLAN

Chaque classe precise default, gate, trace, eval, rollback et exemples.

## 6_FINAL_TARGET

Table canonique des classes policy.

## 7_CANONICAL_STATE

| Capability class | Default status | Description | Gate | Trace | Eval | Rollback | Examples |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `READ_ONLY` | `ALLOW_IF_BOUNDED` | lecture repo/artifact sans secret ni runtime live | none unless source live | `TRACE_MCP_CALL` or `TRACE_TOOL_CALL` | `EVAL_TRACE_COMPLETENESS`, `EVAL_MCP_BOUNDARY_COMPLIANCE` | none | `repo_state`, `branch_state`, `go_index_read` |
| `READ_SANITIZED` | `ALLOW_IF_SANITIZED` | lecture sortie seulement apres redaction/synthese | gate if raw or live source | `TRACE_MCP_CALL`, `TRACE_RUNTIME_READ`, `TRACE_SECRET_BLOCK` if blocked | `EVAL_NO_SECRET_LEAK`, `EVAL_TRACE_COMPLETENESS` | none | `logs_tail_sanitized`, `environment_summary_no_secret` |
| `WRITE_GATED` | `NEEDS_GATE` | write borne, non runtime, avec GO/scope/diff | `GATE_DOC_WRITE` or `GATE_MCP_WRITE` | `TRACE_CODEX_PATCH`, `TRACE_MCP_CALL`, `TRACE_HUMAN_GATE` | `EVAL_GATE_REQUIRED`, `EVAL_ROLLBACK_READY`, `EVAL_DOC_ONLY_COMPLIANCE` | revert patch/delete created file | `create_doc_file`, `create_inbox_entry` |
| `RUNTIME_GATED` | `NEEDS_GATE` | live command/read probe/smoke no-trade | `GATE_RUNTIME` or Ollama gate | `TRACE_RUNTIME_READ`, `TRACE_RUNTIME_GATED_ACTION`, `TRACE_HUMAN_GATE` | `EVAL_NO_RUNTIME_TOUCH`, `EVAL_GATE_APPROVAL_VALID` | stop/restore if applicable | `ollama_health_check`, `gateway_health_check`, `smoke_test_no_trade` |
| `HUMAN_APPROVAL_REQUIRED` | `NEEDS_GATE` | sensitive action requiring explicit human decision | specific family gate | `TRACE_HUMAN_GATE`, plus action trace | `EVAL_GATE_APPROVAL_VALID`, `EVAL_ROLLBACK_READY` | required when destructive | `git push`, `merge`, `service restart`, `model_pull` |
| `BLOCKED_BY_DEFAULT` | `BLOCKED_BY_DEFAULT` | not allowed unless future GO reclassifies into named tool | no generic approval | `TRACE_MCP_CALL` or block trace | `EVAL_MCP_BOUNDARY_COMPLIANCE`, `EVAL_GATE_REQUIRED` | none unless reclassified | `unrestricted shell`, `sudo`, `remote command execution` |
| `NEVER_ALLOWED` | `NEVER_ALLOWED` | no approval path inside OpenClaw MCP | none | `TRACE_SECRET_BLOCK`, `TRACE_TRADE_BLOCK`, `TRACE_MCP_CALL` | `EVAL_NO_SECRET_LEAK`, `EVAL_GATE_REQUIRED` | none | `secret exfiltration`, `credential display`, `bypass gate`, `trade execution without GO` |

## 8_VALIDATED_PLAN

Class transitions allowed only by future GO :

```text
READ_ONLY -> READ_SANITIZED only if output risk increases.
WRITE_GATED -> HUMAN_APPROVAL_REQUIRED if blast radius increases.
RUNTIME_GATED -> HUMAN_APPROVAL_REQUIRED if mutation/restart/install/pull appears.
BLOCKED_BY_DEFAULT -> named gated tool only through dedicated GO.
NEVER_ALLOWED -> no transition inside OpenClaw MCP.
```

## 9_SELECTED_SOLUTION

`READ_ONLY` and sanitized reads are the only classes that can be allowed without a human gate, and only when secret and runtime constraints remain satisfied.

## 12_INVARIANTS

- Class is mandatory.
- Unknown class is `FAIL_POLICY`.
- Missing class is `BLOCKED_BY_POLICY`.
- `NEVER_ALLOWED` cannot be softened by actor, machine or gate.

## 13_ESTABLISHED

The seven classes from MCP Boundary are preserved.

## 14_HYPOTHESIS

Future policy may add subclasses, but the top-level class must remain one of the seven.

## 15_REMAINING_GAP

No machine-readable enum file exists.

## 16_TODO

Bind classes to gates in `04_GATE_BINDING_SCHEMA.md`.

## 17_RESUME_POINT

Use this file to answer "what class is this capability?".

## 18_TO_DOCUMENT

Future runtime policy must keep these class names stable.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
OpenClaw MCP policy has seven canonical classes; anything outside them fails schema validation.
```

## RISKS

- À qualifier.
