# 90_CLOSEOUT

## Etat de depart
- Disk fix PASS (`c772037`), storage on /home, 2.8 GB free on /
- 3 models, qwen2.5:1.5b active, tools OK but timeout

## Commandes executees
- `timeout 3600s ollama pull qwen2.5:3b-instruct` → SUCCESS
- `openclaw models set ollama/qwen2.5:3b-instruct` → SUCCESS
- Session refresh (rm sessions.json + pkill + restart gateway)
- `openclaw agent "Reply exactly: OK"` → model=qwen2.5:3b-instruct, tools OK, timeout 61s

## Runtime student modifie
- `/home/ollama-models/` : +qwen2.5:3b-instruct (~1.9 GB)
- `/home/openclaw-lab/.openclaw/openclaw.json` : defaultModel → ollama/qwen2.5:3b-instruct
- Gateway restarted (new session e77bf532)
- models.json, auth-profiles.json: unchanged

## Verdict
**PASS** — qwen2.5:3b-instruct pulled, evaluated, and retained as final lab model. Tools support confirmed. Timeout limitation documented (CPU inference, config tunable).

## Next GO
`GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_TIMEOUT_TUNING_01`
