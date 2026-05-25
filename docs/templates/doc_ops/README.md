# Doc Ops Templates

This directory contains versioned templates for Doc Ops chantiers and inbox entries.

## Templates

### Initial Project Doc (`chantier_initial_project_doc_v1.md`)
- **Version**: v1
- **Usage**: Standard `00_INITIAL_PROJECT_DOC.md` for a new chantier.
- **Expected Placeholders**:
  - `{go_id}`: The GO ID of the project.
  - `{summary}`: A brief description of the project goal.
  - `{updated_at}`: Today's date (YYYY-MM-DD).

### Inbox Entry (`inbox_entry_v1.md`)
- **Version**: v1
- **Usage**: Entry in `docs/index/inbox/` for a new chantier.
- **Expected Placeholders**:
  - `{go_id}`: The GO ID of the project.
  - `{summary}`: A brief description of the project goal.

## Script Integration
These templates are used by `scripts/ai/workers/doc_ops_create_chantier.py`.

Example usage:
```bash
python3 scripts/ai/workers/doc_ops_create_chantier.py \
  --go-id GO_MY_PROJECT_01 \
  --template-version v1
```

## Known Limits
- Templates use simple Python string formatting (`{key}`). Placeholders must match exactly.
- Fallback inline templates are maintained within the script for cases where external templates are missing.
