---
doc_id: GO_OPT_TRADING_MODULES_CURRENT_BASELINE_CANONIZATION_01
doc_type: baseline_canonization
repo: opt-trading
project: opt-trading
status: pass
mode: doc-only
surface: modules
source_kind: normalized_local_inventory
baseline_id: CURRENT_BASELINE_2026_05_20
---

# 17_CURRENT_BASELINE_CANONIZATION

## Purpose

Canonize the current normalized module inventory as the working baseline for future module-family consolidation, while preserving the historical `87` as an audit-era reference.

## Established

- historical canonical audit reference: `87`
- current raw first-level `modules/` directory count: `100`
- technical exclusions confirmed: `2`
- current normalized functional candidate count: `98`
- current normalized registry mention count: `32`
- current normalized registry missing review count: `66`

## Canonized baseline

The repo baseline canonized by this GO is:

`CURRENT_BASELINE_2026_05_20`

## Canonical artifacts

The following files are the canonical artifacts of `CURRENT_BASELINE_2026_05_20`:

1. `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/11_MODULES_CLEAN_FUNCTIONAL_CANDIDATES.list`
2. `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv`
3. `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/14_NORMALIZED_INVENTORY_SUMMARY.md`
4. `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/15_POST_AUDIT_NEW_MODULES_HEURISTIC.md`
5. `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/16_MISSING_CANONICAL_PROOF_REQUIREMENTS.md`

## Scope of validity

`CURRENT_BASELINE_2026_05_20` is valid as:

- the current operational module baseline for ongoing cartography;
- the current working input for family consolidation decisions;
- the current source of truth for normalized module presence under `modules/`.

It is **not** valid as:

- a rewrite of the historical `87` reference;
- proof that the exact `+11` delta has been historically identified;
- a reason to silently replace prior audit evidence.

## Invariants

- Keep the historical `87` as an audit-era reference.
- Use `98` only as the current normalized baseline.
- Do not collapse historical and current baselines into a single number.
- Do not treat heuristic post-audit candidates as proven net additions.
- Do not update `registry/modules_registry.yaml` in this GO.

## Operational rule

Until a stronger historical proof source is found, all future family consolidation work must reference:

- historical baseline reference: `87`
- current working baseline: `CURRENT_BASELINE_2026_05_20 = 98`

## Next GO

Use `CURRENT_BASELINE_2026_05_20` as the working baseline for the next family-level consolidation GO.

Priority order remains:

1. `GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01`
2. `GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01`
3. `GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01`
4. `GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01`

## Verdict

`PASS`

The current normalized inventory is canonized as `CURRENT_BASELINE_2026_05_20` for forward-looking consolidation work, without overwriting the historical `87` audit reference.
