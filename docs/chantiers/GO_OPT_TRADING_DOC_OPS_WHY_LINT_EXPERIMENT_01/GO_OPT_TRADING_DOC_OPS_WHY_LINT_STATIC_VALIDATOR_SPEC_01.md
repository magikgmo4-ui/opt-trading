---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01
doc_type: chantier_child_spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01
chantier_parent: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: child_spec
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-14
topic_keys:
  - why_lint
  - static_validator
  - warning_only
  - governance
  - runtime_security
  - why_runtime_graph
  - no_autofix
  - no_runtime
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/05_WHY_LINT_WARNING_MODEL_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/06_CROSS_AXIS_GATE_BINDING_01.md
---

# GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01

## 1_MASTER_TARGET

Define the future static validator specification for WHY lint, before any executable implementation.

The validator must remain a future tool specification only in this GO. It must check the coherence of WHY lint rules, warning families, gates, traces, evals, and no-duplication boundaries without changing files, executing runtime, applying fixes, or blocking CI.

## 2_INITIAL_PROJECT_DOC

Parent reference:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
```

Current child reference:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md
```

## 3_INITIAL_NEED

The parent SPEC and review established that WHY lint is valid as a warning-only consolidation layer.

The remaining gap is to specify a static validator before any implementation:

- what it reads;
- what it validates;
- which verdicts it can emit;
- how it handles unknown rules;
- how it remains no-runtime and no-autofix;
- how it maps warning families to gates, traces, and evals;
- how it fails closed when evidence is missing.

## 4_MASTER_PROJECT_PLAN

1. Define validator principles.
2. Define allowed inputs.
3. Define expected outputs.
4. Define rule schema.
5. Define warning-family validation.
6. Define gate / trace / eval binding validation.
7. Define no-duplication boundary validation.
8. Define no-secret and no-runtime checks.
9. Define verdict catalog.
10. Define future fixture corpus requirements.
11. Define future implementation boundaries.

## 5_GO_PLAN

Parent:

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
```

Child:

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01
```

Branch:

```text
go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01
```

Scope: documentation-only static validator specification.

## 6_FINAL_TARGET

**FINAL_TARGET: produce a complete doc-only specification for a future WHY lint static validator that validates warning rules, gate bindings, trace/eval requirements, no-duplication boundaries, and no-runtime/no-autofix invariants, without creating executable code, active CI, or runtime binding.**

## 7_CANONICAL_STATE

Established before this child:

- PR #416 merged the consolidation parent.
- PR #418 merged the SPEC review child.
- `SPEC_WHY_LINT_EXPERIMENT_01.md` is valid as parent reference.
- WHY lint is warning-only.
- WHY lint must not authorize actions.
- WHY lint must not replace governance, runtime security, WHY/runtime graph, or OpenClaw central target.
- Technical implementation is not ready by design.

## 8_VALIDATED_PLAN

Validated steps for this child:

1. Open a child branch after PR #418 merge.
2. Add one spec document under the parent chantier.
3. Keep scope documentation-only.
4. Avoid changes to global indexes.
5. Avoid code, executable files, YAML/JSON active policies, runtime binding, or CI activation.
6. Produce next GO recommendation for fixture corpus.

## 9_SELECTED_SOLUTION

The static validator is defined as a future deterministic checker with these properties:

- local static analysis only;
- explicit input files;
- no source modification;
- no autofix;
- no runtime call;
- no MCP live call;
- no CI failure in this phase;
- fail-closed interpretation for unknown or ambiguous rules;
- reviewable report output.

## 10_SELECTED_SETUP

This GO creates only:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md
```

No implementation path is created yet under `tools/`, `scripts/`, `modules/`, `.github/`, or config directories.

## 11_KEY_DECISIONS

- The validator is future work, not implemented now.
- Unknown warning rule = `BLOCKED_BY_POLICY` or `NEED_MORE_EVIDENCE` depending on context.
- Missing gate binding = validation failure.
- Missing trace/eval binding = validation failure.
- Any autofix setting set to true = validation failure.
- Any runtime binding set to true = validation failure.
- Any CI blocking default set to true = validation failure for this phase.
- Every warning family must map to at least one gate.
- Every warning rule must declare source axis and affected axis.

## 12_INVARIANTS

- Documentation only.
- No executable validator.
- No active YAML/JSON policy.
- No runtime.
- No MCP live.
- No secret.
- No trade.
- No shell operation.
- No autofix.
- No CI blocking.
- No global index mutation.
- No parent SPEC rewrite.
- Fail closed for ambiguous inputs.
- Report only.

## 13_ESTABLISHED

The validator specification is based on these parent assets:

- `SPEC_WHY_LINT_EXPERIMENT_01.md`;
- `05_WHY_LINT_WARNING_MODEL_01.md`;
- `06_CROSS_AXIS_GATE_BINDING_01.md`;
- `02_NO_DUPLICATION_BOUNDARY_MATRIX_01.md`;
- `04_DEPENDENCY_GRAPH_4_AXES_01.md`.

## Validator principles

### Static only

The validator reads documents or future fixture snippets and emits a report. It does not execute OpenClaw, MCP tools, shell commands, trading actions, services, workers, or CI jobs.

### Warning-only

The validator can produce warnings and failures in its own report, but must not block repository CI until a future GO explicitly changes that policy.

### No-autofix

The validator must never patch files, rewrite docs, stage changes, or suggest direct auto-remediation as an executable action.

### Fail closed

If a rule, source, axis, or capability cannot be classified, the result must be one of:

```text
BLOCKED_BY_POLICY
NEED_MORE_EVIDENCE
FAIL_UNKNOWN_RULE
```

## Input contract

Allowed future inputs:

| Input | Required | Notes |
| --- | --- | --- |
| warning rule catalog | yes | Future child output. |
| warning family model | yes | From `05_WHY_LINT_WARNING_MODEL_01.md`. |
| gate binding table | yes | From `06_CROSS_AXIS_GATE_BINDING_01.md`. |
| source manifest | yes | From `03_EXISTING_SOURCE_MANIFEST_01.md`. |
| no-duplication matrix | yes | From `02_NO_DUPLICATION_BOUNDARY_MATRIX_01.md`. |
| fixture corpus | future | Not created in this GO. |
| runtime files | no | Runtime inspection is out of scope. |
| secrets | never | Secret values are forbidden. |

## Output contract

Future validator output must be reviewable and deterministic:

```text
verdict
warnings
failures
blocked_items
missing_evidence
source_files_checked
rules_checked
gates_checked
trace_eval_bindings_checked
next_safe_action
```

No output may contain secrets, credentials, raw environment dumps, unrestricted command output, or runtime mutation results.

## Rule schema draft

A future WHY lint rule must define:

```yaml
rule_id: "string_required"
family: "WHY_GAP | GOVERNANCE_DRIFT | RUNTIME_SECURITY_GAP | MACHINE_SCOPE_GAP | WORKER_OWNER_GAP | MEMORY_SCOPE_GAP | CONTROL_PLANE_GAP | SKILL_REGISTRY_GAP | TRACE_EVAL_GAP | OBSERVABILITY_GAP | BRANCH_CHANTIER_GAP"
severity: "R0 | R1 | R2 | R3 | R4 | R5"
source_axis: "Governance | Runtime Security | WHY Runtime Graph | WHY Lint | OpenClaw Central"
affected_axis:
  - "Governance"
  - "Runtime Security"
  - "WHY Runtime Graph"
  - "OpenClaw Central"
gate_required: "string_required"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "source_file"
  - "section_or_line"
  - "reason"
```

## Schema validation rules

The future validator must check:

1. `rule_id` is present.
2. `family` is one of the approved families.
3. `severity` is one of R0-R5.
4. `source_axis` is known.
5. `affected_axis` is non-empty.
6. `gate_required` exists and is known.
7. `trace_required` is explicit.
8. `eval_required` is explicit.
9. `autofix_allowed` is false.
10. `runtime_binding` is false.
11. `can_fail_ci` is false unless a future GO changes the phase.
12. `evidence_required` is non-empty.

## Warning family validation rules

Approved families:

```text
WHY_GAP
GOVERNANCE_DRIFT
RUNTIME_SECURITY_GAP
MACHINE_SCOPE_GAP
WORKER_OWNER_GAP
MEMORY_SCOPE_GAP
CONTROL_PLANE_GAP
SKILL_REGISTRY_GAP
TRACE_EVAL_GAP
OBSERVABILITY_GAP
BRANCH_CHANTIER_GAP
```

Unknown family verdict:

```text
FAIL_UNKNOWN_WARNING_FAMILY
```

## Gate binding validation rules

Every warning rule must map to one valid gate family from the parent gate binding document.

Minimum accepted gates:

```text
REVIEW_REQUIRED
RUNTIME_PROOF_REQUIRED
GOVERNANCE_ALIGNMENT_REQUIRED
MULTI_MACHINE_REVIEW_REQUIRED
GATE_SECRET
GATE_TRADE
GATE_GIT_PUSH
GATE_GLOBAL_INDEX
GATE_RUNTIME
GATE_OLLAMA_INSTALL
GATE_DOC_WRITE
```

Missing or unknown gate verdict:

```text
FAIL_GATE_BINDING
```

## Trace / eval validation rules

Every warning rule must explicitly require trace and eval metadata.

Missing trace verdict:

```text
FAIL_TRACE_BINDING
```

Missing eval verdict:

```text
FAIL_EVAL_BINDING
```

## No-duplication boundary validation

The future validator must check that a rule does not assign authority to the wrong axis.

Examples:

| Invalid condition | Verdict |
| --- | --- |
| WHY lint authorizes runtime action | FAIL_AXIS_AUTHORITY_DRIFT |
| WHY graph defines permission | FAIL_AXIS_AUTHORITY_DRIFT |
| OpenClaw target grants execution permission | FAIL_AXIS_AUTHORITY_DRIFT |
| Runtime security replaces governance | FAIL_AXIS_AUTHORITY_DRIFT |
| Governance rewrites product target | NEED_MORE_EVIDENCE |

## No-secret static checks

The future validator must reject examples or rules containing likely secret material.

Allowed: obvious placeholders such as:

```text
EXAMPLE_REDACTED_TOKEN
FAKE_SECRET_DO_NOT_USE
DUMMY_CREDENTIAL_BLOCKED
```

Forbidden:

- real-looking token values;
- raw credential dumps;
- environment dumps;
- private key blocks;
- unredacted webhook URLs;
- unredacted API keys.

Secret risk verdict:

```text
FAIL_SECRET_RISK
```

## Runtime binding checks

The future validator must fail any rule or config that implies live runtime operation in this phase.

Invalid fields or meanings:

```text
runtime_binding: true
autofix_allowed: true
can_fail_ci: true
execute_command: true
apply_patch: true
send_message: true
trade_execution: true
service_restart: true
```

Verdict:

```text
FAIL_RUNTIME_BINDING_ENABLED
```

## Verdict catalog

| Verdict | Meaning |
| --- | --- |
| PASS_STATIC_VALIDATOR_SPEC | Spec review passed. |
| PASS_RULE_STATIC_VALIDATION | Rule is valid. |
| WARN_REVIEW_REQUIRED | Rule is valid but requires review. |
| NEED_MORE_EVIDENCE | Source/evidence insufficient. |
| BLOCKED_BY_POLICY | Action or rule cannot be accepted by policy. |
| FAIL_UNKNOWN_RULE | Rule id unknown or malformed. |
| FAIL_UNKNOWN_WARNING_FAMILY | Warning family is not approved. |
| FAIL_SCHEMA_MISSING_FIELD | Required field missing. |
| FAIL_GATE_BINDING | Gate missing or invalid. |
| FAIL_TRACE_BINDING | Trace requirement missing. |
| FAIL_EVAL_BINDING | Eval requirement missing. |
| FAIL_AXIS_AUTHORITY_DRIFT | Rule assigns authority to wrong axis. |
| FAIL_SECRET_RISK | Secret-like material detected. |
| FAIL_RUNTIME_BINDING_ENABLED | Runtime/execution binding detected. |
| FAIL_AUTOFIX_ENABLED | Autofix detected. |
| FAIL_CI_BLOCKING_ENABLED | CI blocking detected before future GO approval. |

## Future fixture corpus requirements

The next child GO should create Markdown-only fixtures covering:

- valid minimal rule;
- valid warning family;
- missing rule id;
- unknown warning family;
- missing gate;
- missing trace;
- missing eval;
- autofix enabled;
- runtime binding enabled;
- CI blocking enabled;
- authority drift;
- secret-like pattern;
- unknown axis;
- missing evidence;
- OpenClaw target treated as permission.

Fixtures must remain non-executable and must not create active YAML/JSON runtime files.

## Future implementation boundaries

If implementation is later approved, it must remain:

- local;
- static;
- read-only;
- no runtime;
- no MCP live;
- no autofix;
- no secret exposure;
- deterministic;
- report-only by default.

Potential implementation surfaces are intentionally not selected in this GO.

## 14_HYPOTHESIS

To validate later:

- whether Markdown-only fixtures are sufficient;
- whether a future parser should consume Markdown fences or extracted YAML;
- whether `can_fail_ci` should remain false forever or only until a future CI GO;
- whether R0 warnings should become review blockers but not CI blockers;
- whether missing OpenClaw governance source docs require a separate reconciliation GO.

## 15_REMAINING_GAP

- No fixture corpus yet.
- No concrete rule catalog yet.
- No implementation yet.
- No CI integration.
- No machine-readable schema file.
- No decision on parser language.
- Missing OpenClaw governance source documents remain unresolved.

## 16_TODO

Next safe sequence:

1. Merge this spec PR.
2. Open fixture corpus child GO.
3. Produce Markdown-only fixtures.
4. Review fixture coverage.
5. Only then consider an implementation GO.

## 17_RESUME_POINT

After merge, resume with:

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01
```

Purpose:

```text
Create Markdown-only fixture corpus for WHY lint static validation before any executable implementation.
```

## 18_TO_DOCUMENT

TAGS:

- WHY_LINT_STATIC_VALIDATOR_SPEC
- WHY_LINT_RULE_SCHEMA
- WHY_LINT_VERDICT_CATALOG
- WHY_LINT_NO_RUNTIME
- WHY_LINT_NO_AUTOFIX
- WHY_LINT_FIXTURE_CORPUS_NEXT

Blocks to extract:

- `Rule schema draft`
- `Schema validation rules`
- `Verdict catalog`
- `Future fixture corpus requirements`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

Memory Bricks candidates:

- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01` defines the future WHY lint static validator only as doc-only spec.
- Unknown or ambiguous lint rules fail closed as `BLOCKED_BY_POLICY`, `NEED_MORE_EVIDENCE`, or `FAIL_UNKNOWN_RULE`.
- Future WHY lint implementation must remain local, static, read-only, report-only, no runtime, no autofix.
- Next safe GO is `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01`.

## Verdict

```text
PASS_STATIC_VALIDATOR_SPEC_DOC_ONLY
```

## RISKS

- À qualifier.
