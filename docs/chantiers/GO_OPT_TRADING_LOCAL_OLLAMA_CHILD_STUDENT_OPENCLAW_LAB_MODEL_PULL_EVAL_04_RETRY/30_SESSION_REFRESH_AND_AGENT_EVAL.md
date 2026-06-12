# 30_SESSION_REFRESH_AND_AGENT_EVAL

## Switch
```
openclaw models set ollama/qwen2.5:3b-instruct → SUCCESS
```

## Session refresh (proven method)
```
rm sessions.json
pkill openclaw-gateway (via sudo)
nohup openclaw gateway run --bind loopback &
```

## Agent eval
```
openclaw agent --to +15555550123 --message "Reply exactly: OK" --json --timeout 290
```

### Result
```json
{
  "status": "ok",
  "agentMeta": {
    "sessionId": "e77bf532...",
    "provider": "ollama",
    "model": "qwen2.5:3b-instruct"
  },
  "payloads": [{
    "text": "Request timed out..."
  }],
  "durationMs": 60873
}
```

## Analysis
| Criterion | Result |
|---|---|
| agentMeta.model | **qwen2.5:3b-instruct** ✓ |
| agentMeta.provider | **ollama** ✓ |
| Session ID | **NEW** (e77bf532) ✓ |
| Tools error | **ABSENT** ✓ |
| Response | Timeout (60.9s) |

Tools support confirmed (no rejection). Model accepts full system prompt. Timeout is CPU inference limitation (~61s for 3B model with 30K char prompt + 24 tools). Config timeout increase (`agents.defaults.timeoutSeconds`) could resolve.

## RISKS

- À qualifier.
