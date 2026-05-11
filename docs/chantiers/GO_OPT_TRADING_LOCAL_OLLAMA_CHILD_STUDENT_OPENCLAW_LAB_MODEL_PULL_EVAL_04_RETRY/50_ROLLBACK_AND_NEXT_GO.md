# 50_ROLLBACK_AND_NEXT_GO

## Rollback
Non execute. qwen2.5:3b-instruct retained as final model.

## Rollback available
```
openclaw models set ollama/deepseek-r1:1.5b
# + session refresh (rm sessions.json + gateway restart)
```

## Final state
- defaultModel: `ollama/qwen2.5:3b-instruct`
- missingProvidersInUse: `[]`
- Models: 4 (deepseek-r1 1.1 GB + qwen 0.5b 397 MB + qwen 1.5b 986 MB + qwen 3b 1.9 GB)
- Disk /: 90% (2.8 GB), /home: 180 GB
- Health: OK, local-only

## Next GO
`GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_TIMEOUT_TUNING_01`

Increase `agents.defaults.timeoutSeconds` to accommodate CPU inference latency (~120-180s), then retest agent with qwen2.5:3b-instruct.
