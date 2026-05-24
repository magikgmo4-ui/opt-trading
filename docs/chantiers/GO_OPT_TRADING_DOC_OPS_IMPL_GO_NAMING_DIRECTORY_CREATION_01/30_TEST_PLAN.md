# 30_TEST_PLAN

## Unit Tests (`tests/ai/workers/test_doc_ops_create_chantier.py`)
- Test `validate_go_id` with various strings (valid, lowercase, no suffix, symbols).
- Test directory creation in a temporary sandbox.
- Test template generation.
- Test `--dry-run` prevents any writes.
- Test `--force` behavior on existing files.
- Test `--create-inbox` adds the expected file.

## Integration Tests
- Run the script against the current GO_ID in dry-run mode and check JSON output.
