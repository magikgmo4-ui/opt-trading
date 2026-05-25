# 10_SOURCE_SPEC

## Derived from
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01/50_NEXT_IMPLEMENTATION_GO_SPEC.md`

## Requirements
- CLI Interface: `python3 scripts/ai/workers/doc_ops_create_chantier.py --go-id <GO_ID>`
- GO_ID Validation:
    - Starts with `GO_`
    - Uppercase only
    - Underscores only
    - Numeric suffix `_NN`
- Actions:
    - Create `docs/chantiers/<GO_ID>/`
    - Create `docs/chantiers/<GO_ID>/00_INITIAL_PROJECT_DOC.md` from template
    - (Optional) Create `docs/index/inbox/<GO_ID>.md`
- Safety:
    - Do not overwrite unless `--force`
    - `--dry-run` mode
    - `--json` output
