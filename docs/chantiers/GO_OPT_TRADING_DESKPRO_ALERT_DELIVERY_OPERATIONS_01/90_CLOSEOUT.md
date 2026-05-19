---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_OPERATIONS_01
doc_type: closeout
repo: opt-trading
status: CLOSED / MERGED
closed_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_OPERATIONS_01 — CLOSEOUT

## 7_CANONICAL_STATE

```text
ALERT_DELIVERY_OPERATIONS = CLOSED / MERGED
SOT_MAINLINE = UPDATED
UNITTEST = 107_PASS
CODE_CHANGES = NONE
RUNBOOK = DELIVERED
SECRETS = NOT_INCLUDED
```

## 13_ESTABLISHED

| Élément | État |
|---|---|
| Runbook opérationnel | livré — `ALERT_DELIVERY_OPERATIONS_RUNBOOK.md` |
| Variables env documentées | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `ALERT_WEBHOOK_URL`, `ALERT_COOLDOWN_SEC` |
| Launch command | `uvicorn modules.perf.app:app --host 0.0.0.0 --port 8010` |
| Fallback JSONL confirmé | `/opt/trading/tmp/desk_pro_alerts.jsonl` — alertes réelles seulement |
| Smoke test documenté | `POST /desk/alert/test` — no JSONL, no cooldown side-effect |
| Diagnostic complet | 6 étapes, sans afficher de secret |
| Non-fuite secret prouvée | booléens dans `/desk/status`, payload smoke sans token |
| Tests | 107/107 PASS |
| Patch de code | aucun |

## Nuance importante

```text
Smoke test (POST /desk/alert/test) :
  → dispatch Telegram/webhook si env configuré
  → NE TOUCHE PAS _alert_state (pas de cooldown)
  → N'ÉCRIT PAS dans JSONL

Alerte réelle (_check_alert, degraded/down) :
  → ÉCRIT dans JSONL AVANT dispatch
  → MET À JOUR _alert_state + cooldown
  → dispatch Telegram/webhook

Fallback JSONL = trace locale des alertes réelles uniquement
```
