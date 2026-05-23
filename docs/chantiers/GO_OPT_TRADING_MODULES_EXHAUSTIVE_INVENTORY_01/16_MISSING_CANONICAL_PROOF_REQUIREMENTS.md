---
doc_id: GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01_MISSING_CANONICAL_PROOF_REQUIREMENTS
doc_type: proof_requirements
repo: opt-trading
project: opt-trading
status: blocked_with_reason
mode: doc-only
surface: modules
source_kind: local_inventory_followup
---

# 16_MISSING_CANONICAL_PROOF_REQUIREMENTS

## 13_ESTABLISHED

The current module inventory normalization produced:

- raw `modules/` first-level directory count: `100`
- clean functional candidate count after technical exclusions: `98`
- historical canonical audit reference count: `87`
- normalized divergence: `98 != 87`
- `POST_AUDIT_NEW_MODULES` block exists in:
  - `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/15_POST_AUDIT_NEW_MODULES_HEURISTIC.md`

A heuristic list of `36` candidates not explicitly mentioned in the canonical module-family audit exists, but this does **not** prove which exact modules are new versus simply absent from the textual audit summary.

## 14_HYPOTHESIS

The `+11` normalized delta may come from one or more of:

- modules added after the historical audit;
- modules present during the audit but not listed in the summary;
- modules counted differently by the old audit method;
- support/tooling directories now treated as modules;
- registry or tree drift since the audit baseline.

## 15_REMAINING_GAP

The exact delta cannot be closed without one of the following proof sources:

1. the historical flat list of the original `87` audited modules;
2. the original audit artifact/script output that generated the `87` count;
3. a commit/branch snapshot matching the audit date, then re-running the same inventory rule;
4. a maintained registry snapshot contemporaneous with the audit.

Without one of these, the repo can prove:

- current normalized inventory = `98`
- historical audit reference = `87`

But it cannot prove the exact identity of the `11` net additions.

## 12_INVARIANTS

- Do not rewrite the historical `87` count.
- Do not promote `98` as the new canonical count without proof.
- Do not proceed to physical consolidation based only on heuristic delta.
- Do not update `registry/modules_registry.yaml` in this GO.
- Keep this GO `doc-only`.

## 16_TODO

- Search for a historical flat module list artifact.
- Search previous audit scripts or generated outputs.
- If no source exists, create a new canonical baseline from the current normalized `98`.
- Mark the baseline as `CURRENT_BASELINE_2026_05_20`, not as a replacement for the historical `87`.
- Use the current baseline for future consolidation only after explicit validation.

## NEXT_GO

`GO_OPT_TRADING_MODULES_CURRENT_BASELINE_CANONIZATION_01`

## GOAL

Create a current canonical module baseline from the normalized inventory, while preserving the historical `87` as an audit-era reference.

## VERDICT

`BLOCKED_WITH_REASON`

The normalized module inventory divergence is confirmed, but the exact historical delta cannot be proven without an additional canonical proof source.
