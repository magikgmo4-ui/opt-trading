# 20_QWEN3_PULL_AND_DIRECT_EVAL

## Pull
- `timeout 3600s ollama pull qwen2.5:3b-instruct`
- Size: 1.9 GB
- Speed: 1.3 MB/s stable
- Result: SUCCESS, sha256 verified

## Disk after pull
| Partition | Free |
|---|---|
| `/` | 2.8 GB |
| `/home` | 180 GB |

## Models (4 total)
```
qwen2.5:3b-instruct     3.1B   NEW
qwen2.5:1.5b-instruct    1.5B
deepseek-r1:1.5b         1.8B
qwen2.5:0.5b-instruct    494M
```

## Ollama direct eval
```
"Reply exactly: OK" → "OK" (4.3s, clean)
```
PASS.
