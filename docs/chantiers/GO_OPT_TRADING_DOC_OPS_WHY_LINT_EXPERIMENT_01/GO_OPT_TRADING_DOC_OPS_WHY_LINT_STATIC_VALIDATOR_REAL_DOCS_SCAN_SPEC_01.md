---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01
doc_type: chantier_child_spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01
chantier_parent: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: child_spec
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-14
topic_keys:
  - why_lint
  - real_docs_scan
  - static_validator
  - read_only
  - report_only
  - no_autofix
  - no_runtime
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01.md
  - tools/why_lint_static_validator/README.md
  - tools/why_lint_static_validator/why_lint_static_validator.py
  - tests/why_lint_static_validator/test_why_lint_static_validator.py
---

# GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01

## 1_MASTER_TARGET

Specify the first read-only scan of real repository documents with the WHY lint static validator.

This GO does not implement the real-docs scan. It defines the safe scope, input set, output report, failure modes, and review gates required before extending the validator beyond the fixture corpus.

## WHY

This specification exists to define a safe path from fixture-only validation to real-doc scanning, while preserving read-only/report-only behavior and preventing the validator from becoming an autofix, CI, or runtime authority.

## 2_INITIAL_PROJECT_DOC

Parent reference:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
```

Implementation reference:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01.md
```

Current child reference:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md
```

## 3_INITIAL_NEED

The WHY lint static validator now validates the Markdown fixture corpus in read-only/report-only mode.

The next gap is to define how the validator may later scan real documents in the repository without becoming an auto-fix tool, CI blocker, runtime connector, or source of authority.

Need:

- identify allowed real-doc targets;
- define what can be scanned;
- define what cannot be scanned;
- define report-only output;
- preserve no-runtime and no-autofix invariants;
- avoid touching global indexes;
- avoid replacing human review.

## 4_MASTER_PROJECT_PLAN

1. Define real-doc scan scope.
2. Define allowed input surfaces.
3. Define excluded input surfaces.
4. Define scan checks.
5. Define output report schema.
6. Define severity and verdict mapping.
7. Define human review path.
8. Define no-mutation guarantees.
9. Define next implementation GO boundaries.

## 5_GO_PLAN

Parent:

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
```

Child:

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01
```

Branch:

```text
go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01
```

Scope: documentation-only scan specification.

## 6_FINAL_TARGET

**FINAL_TARGET: define a doc-only specification for scanning real repository documents with the WHY lint static validator in read-only/report-only mode, without mutation, autofix, runtime binding, CI blocking, or authority replacement.**

## 7_CANONICAL_STATE

Established before this GO:

- parent consolidation merged;
- SPEC review merged;
- static validator spec merged;
- fixture corpus merged;
- read-only static validator implementation merged;
- validator currently validates fixtures, not real docs;
- next safe step is a real-docs scan specification.

## 8_VALIDATED_PLAN

Validated steps:

1. Keep this GO documentation-only.
2. Do not modify validator code.
3. Do not add CI workflow.
4. Do not add active YAML/JSON config.
5. Define allowed scan targets.
6. Define report output.
7. Define implementation constraints for the future GO.

## 9_SELECTED_SOLUTION

Define a two-stage future approach:

1. `REAL_DOCS_SCAN_SPEC`: current GO, doc-only.
2. `REAL_DOCS_SCAN_IMPLEMENTATION_READONLY`: future GO, optional, still read-only/report-only.

No direct jump from fixture validation to real repo scanning implementation.

## 10_SELECTED_SETUP

This GO creates only one document:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md
```

No files are added under `tools/`, `tests/`, `.github/`, `configs/`, or global indexes in this GO.

## 11_KEY_DECISIONS

- Real-doc scanning must be opt-in and path-scoped.
- Default scan target should be the parent WHY lint chantier first.
- The scan must produce a report only.
- The scan must not rewrite documents.
- The scan must not stage, commit, or patch anything.
- The scan must not become CI blocking.
- The scan must not call OpenClaw, MCP, services, Telegram, workers, or trading runtime.
- Any uncertain finding becomes `NEED_MORE_EVIDENCE`.
- Any authority confusion becomes `FAIL_AXIS_AUTHORITY_DRIFT` in the report only.

## 12_INVARIANTS

- Documentation only for this GO.
- Future scan remains local.
- Future scan remains read-only.
- Future scan remains report-only.
- No runtime.
- No MCP live.
- No service call.
- No Telegram send.
- No trade.
- No secret inspection.
- No autofix.
- No CI blocking.
- No global index mutation.
- No source mutation.
- Human review remains required for action.

## 13_ESTABLISHED

The real-doc scan must extend from the fixture validator, not replace it.

The fixture corpus remains the safety contract. Any real-doc scan behavior must be tested against fixture patterns before running over broader repo documents.

## Allowed scan surfaces

Initial allowed surfaces for future implementation:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/*.md
```

Future expanded surfaces only after review:

```text
docs/chantiers/*/*.md
docs/governance/*.md
docs/index/inbox/*.md
```

## Excluded scan surfaces

Excluded by default:

```text
.env
.env.*
**/secrets/**
**/private/**
**/*.key
**/*.pem
**/*.sqlite
**/*.db
runtime/**
logs/**
configs/** active runtime configs
.github/workflows/**
```

The validator must not search for secrets. It may only detect unsafe patterns in scanned text if those patterns appear in allowed docs.

## Real-doc scan checks

The future scan may check:

| Check | Description | Verdict family |
| --- | --- | --- |
| missing WHY section | document has GO/spec content but no WHY | WHY_GAP |
| missing gate binding | warning-like rule has no gate | FAIL_GATE_BINDING |
| missing trace/eval binding | rule-like block lacks trace/eval | FAIL_TRACE_BINDING / FAIL_EVAL_BINDING |
| autofix enabled | text implies autofix allowed | FAIL_AUTOFIX_ENABLED |
| runtime binding enabled | text implies live binding | FAIL_RUNTIME_BINDING_ENABLED |
| CI blocking enabled | text implies blocking CI before approval | FAIL_CI_BLOCKING_ENABLED |
| authority drift | layer claims wrong authority | FAIL_AXIS_AUTHORITY_DRIFT |
| missing source evidence | claim lacks source or file evidence | NEED_MORE_EVIDENCE |
| unknown warning family | warning family not approved | FAIL_UNKNOWN_WARNING_FAMILY |

## Output report schema

Future report output should include:

```text
scan_id
scan_timestamp
repo
branch
scan_scope
files_scanned
files_skipped
findings_count
findings_by_severity
findings_by_family
findings
summary_verdict
next_safe_action
```

Each finding should include:

```text
finding_id
file
section_or_line
warning_family
severity
verdict
expected_gate
trace_required
eval_required
evidence
human_review_required
```

## Summary verdicts

Allowed summary verdicts:

```text
PASS_REAL_DOCS_SCAN_REPORT
WARN_REAL_DOCS_SCAN_FINDINGS
NEED_MORE_EVIDENCE
BLOCKED_BY_POLICY
FAIL_SCAN_INPUT_SCOPE
FAIL_SCAN_FORMAT
FAIL_SECRET_RISK
FAIL_INTERNAL_ERROR
```

These verdicts are report verdicts only. They do not block CI and do not modify files.

## Human review protocol

If findings are emitted:

1. Human reviews the report.
2. Human decides whether a follow-up GO is needed.
3. Corrections happen in the source axis, not inside WHY lint.
4. WHY lint never patches the source document automatically.

## Future command shape

Possible future command, not implemented in this GO:

```text
python tools/why_lint_static_validator/why_lint_static_validator.py \
  --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01 \
  --report-format text
```

The current GO does not add this command.

## Future implementation constraints

A future implementation must:

- keep fixture validation unchanged;
- add real-doc scan behind an explicit flag;
- require explicit path argument;
- refuse excluded paths;
- default to report-only;
- never write output files unless a future GO approves report artifacts;
- never modify scanned docs;
- keep exit codes deterministic;
- keep tests isolated with temporary files.

## 14_HYPOTHESIS

To validate later:

- whether scan output should be text-only first;
- whether JSON report files should be allowed in a later GO;
- whether scan scope should start only with the WHY lint parent directory;
- whether global docs should be scanned only after parent directory proof;
- whether findings should reuse R0-R5 exactly or include a separate confidence score.

## 15_REMAINING_GAP

- No real-doc scan implementation yet.
- No report artifact format selected.
- No tests for real-doc scan yet.
- No path exclusion implementation yet.
- No human review report template yet.
- No broader docs scan scope approved yet.
- No CI integration approved.
- No OpenClaw integration approved.

## 16_TODO

Next safe sequence:

1. Merge this spec PR.
2. Open implementation GO for real-doc scan read-only.
3. Add explicit `--scan-docs` flag.
4. Add path allowlist/exclusion rules.
5. Add tests with temporary Markdown files.
6. Validate scan over the WHY lint parent directory only.
7. Report results in stdout only.

## 17_RESUME_POINT

After merge, resume with:

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_READONLY_01
```

Purpose:

```text
Implement explicit-path real-doc scanning for WHY lint static validator, read-only/report-only, starting only with the WHY lint parent directory.
```

## 18_TO_DOCUMENT

TAGS:

- WHY_LINT_REAL_DOCS_SCAN_SPEC
- WHY_LINT_READ_ONLY_SCAN
- WHY_LINT_REPORT_ONLY
- WHY_LINT_NO_AUTOFIX
- WHY_LINT_NO_CI_BLOCKING

Blocks to extract:

- `Allowed scan surfaces`
- `Excluded scan surfaces`
- `Real-doc scan checks`
- `Output report schema`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

Memory Bricks candidates:

- Real-doc scanning for WHY lint must start with explicit path scope and report-only output.
- The future first scan target is `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/` only.
- Real-doc scan must not modify docs, block CI, call runtime, or integrate OpenClaw.
- Next safe GO is `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_READONLY_01`.

## Verdict

```text
PASS_REAL_DOCS_SCAN_SPEC_DOC_ONLY
```
