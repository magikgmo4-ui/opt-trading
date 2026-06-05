# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 02_INPUT_OUTPUT_CONTRACT

## 1_MASTER_TARGET

Define the input and output contract for the future static validator.

## 2_INITIAL_PROJECT_DOC

This contract is derived from the MCP Policy Schema and MCP Policy YAML Draft.

## 3_INITIAL_NEED

A future validator must be able to receive policy documentation artifacts and produce a structured, auditable verdict without executing the policy.

## 4_MASTER_PROJECT_PLAN

The contract defines:

- accepted inputs;
- forbidden inputs;
- required outputs;
- evidence summary;
- deterministic verdict shape;
- no-secret output behavior.

## 6_FINAL_TARGET

The final target is a validator IO specification, not an executable interface.

## 7_CANONICAL_STATE

The current GO creates no command and no file format binding beyond documentation.

## 8_VALIDATED_PLAN

Future validator inputs:

| Input | Required | Description | Rejection condition |
|---|---:|---|---|
| Policy YAML draft | Yes | Canonical policy draft content. | Missing file or unreadable content. |
| Optional JSON mapping draft | No | Conceptual mapping used to compare structural equivalence. | Conflicting content with YAML draft. |
| Schema requirements | Yes | Required fields, enum values, and policy invariants. | Missing schema reference. |
| Validation profile | Yes | Static validation profile, expected to be doc-only and fail-closed. | Unknown profile. |

Forbidden inputs:

- secret values;
- raw environment dumps;
- credential payloads;
- unrestricted command payloads;
- broker order payloads;
- runtime mutation handles;
- live service restart handles.

## 9_SELECTED_SOLUTION

Future validator outputs must use this conceptual shape:

```text
validation_result:
  verdict: PASS_POLICY_STATIC_VALIDATION | failure verdict
  errors:
    - error_code
      severity
      path
      message
      blocked_action
      remediation_safe
  warnings:
    - warning_code
      path
      message
  evidence_summary:
    policy_id
    policy_version
    validated_sections
    missing_sections
    gated_capabilities
    never_allowed_capabilities
  blocked_capabilities:
    - capability_id
  missing_gates:
    - capability_id
  missing_traces:
    - capability_id
  missing_evals:
    - capability_id
  secret_risk_status: PASS_NO_SECRET_RISK | FAIL_SECRET_RISK
  next_action: approve_for_review | fix_policy_doc | block_policy | request_evidence
```

This is not an executable YAML or JSON artifact. It is only a documentation contract.

Required output properties:

- no secret values are reproduced;
- path references point to fields, not secret values;
- every error includes a blocked action;
- every final result includes one verdict;
- failures are sorted deterministically by path and error code;
- ambiguous state produces a blocking verdict.

## 12_INVARIANTS

- Validator output is evidence, not approval.
- `PASS_POLICY_STATIC_VALIDATION` does not authorize runtime use by itself.
- Any secret risk blocks validation.
- Missing policy data blocks validation.
- Unknown capability is listed as blocked.
- No output may include raw secret or credential values.

## 13_ESTABLISHED

Prior docs establish standard verdicts, trace families, eval profiles, gate ids, and capability classes. This contract reuses those names and adds static-validator-specific failure codes.

## 14_HYPOTHESIS

Future output may be JSON for machine consumption, but the conceptual fields above remain required regardless of serialization.

## 15_REMAINING_GAP

No actual serializer exists in this GO.

## 16_TODO

- Map required fields to schema validation rules.
- Map error codes to verdicts.
- Map conceptual fixtures to expected outputs.

## 17_RESUME_POINT

Resume point:

```text
Use this IO contract before implementing any future validator command.
```

## 18_TO_DOCUMENT

Future implementation must document exactly which policy paths were validated and why any path was blocked.

## 19_TO_REMEMBER

The validator output cannot be used as a human approval gate. It is static evidence only.

## RISKS

- À qualifier.
