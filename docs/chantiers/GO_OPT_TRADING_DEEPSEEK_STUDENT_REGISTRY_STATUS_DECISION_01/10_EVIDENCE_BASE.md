---
go_id: GO_OPT_TRADING_DEEPSEEK_STUDENT_REGISTRY_STATUS_DECISION_01
doc_type: EVIDENCE_BASE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 10_EVIDENCE_BASE

## Established facts

1. Family decision already classifies `deepseek_student` as legacy/transitional and not the canonical runtime truth.

2. `modules/deepseek_student/README.md` states explicitly:
- not the current runtime truth
- active logic is in `scripts/student/`
- canonical target workspace is `student/scripts/`
- module is awaiting migration/consolidation

3. `student/scripts/MIGRATION_STATUS.md` states:
- `student/scripts/` is the official operator workspace
- `scripts/student/` is still a legacy active directory kept for compatibility
- callers are not fully retired

4. `scripts/ai/menu/opt_trading_menu.json` places `deepseek_student` under archived/closed entries.

5. `docs/product/PRODUCT_USAGE_MATRIX.md` still exposes a bounded product-level usability view: `USABLE_LIMITED`.

## Interpretation

These signals are not a simple status mismatch inside one central registry.

They show a split between:

- product-level bounded usability,
- family-level legacy/transitional role,
- module-level non-canonical state,
- runtime-level migration not fully closed.

## Consequence for central registries

Adding `deepseek_student` now to `registry/modules_registry.yaml` would describe a module object whose physical/runtime boundary is still unresolved and whose current module path is explicitly non-canonical.
