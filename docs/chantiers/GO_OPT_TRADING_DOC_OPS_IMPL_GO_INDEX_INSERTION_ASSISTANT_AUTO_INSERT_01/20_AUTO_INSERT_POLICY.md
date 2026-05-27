# 20_AUTO_INSERT_POLICY

## Rules
1. Only one entry per PR.
2. Use the assistant tool `doc_ops_go_index_insert.py`.
3. Dry-run before apply to confirm duplicate=false.
4. Apply only if duplicate=false.
5. Verify duplicate=true after apply.
6. No batch insertion.
7. No modification of the assistant tool.

## This execution
- Target: `docs/index/GO_INDEX.md`
- Entry: `GO_OPT_TRADING_DOC_OPS_IMPL_GO_INDEX_INSERTION_ASSISTANT_AUTO_INSERT_01`
- Applied: yes
