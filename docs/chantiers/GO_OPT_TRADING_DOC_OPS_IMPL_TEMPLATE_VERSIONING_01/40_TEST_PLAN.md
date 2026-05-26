# 40_TEST_PLAN

## Automated Tests
- `test_external_template_v1`: Verifies loading of v1 templates from a temporary directory.
- `test_missing_template_version_fails`: Verifies exit code 2 when a version is requested but missing.
- `test_main_exit_code_2_on_missing_template`: Verifies stderr output and exit code in `main()`.

## Manual Verification
- Dry-run with `--template-version v1` and `--json`.
- Verify `info` field in JSON shows `loaded:docs/templates/doc_ops/...`.
