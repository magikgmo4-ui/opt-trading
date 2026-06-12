# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01 -- 04_CI_NO_SECRET_NO_RUNTIME_POLICY

## 1_MASTER_TARGET

Define the future CI no-secret, no-runtime, no-network policy for the MCP Policy static validator and fixture harness.

## 2_INITIAL_PROJECT_DOC

This policy extends the validator static checks and harness invariants into future CI boundaries.

## 3_INITIAL_NEED

CI must not leak secrets, read secret stores, dump environment variables, call runtime services, or treat documentary fixture snippets as active policies.

## 4_MASTER_PROJECT_PLAN

Document the safety policy only. Do not create CI configuration, runtime bindings, or active YAML/JSON artifacts.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`

## 7_CANONICAL_STATE

The current validator suppresses secret-like values in output. The current harness compares fixture outcomes without printing snippet bodies and writes materialized snippets only to temporary storage.

## 8_VALIDATED_PLAN

Future CI safety rules:

| Area | Required rule | Failure verdict |
|---|---|---|
| Logs | No secret value or secret-like value is printed. | `FAIL_SECRET_RISK` |
| Environment | No environment dump is allowed. | `FAIL_SECRET_RISK` |
| Tokens | No token-like output is allowed. | `FAIL_SECRET_RISK` |
| MCP | No live MCP call is allowed. | `BLOCKED_WITH_REASON` |
| OpenClaw runtime | No runtime policy load is allowed. | `FAIL_RUNTIME_BINDING_ENABLED` |
| Ollama | No Ollama runtime call is allowed. | `BLOCKED_WITH_REASON` |
| Trade | No trade command is allowed. | `FAIL_POLICY` |
| Sudo | No sudo is allowed. | `BLOCKED_WITH_REASON` |
| Network | Validator and harness must not require network. | `BLOCKED_WITH_REASON` |
| Snippets | Extracted snippets may exist only in temporary storage. | `FAIL_POLICY` |

## 9_SELECTED_SOLUTION

The future CI should use read-only checkout content and temporary files for extracted snippets. It should not write policy YAML, JSON reports, or runtime config back into the repository unless a later GO explicitly approves a report artifact path.

## 12_INVARIANTS

- No secret read.
- No secret display.
- No environment dump.
- No token-like output.
- No credential display.
- No runtime binding.
- No MCP live call.
- No Ollama runtime call.
- No trade.
- No sudo.
- No network dependency in validator or harness behavior.
- Temporary snippet files only.

## 13_ESTABLISHED

The existing tools already state:

- the validator reads only the explicit local file;
- the validator does not mutate the policy;
- the validator does not load runtime;
- the harness writes snippets only under system temporary storage;
- the harness does not create active repository YAML/JSON files.

## 14_HYPOTHESIS

Future CI platform setup may require checkout and dependency installation. That platform setup must remain separate from validator/harness behavior and must not introduce runtime or secret access.

## 15_REMAINING_GAP

No active CI environment has been approved. Therefore no secret policy has been tested inside GitHub Actions.

## 16_TODO

Future activation must verify:

- no `secrets.*` usage in workflow steps;
- no `env` dump;
- no service containers;
- no runtime endpoint;
- no MCP URL;
- no Ollama host;
- no broker credentials;
- no artifact containing snippet bodies unless explicitly approved.

## 17_RESUME_POINT

This policy must be carried into `GATE_CI_ACTIVATION`.

## 18_TO_DOCUMENT

Future workflow closeout must state whether any dependency installation occurs and why it does not violate validator/harness no-network behavior.

## 19_TO_REMEMBER

The presence of `SECRET` in this Markdown file path is a documentary no-secret policy label, not secret content.

## RISKS

- À qualifier.
