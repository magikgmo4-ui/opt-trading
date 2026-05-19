---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01
doc_type: chantier_child_review
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01
chantier_parent: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: child_review
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-14
topic_keys:
  - why_lint
  - spec_review
  - consolidation
  - governance
  - runtime_security
  - why_runtime_graph
  - openclaw_central
  - warning_only
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_CONSOLIDATION_MAP_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/05_WHY_LINT_WARNING_MODEL_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/06_CROSS_AXIS_GATE_BINDING_01.md
---

# GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01

## 1_MASTER_TARGET

Review `SPEC_WHY_LINT_EXPERIMENT_01.md` after merge of the consolidation parent, before any technical lint implementation.

The target is to confirm whether the SPEC is sufficiently stable to serve as the parent reference for future child GO workstreams: static validator spec, fixture corpus, and possible later implementation.

## WHY

This review exists to verify that the merged parent SPEC can safely anchor the next child GO sequence before any validator code, fixture expansion, or runtime-adjacent work is opened.

## 3_INITIAL_NEED

PR #416 merged the parent consolidation plan for four axes:

1. Gouvernance.
2. WHY / WHY-runtime graph.
3. WHY lint.
4. OpenClaw central operational orchestrator.

Before opening a technical lint implementation, the SPEC must be reviewed for:

- boundary clarity;
- no-duplication rules;
- warning-only invariants;
- runtime exclusion;
- gate / trace / eval binding;
- source authority;
- unresolved gaps.

## 6_FINAL_TARGET

**FINAL_TARGET: validate `SPEC_WHY_LINT_EXPERIMENT_01.md` as a doc-only parent SPEC, with explicit gaps isolated, and confirm the next child GO should remain documentation-only: static validator specification before any code or runtime binding.**

## 7_CANONICAL_STATE

Current established parent state:

- parent GO: `GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`;
- parent PR merged into `sot/mainline`;
- branch for this child review: `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01`;
- reviewed file: `SPEC_WHY_LINT_EXPERIMENT_01.md`;
- scope: documentation only;
- no runtime;
- no auto-fix;
- no CI blocking;
- no global index mutation.

## 8_VALIDATED_PLAN

Review steps:

1. Read `SPEC_WHY_LINT_EXPERIMENT_01.md`.
2. Verify parent target and WHY.
3. Verify four-axis consolidation model.
4. Verify no-duplication doctrine.
5. Verify warning-only constraints.
6. Verify gate / trace / eval binding.
7. Identify blocking gaps.
8. Decide next safe GO.

## 9_SELECTED_SOLUTION

Use a child review document rather than modifying the parent SPEC immediately.

Reason:

- the parent SPEC is already merged;
- review findings should remain additive;
- any future SPEC patch should be a separate GO only if needed;
- this avoids mixing review, rewrite, and implementation.

## 11_KEY_DECISIONS

- The SPEC correctly defines WHY lint as a warning-only consolidation layer.
- The SPEC correctly states that WHY lint does not authorize actions.
- The SPEC correctly prevents WHY lint from becoming a fifth source of truth.
- The SPEC correctly binds itself to governance, runtime security, WHY runtime graph, and OpenClaw central target.
- The SPEC correctly excludes runtime, auto-fix, CI blocking, MCP live, secrets, and trade.
- The SPEC correctly routes future work toward a static validator spec before any implementation.

## 12_INVARIANTS

- Doc-only review.
- No runtime.
- No MCP live.
- No secret.
- No trade.
- No shell operation.
- No auto-fix.
- No global index mutation.
- No parent SPEC rewrite in this child review.
- Any implementation requires a future GO.

## 13_ESTABLISHED

The SPEC contains the required core bindings:

- `Governance Binding`;
- `Runtime Security Binding`;
- `WHY Runtime Graph Binding`;
- `OpenClaw Central Target Binding`;
- `No Duplication Rules`;
- `Warning Model`;
- `Gate / Trace / Eval Binding`;
- `No Runtime / No Autofix / No CI Blocking`;
- `Future Implementation Path`.

The SPEC also establishes the intended perpetual behavior of WHY lint:

```text
WHY lint detects and reports only.
WHY lint does not authorize actions.
WHY lint does not replace governance.
WHY lint does not replace runtime security.
WHY lint does not replace WHY/runtime graph.
WHY lint does not define OpenClaw central target.
```

## Review matrix

| Area | Review verdict | Notes |
| --- | --- | --- |
| Parent target | PASS | FINAL_TARGET is explicit. |
| WHY section | PASS | The reason for the chantier is clear. |
| Four-axis consolidation | PASS | Axes are separated and bounded. |
| No-duplication rules | PASS | Each axis has a distinct authority. |
| Warning model | PASS_WITH_GAP | Families exist; future rule catalog still needed. |
| Gate binding | PASS_WITH_GAP | Gates exist; future trace/eval schema still needed. |
| Runtime exclusion | PASS | No runtime binding allowed. |
| Auto-fix exclusion | PASS | `autofix_allowed: false` doctrine established. |
| CI blocking exclusion | PASS | `can_fail_ci: false` doctrine established. |
| Source manifest | PASS_WITH_GAP | Some OpenClaw governance sources are referenced as absent. |
| Implementation readiness | NOT_READY_BY_DESIGN | Next step is spec, not code. |

## 14_HYPOTHESIS

To validate later:

- whether the missing OpenClaw governance documents should be imported, mirrored, or treated as external session history;
- whether the warning families need a normalized error-code catalog;
- whether R0-R5 severity should be reused exactly from WHY/runtime overlays;
- whether future lint fixtures should be Markdown-only first;
- whether future implementation should parse Markdown, YAML, or both.

## 15_REMAINING_GAP

Non-blocking gaps for this review:

1. OpenClaw governance session docs referenced in the plan are not all present in the repo.
2. Warning families are defined, but individual lint rules are not yet enumerated.
3. Gate binding exists at family level, but not at rule-level.
4. Trace/eval requirements exist conceptually, but not as schemas.
5. No fixture corpus exists yet for WHY lint.
6. No static validator spec exists yet for WHY lint.
7. No implementation should start until the static validator spec is written.

## 16_TODO

Next safe sequence:

1. Merge this review PR.
2. Open child GO: `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01`.
3. Define static validator inputs/outputs, rule schema, verdicts, no-secret checks, warning catalog, and fail-closed behavior.
4. Then open a fixture corpus GO.
5. Only after that evaluate implementation.

## 17_RESUME_POINT

After this child review is merged, resume from:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
```

Recommended next GO:

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01
```

Purpose:

```text
Define the future static validator specification for WHY lint, still doc-only, warning-only, no runtime, no auto-fix, and no CI blocking.
```

## 18_TO_DOCUMENT

TAGS:

- WHY_LINT_SPEC_REVIEW
- WHY_LINT_PARENT_VALIDATED
- WHY_LINT_STATIC_VALIDATOR_NEXT
- WHY_LINT_NO_RUNTIME
- WHY_LINT_WARNING_ONLY

Blocks to extract:

- `Review matrix`
- `15_REMAINING_GAP`
- `16_TODO`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

Memory Bricks candidates:

- `SPEC_WHY_LINT_EXPERIMENT_01.md` is valid as a doc-only parent SPEC.
- The next safe GO is `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01`.
- WHY lint must remain warning-only, no runtime, no auto-fix, no CI blocking.
- Missing OpenClaw governance source documents are a non-blocking gap to reconcile later.

## Verdict

```text
PASS_SPEC_REVIEW_DOC_ONLY
```
