# ROUTING_DECISION_TEMPLATE_01

Template à remplir avant chaque exécution agent.

```yaml
routing_decision:
  task:
    description: "description courte de la tâche"
    type: "smoke|diagnostic|read-only|format-exact|raisonnement"
    risk: "faible|moyen|élevé|bloqué"
    format: "libre|exact|structuré"
    latency_tolerant: true|false

  provider:
    selected: "qwen2.5:0.5b-instruct|qwen2.5:1.5b-instruct|deepseek-r1:1.5b|refus"
    pipeline: "agent-chain|direct-ollama|refus"
    reason: "justification du choix selon la politique de routage"

  session:
    fresh: true|false
    rotated: true|false
    id: "session-uuid"

  fallback:
    planned: "1.5b-direct|deepseek-direct|refus"
    executed: true|false
    result: "PASS|FAIL|NOT_NEEDED"

  precheck:
    gateway_live: true|false
    prewarm_ok: true|false
    no_trade_worker: true|false

  result:
    duration_ms: 0
    input_tokens: 0
    status: "PASS|FAIL|REFUS"
    notes: ""
```

## RISKS

- À qualifier.
