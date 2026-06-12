# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01 -- 00_CADRAGE

## 1_MASTER_TARGET

OpenClaw needs a documentation-only fixture corpus for the future MCP policy static validator.

The master target is to prepare expected pass, fail, and blocked examples without creating executable tests, active YAML, active JSON, runtime hooks, or a validator.

## 2_INITIAL_PROJECT_DOC

This chantier follows:

```text
Reconciliation
-> MCP Boundary
-> Human Review Gates
-> Trace / Evals Profile
-> MCP Policy Schema
-> MCP Policy YAML Draft
-> MCP Policy Static Validator Spec
-> MCP Policy Static Validator Fixture Corpus
```

## 3_INITIAL_NEED

The future validator needs a stable corpus of examples that can later become test fixtures.

This GO keeps the examples in Markdown only, with fenced `text` snippets and explicit expected verdicts.

## 4_MASTER_PROJECT_PLAN

Create a local chantier with:

- fixture corpus principles;
- valid fixture set;
- schema failure fixture set;
- capability class failure fixture set;
- gate, trace, and eval failure fixture set;
- never-allowed failure fixture set;
- no-secret failure fixture set with fake placeholders only;
- strict worker failure fixture set;
- fixture index and expected verdicts;
- future test harness requirements;
- closeout.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01`

Final target:

```text
Create a complete Markdown-only conceptual fixture corpus for the future OpenClaw MCP policy static validator.
```

## 7_CANONICAL_STATE

Git state checked in the dedicated worktree:

```text
Worktree:
C:\Users\ghost\opt-trading-mcp-policy-static-validator-fixture-corpus

git status --short --branch:
## go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01

git branch --show-current:
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01

git log --oneline -5:
248b6c38 docs: specify OpenClaw MCP policy static validator
1403a3e6 docs: draft OpenClaw MCP policy YAML
fa7558f2 docs: define OpenClaw MCP policy schema
e34b9952 Merge pull request #343 from magikgmo4-ui/go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01
b21a6cd1 Merge pull request #344 from magikgmo4-ui/go/GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01

git remote -v:
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
```

Branch:

```text
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01
```

Base:

```text
248b6c38 docs: specify OpenClaw MCP policy static validator
```

## 8_VALIDATED_PLAN

Validated plan:

1. Keep all fixtures in Markdown.
2. Use fenced `text` snippets only.
3. Assign one expected verdict to every fixture.
4. Assign one expected error code to every invalid fixture.
5. Map every fixture to rule, gate, trace, and eval.
6. Do not create `.yaml`, `.yml`, `.json`, script, validator, runner, or config file.
7. Do not modify global indexes.
8. Stage only the current chantier and local inbox.

## 9_SELECTED_SOLUTION

Create the fixture corpus under:

```text
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/
```

Create the local inbox entry:

```text
docs/index/inbox/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md
```

## 12_INVARIANTS

- Documentation only.
- No executable code.
- No real validator.
- No active YAML file.
- No active JSON file.
- No runtime.
- No trade.
- No sudo.
- No secret.
- No unrestricted shell.
- No merge.
- No forced push.
- No branch cleanup.
- No auto-fix.
- No global index modification.
- Never use `git add -A`.
- Stage only current chantier and inbox.
- Fixtures remain Markdown.
- Snippets are fenced documentation examples only.
- Future validator behavior must fail closed.

## 13_ESTABLISHED

Sources read:

```text
docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_BOUNDARY_SPEC_01/ via branch reference
docs/chantiers/GO_OPENCLAW_GOVERNANCE_HUMAN_REVIEW_GATES_01/ via branch reference
docs/chantiers/GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01/ via branch reference
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01/
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01/
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01/
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01/09_CONCEPTUAL_FIXTURES.md
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01/08_VERDICT_AND_ERROR_CATALOG.md
docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
docs/index/BRANCH_STATE.md
docs/index/GO_INDEX.md
docs/index/ACTIVE_STREAMS.md
docs/index/REPRISE.md
```

Established decisions:

- unknown capability must be blocked by default;
- unknown class fails as `FAIL_UNKNOWN_CLASS`;
- missing fields fail as `FAIL_SCHEMA_MISSING_FIELD`;
- missing gate, trace, or eval binding returns its dedicated failure;
- `runtime_binding: true` fails as `FAIL_RUNTIME_BINDING_ENABLED`;
- `NEVER_ALLOWED` with approval path returns `FAIL_NEVER_ALLOWED_APPROVAL_PATH`;
- secret risk returns `FAIL_SECRET_RISK` without value reproduction;
- strict workers cannot self-approve.

## 14_HYPOTHESIS

The future test harness may parse Markdown and extract fenced snippets, but this GO does not implement that parser.

## 15_REMAINING_GAP

After this GO, remaining gaps are expected:

- no runnable fixture corpus;
- no validator implementation;
- no Markdown parser;
- no test harness;
- no CI integration;
- no runtime binding.

## 16_TODO

- Create 12 chantier files.
- Create one local inbox entry.
- Verify no executable files.
- Verify no active YAML/JSON files.
- Verify no global indexes changed.
- Stage only current chantier and inbox.
- Commit doc-only corpus.

## 17_RESUME_POINT

Resume from:

```text
Static Validator Spec PASS_DOC_ONLY on branch go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 with commit 248b6c38.
```

Current work:

```text
Prepare a Markdown-only fixture corpus before static validator implementation.
```

## 18_TO_DOCUMENT

Document fixture id, purpose, expected verdict, expected error code, policy snippet, reason, validator rule, related gate, related trace, and related eval for every fixture.

## 19_TO_REMEMBER

The expected closeout verdict for this GO is:

```text
PASS_DOC_ONLY
```

If any executable file, active YAML/JSON, runtime binding, global index edit, or real secret appears, the expected verdict becomes:

```text
BLOCKED_WITH_REASON
```

## RISKS

- À qualifier.
