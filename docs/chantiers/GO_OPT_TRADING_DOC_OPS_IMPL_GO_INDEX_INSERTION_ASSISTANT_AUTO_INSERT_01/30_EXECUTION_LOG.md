# 30_EXECUTION_LOG

## Step 1: Dry-run (pre-apply)
```
python3 scripts/ai/workers/doc_ops_go_index_insert.py \
  --go-id GO_OPT_TRADING_DOC_OPS_IMPL_GO_INDEX_INSERTION_ASSISTANT_AUTO_INSERT_01 \
  --dry-run --json
```
Result: status=PASS, duplicate=false, would_change=true

## Step 2: Apply
```
python3 scripts/ai/workers/doc_ops_go_index_insert.py \
  --go-id GO_OPT_TRADING_DOC_OPS_IMPL_GO_INDEX_INSERTION_ASSISTANT_AUTO_INSERT_01 \
  --apply --json
```
Result: status=PASS, entry inserted into GO_INDEX.md

## Step 3: Dry-run (post-apply)
```
python3 scripts/ai/workers/doc_ops_go_index_insert.py \
  --go-id GO_OPT_TRADING_DOC_OPS_IMPL_GO_INDEX_INSERTION_ASSISTANT_AUTO_INSERT_01 \
  --dry-run --json
```
Result: status=PASS, duplicate=true, would_change=false
