# 20_OLLAMA_BASELINE_DIRECT

## /api/tags
```json
{"models":[{"name":"deepseek-r1:1.5b","model":"deepseek-r1:1.5b",...}]}
```
Modele `deepseek-r1:1.5b` visible et accessible.

## /api/generate direct smoke
```json
{
  "model": "deepseek-r1:1.5b",
  "response": "OK",
  "done": true,
  "done_reason": "stop",
  "total_duration": 1885333254,
  "eval_count": 6,
  "eval_duration": 335303839
}
```

## Verdict baseline directe
PASS — Ollama repond directement `"OK"` au prompt `"Reply OK only."`. Le modele fonctionne correctement en acces direct.
