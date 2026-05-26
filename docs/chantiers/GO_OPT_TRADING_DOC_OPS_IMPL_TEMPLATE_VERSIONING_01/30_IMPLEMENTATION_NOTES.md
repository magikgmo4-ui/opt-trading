# 30_IMPLEMENTATION_NOTES

## Changes in `doc_ops_create_chantier.py`
- Added `load_template` helper function.
- Modified `create_chantier` to accept `template_version` and `template_dir`.
- Templates are loaded before file creation.
- Result JSON includes `info` field with template loading status.
- Specific exit code 2 for missing templates when requested.

## Fallback Mechanism
If `--template-version` is not provided, the script uses internal `INITIAL_DOC_FALLBACK` and `INBOX_FALLBACK` strings to ensure functionality even if `docs/templates/` is missing or inaccessible.
