# 00_START
## Contexte
- Disk fix PASS (`c772037`) — Ollama storage migrated to /home
- Root free: ~2.8 GB, /home free: ~182 GB
- 3 models present, need 4th: qwen2.5:3b-instruct

## Objectif
Pull qwen2.5:3b-instruct, apply proven session refresh method, evaluate as final lab model.

## Regle cle
- Use validated refresh: rm sessions.json + pkill gateway + restart
