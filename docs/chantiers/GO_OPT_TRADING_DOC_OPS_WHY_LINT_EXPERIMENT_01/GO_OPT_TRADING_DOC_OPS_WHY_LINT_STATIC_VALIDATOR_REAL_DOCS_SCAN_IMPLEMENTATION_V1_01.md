---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01
doc_type: chantier_child_implementation
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01
chantier_parent: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: child_implementation
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
  - no_ci_blocking
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md
  - tools/why_lint_static_validator/why_lint_static_validator.py
  - tests/why_lint_static_validator/test_why_lint_static_validator.py
  - tools/why_lint_static_validator/README.md
---

# GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01

## 1_MASTER_TARGET

Implement V1 of the real-document scan mode for the local WHY lint static validator.

The goal is to extend the existing read-only/report-only validator beyond fixture corpus validation, while keeping the first real-document scan deliberately bounded to the WHY lint parent chantier folder.

## 2_INITIAL_PROJECT_DOC

Parent reference:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
```

Real docs scan spec:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md
```

Current implementation document:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md
```

## 3_INITIAL_NEED

The validator already supports fixture corpus validation. The next safe step is a bounded scan mode for real Markdown documents.

The scan must remain:

- local;
- read-only;
- report-only;
- no runtime;
- no autofix;
- no CI blocking;
- no source mutation;
- no repo-wide scan.

## 4_MASTER_PROJECT_PLAN

1. Add a CLI option for real-document scan mode.
2. Restrict the V1 scan root to the WHY lint parent folder.
3. Scan only Markdown files in that folder.
4. Skip the fixture corpus file.
5. Detect missing required markers.
6. Detect forbidden runtime/autofix/CI implications.
7. Detect unexpected secret-like patterns.
8. Produce deterministic text and JSON reports.
9. Add unit tests for pass, findings, out-of-scope root, forbidden implication, and secret-like risk.
10. Update README.
11. Document the implementation.

## 6_FINAL_TARGET

**FINAL_TARGET: implement a bounded `--scan-docs` mode for the WHY lint static validator, limited to `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`, read-only/report-only, with deterministic reports and no mutation, no autofix, no runtime, and no CI blocking.**

## 7_CANONICAL_STATE

Established before this GO:

- parent consolidation merged;
- SPEC review merged;
- static validator spec merged;
- fixture corpus merged;
- read-only static validator implementation merged;
- real docs scan spec merged;
- no repo-wide scan was allowed by the spec.

Current GO adds the V1 scan implementation only.

## 8_VALIDATED_PLAN

Validated implementation scope:

- update `tools/why_lint_static_validator/why_lint_static_validator.py`;
- update `tests/why_lint_static_validator/test_why_lint_static_validator.py`;
- update `tools/why_lint_static_validator/README.md`;
- add this GO implementation document;
- no workflow;
- no active YAML/JSON files;
- no index mutation.

## 9_SELECTED_SOLUTION

Add a new mutually exclusive CLI input:

```text
--scan-docs <WHY_LINT_PARENT_FOLDER>
```

The V1 scan accepts only roots ending with:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
```

It scans `*.md` files in that folder, skipping the fixture corpus file.

## 10_SELECTED_SETUP

Changed files:

```text
tools/why_lint_static_validator/why_lint_static_validator.py
tools/why_lint_static_validator/README.md
tests/why_lint_static_validator/test_why_lint_static_validator.py
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md
```

No other surface should change.

## 11_KEY_DECISIONS

- V1 scan is not repo-wide.
- V1 scan is not CI-integrated.
- V1 scan does not write report files.
- V1 scan prints text or JSON to stdout.
- V1 scan returns exit code 1 when findings exist.
- V1 scan returns exit code 3 for unexpected secret-like risk.
- Fixture corpus validation remains backward-compatible.

## 12_INVARIANTS

- local only;
- read-only;
- report-only;
- deterministic;
- no runtime;
- no MCP live;
- no trade;
- no secret;
- no autofix;
- no CI blocking;
- no global index mutation;
- no source mutation;
- no repo-wide scan in V1;
- fail closed for out-of-scope scan roots.

## 13_ESTABLISHED

Implemented scan behaviors:

- `--scan-docs` CLI mode;
- V1 root restriction;
- Markdown-only scan;
- fixture corpus skip;
- required marker checks:
  - `WHY`;
  - `FINAL_TARGET`;
  - `12_INVARIANTS`;
  - `17_RESUME_POINT`;
- forbidden implication checks:
  - `autofix_allowed: true`;
  - `runtime_binding: true`;
  - `can_fail_ci: true`;
  - `execute_command: true`;
  - `apply_patch: true`;
- unexpected secret-like pattern checks;
- text report;
- JSON report;
- dedicated tests.

## 14_HYPOTHESIS

To validate later:

- whether the required marker set is sufficient;
- whether marker detection should be frontmatter-aware;
- whether V2 should scan all `docs/chantiers`;
- whether V2 should write report artifacts;
- whether R0-R5 severity should be tuned from real findings;
- whether CI should remain disabled permanently or only until a future GO.

## 15_REMAINING_GAP

- no repo-wide docs scan;
- no scan of `docs/governance`;
- no scan of `docs/index`;
- no persisted report file;
- no HTML report;
- no CI integration;
- no OpenClaw integration;
- no MCP integration;
- no auto-remediation.

## 16_TODO

Next safe sequence:

1. Merge this V1 implementation PR.
2. Run the V1 scan locally on the WHY lint parent folder.
3. Review findings without auto-remediation.
4. Open a report/triage GO if findings need documentation.
5. Only then consider a V2 scan expansion.

## 17_RESUME_POINT

After merge, resume with:

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01
```

Purpose:

```text
Run the V1 scan locally against the WHY lint parent folder and document the findings as a report, without changing scanned documents.
```

## 18_TO_DOCUMENT

TAGS:

- WHY_LINT_REAL_DOCS_SCAN_V1
- WHY_LINT_READONLY_SCAN
- WHY_LINT_REPORT_ONLY
- WHY_LINT_NO_AUTOFIX
- WHY_LINT_NO_CI_BLOCKING

Blocks to extract:

- `6_FINAL_TARGET`
- `12_INVARIANTS`
- `13_ESTABLISHED`
- `15_REMAINING_GAP`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

Memory Bricks candidates:

- `--scan-docs` V1 is bounded to `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`.
- The real-document scan is read-only/report-only and skips the fixture corpus file.
- V1 scan findings do not trigger autofix or CI blocking.
- Next safe GO is `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01`.

## Verdict

```text
PASS_REAL_DOCS_SCAN_IMPLEMENTATION_V1
```
