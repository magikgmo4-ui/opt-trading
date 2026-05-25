# 10_SOURCE_SPEC

## Goal
Implement a versioned template system for Doc Ops chantiers, allowing the creation helper to load external templates while maintaining a robust fallback mechanism.

## Requirements
- Support `--template-version` (e.g., `v1`).
- Support `--template-dir` (default: `docs/templates/doc_ops`).
- Templates stored as external Markdown files.
- Fallback to inline templates if external files are missing (unless version specified).
- Exit code 2 if a requested version is explicitly missing.

## Success Criteria
- Script loads `v1` templates from `docs/templates/doc_ops`.
- Templates correctly receive `{go_id}`, `{summary}`, and `{updated_at}`.
- Tests cover external loading and error cases.
- Documentation includes a README in the templates directory.
