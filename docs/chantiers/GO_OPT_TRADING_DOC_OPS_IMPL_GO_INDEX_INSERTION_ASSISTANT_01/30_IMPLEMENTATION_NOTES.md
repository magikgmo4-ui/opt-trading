# 30_IMPLEMENTATION_NOTES

## Design
- The script `doc_ops_go_index_insert.py` is a standalone CLI tool.
- It reuses the same GO_ID regex as `doc_ops_create_chantier.py`.
- It parses the initial project doc frontmatter and sections.
- Entry generation follows the existing format in `docs/index/GO_INDEX.md`.

## Safety
- Default mode is dry-run (preview + diff).
- `--apply` requires explicit user opt-in.
- Duplicate entries are rejected.
- Exit codes: 0 PASS, 1 violation/duplicate, 2 missing file.

## CLI interface
```
python3 scripts/ai/workers/doc_ops_go_index_insert.py --go-id <GO_ID> --dry-run
python3 scripts/ai/workers/doc_ops_go_index_insert.py --go-id <GO_ID> --apply
python3 scripts/ai/workers/doc_ops_go_index_insert.py --go-id <GO_ID> --json
python3 scripts/ai/workers/doc_ops_go_index_insert.py --go-id <GO_ID> --entry-status ACTIVE
python3 scripts/ai/workers/doc_ops_go_index_insert.py --go-id <GO_ID> --section "Entrées"
```
