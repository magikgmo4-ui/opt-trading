# 40_TEST_PLAN

## Scope
Unit and integration tests in `tests/ai/workers/test_doc_ops_go_index_insert.py`.

## Test cases
| # | Test | Expected |
|---|------|----------|
| 1 | Valid GO_ID | entry generated |
| 2 | Invalid GO_ID | FAIL (exit 1) |
| 3 | Missing initial doc | FAIL (exit 2) |
| 4 | Missing index file | detected gracefully |
| 5 | Dry-run does not modify index | index unchanged |
| 6 | --apply modifies tmp copy | entry inserted |
| 7 | Duplicate detection | FAIL |
| 8 | JSON output parseable | valid JSON with status |
| 9 | Extract 1_MASTER_TARGET | content extracted |
| 10 | Extract 6_FINAL_TARGET | content extracted |
| 11 | Parent GO_ID detection | entry type adjusted |

## Running
```bash
python3 -m pytest tests/ai/workers/test_doc_ops_go_index_insert.py -q
```
