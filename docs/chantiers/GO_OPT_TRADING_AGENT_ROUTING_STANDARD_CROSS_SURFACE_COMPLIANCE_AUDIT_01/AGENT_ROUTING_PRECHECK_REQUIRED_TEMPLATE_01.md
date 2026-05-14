# AGENT_ROUTING_PRECHECK_REQUIRED_TEMPLATE_01

Template de précheck obligatoire pour toute nouvelle surface agent.

```yaml
surface_compliance_audit:
  surface_name: "nom-de-la-surface"
  audit_date: "YYYY-MM-DD"

  has_agent_configured: true|false
  if_false:
    action: "AUCUN_AUDIT_REQUIS"

  if_true:
    provider_documented: true|false
    routing_policy_defined: true|false
    capability_gate_active: true|false
    fallback_ladder_defined: true|false
    decision_tracing_active: true|false
    session_fresh_required: true|false
    rotation_after_10runs: true|false
    no_unauthorized_trade_worker: true|false

    compliant: true|false
    if_false:
      blocking_issues:
        - "description du manquement"
      required_actions:
        - "action corrective"

    notes: ""
```
