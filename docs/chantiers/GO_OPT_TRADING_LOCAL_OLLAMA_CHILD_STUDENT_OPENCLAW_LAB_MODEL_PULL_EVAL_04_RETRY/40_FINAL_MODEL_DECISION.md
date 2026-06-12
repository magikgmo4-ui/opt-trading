# 40_FINAL_MODEL_DECISION

## qwen2.5:3b-instruct RETAINED as final lab model

## Comparison across all models tested

| Model | Size | Tools | Agent | Verdict |
|---|---|---|---|---|
| deepseek-r1:1.5b | 1.1 GB | NO | REJECT (400) | Lab only |
| qwen2.5:0.5b | 397 MB | YES | Timeout (61s) | Too small |
| qwen2.5:1.5b | 986 MB | YES | Timeout (61s) | Undersized |
| **qwen2.5:3b** | **1.9 GB** | **YES** | **Timeout (61s)** | **BEST** |

## ACCEPTABLE_FOR
- OpenClaw agent (tools supported, no rejection)
- Lab experimentation
- Sanity smoke tests
- Routing/provider validation

## NOT_ACCEPTABLE_FOR
- Real-time agent responses (CPU inference too slow)
- Production workloads without GPU
- Tasks requiring sub-60s latency

## Limitation
All qwen2.5 models timeout at ~61s because OpenClaw's default `agents.defaults.timeoutSeconds` is too low for CPU inference on a 3B model with full tool schemas. Increasing this config value should resolve the timeout. A GPU would eliminate this limitation entirely.

## Model final actif
```
ollama/qwen2.5:3b-instruct
```

## RISKS

- À qualifier.
