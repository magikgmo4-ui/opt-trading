# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01 -- 01_CI_DRAFT_PRINCIPLES

## 1_MASTER_TARGET

Define the principles for a future CI integration of the OpenClaw MCP Policy static validator and fixture harness.

## 2_INITIAL_PROJECT_DOC

The draft follows the validator spec, fixture corpus, implementation closeout, and fixture harness closeout.

## 3_INITIAL_NEED

The CI path must be precise before a workflow exists, because the validator and harness are safety controls and must not become runtime activation or policy promotion mechanisms.

## 4_MASTER_PROJECT_PLAN

Record CI principles as documentation only, with no active workflow file and no change to CI configuration.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`

## 7_CANONICAL_STATE

The current validator and harness are local static tools:

- validator command: `python -m modules.governance.openclaw_mcp_policy_validator path\to\policy.yaml`
- fixture harness command: `python -m modules.governance.openclaw_mcp_policy_validator.fixture_harness docs\chantiers\GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01`
- fixture corpus count: `37`
- canonical fixture index: `09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md`

## 8_VALIDATED_PLAN

CI draft principles:

| Principle | Rule | CI consequence |
|---|---|---|
| CI draft only | This GO creates documentation only. | No workflow file is added. |
| No active workflow | `.github/workflows` is untouched. | No GitHub Action can run from this GO. |
| Fail closed | Any unsafe, ambiguous, or missing evidence fails. | Future CI exits non-zero. |
| No runtime | Static validation cannot load policy runtime. | Runtime binding checks must remain mandatory. |
| No MCP live | CI must not call a live MCP server. | No server URL or token is required. |
| No Ollama call | CI must not call Ollama runtime. | Ollama checks remain policy text validation only. |
| No network | Validator and harness must not require network. | Network is not part of tool behavior. |
| No secret | Logs must not display secret-like values. | Secret risk fails closed. |
| No env dump | CI must not print environment variables. | Debug env steps are forbidden. |
| Deterministic tests | Same input produces same report. | Reports can be compared safely. |
| Warnings explicit | Inline/index drift must be visible. | Activation remains gated while warnings exist. |

## 9_SELECTED_SOLUTION

The future CI should run static commands only and report verdicts. It must never approve runtime policy use, human gates, trades, shell access, secrets, or policy promotion.

## 12_INVARIANTS

- Documentation only in this GO.
- No active workflow.
- No runtime.
- No MCP live.
- No Ollama call.
- No network call.
- No secret read.
- No environment dump.
- No trade.
- No sudo.
- No active YAML or JSON policy added.
- No global index modification.

## 13_ESTABLISHED

The harness closeout established:

```text
PASS_FIXTURE_HARNESS
total_fixtures=37
pass_count=37
fail_count=0
mismatches=0
warnings=4
```

The 4 warnings are metadata drift between inline fixture expectations and the canonical index. They are not validator mismatches.

## 14_HYPOTHESIS

Future CI should first treat warnings as reported-but-gated evidence, not as silent success. Strict failure on warnings can be added after a dedicated warning reconciliation or acceptance GO.

## 15_REMAINING_GAP

The future active workflow is not authorized by this draft. The warnings must be corrected or accepted before activation.

## 16_TODO

Future CI activation must verify:

- current tests still pass;
- harness still reports 37/37 PASS;
- warning handling is explicit;
- no runtime binding exists;
- no secret output exists.

## 17_RESUME_POINT

The next operational step after this doc-only GO should address warning reconciliation or gated CI activation.

## 18_TO_DOCUMENT

Future CI activation closeout must include the exact workflow path, commit hash, workflow trigger scope, rollback path, and human approval evidence.

## 19_TO_REMEMBER

CI is a preflight safety check. It is not a runtime gate approval and not a policy loader.

## RISKS

- À qualifier.
