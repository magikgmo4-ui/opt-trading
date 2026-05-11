# 10_PREFLIGHT_AFTER_DISK_FIX

## Disk
| Partition | Usage | Free |
|---|---|---|
| `/` (28 GB) | 90% | 2.8 GB |
| `/home` (200 GB) | 5% | 182 GB |

## OLLAMA_MODELS
```
Environment=OLLAMA_MODELS=/home/ollama-models
```
Confirmed via `systemctl show ollama -p Environment`.

## Models before pull
- qwen2.5:1.5b-instruct (1.5B)
- qwen2.5:0.5b-instruct (494M)
- deepseek-r1:1.5b (1.8B)

## Active model
- OpenClaw defaultModel: `ollama/qwen2.5:1.5b-instruct`
- missingProvidersInUse: `[]`
- Health: OK
- Listeners: loopback-only
