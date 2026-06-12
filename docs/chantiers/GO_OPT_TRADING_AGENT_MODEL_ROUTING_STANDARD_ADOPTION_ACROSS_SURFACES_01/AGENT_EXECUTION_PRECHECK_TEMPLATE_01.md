# AGENT_EXECUTION_PRECHECK_TEMPLATE_01

Checklist pré-exécution agent, toutes surfaces.

```yaml
precheck:
  surface: "student-ollama-local|distant-ssh|distant-api|gpu-local"
  gateway_live: true|false
  session:
    fresh: true|false
    rotated: true|false
    runs_count: 0
  provider:
    selected: "0.5b-agent-chain|1.5b-direct|deepseek-direct|refus"
    fallback_planned: "1.5b-direct|deepseek-direct|refus"
  task:
    type: "smoke|diagnostic|read-only|format-exact|raisonnement"
    risk: "faible|moyen|élevé|bloqué"
    trading_related: true|false
  no_unauthorized_trade_worker: true|false
  prewarm_ok: true|false
  result:
    authorized: true|false
    notes: ""
```

## RISKS

- À qualifier.
