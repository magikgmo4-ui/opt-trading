---
doc_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01_ALERTING
doc_type: ci_alerting
go_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01
status: draft
---

# 50_ALERTING.md

## Canaux d'alerting

| Canal | Usage | Priorité | Template |
|---|---|---|---|
| **Telegram** | Échecs critiques, dead-letter threshold, kill switch activation | Haute | `[ALERT] <level>: <summary> — <action_required>` |
| **Ledger** | Tous les événements (G06) | Tous | Event JSON structuré |
| **Health Status** | Check périodique de santé (G09) | Monitoring | JSON formaté |

## Règles d'alerting

```yaml
alerting_rules:
  - trigger: "dead_letter_count >= 3 in 1 hour"
    channel: telegram
    message: "Dead-letter threshold exceeded: {count} events in 1h"
  - trigger: "kill_switch != NORMAL"
    channel: telegram
    message: "Kill switch activated: {state} — immediate attention required"
  - trigger: "ledger FAIL rate > 20% in 5 min"
    channel: telegram
    message: "High failure rate: {rate}% in last 5 min"
  - trigger: "systemd timer inactive > 5 min"
    channel: telegram
    message: "Timer {timer_name} inactive for >5 min"
```
