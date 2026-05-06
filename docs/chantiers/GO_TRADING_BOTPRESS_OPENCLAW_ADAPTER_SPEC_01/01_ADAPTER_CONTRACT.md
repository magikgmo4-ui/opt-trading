---
doc_id: GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01_CONTRACT
doc_type: api_contract
repo: opt-trading
go_id: GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01
status: open
lifecycle_stage: specification
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01/00_CADRAGE.md
---

# 01_ADAPTER_CONTRACT — Botpress ↔ OpenClaw

## Endpoints

| Direction | Method | Path | Role |
| --- | --- | --- | --- |
| Botpress → Adapter | POST | `/api/v1/botpress/intent` | Recevoir intent classifie |
| Adapter → OpenClaw | POST | `http://<openclaw>:<port>/api/v1/execute` | Transmettre au gateway |
| Adapter → Botpress | JSON response | — | Reponse formatee |

## Intent → Gateway Route Mapping

| Intent | Gateway action | Read-only | Safety |
| --- | --- | --- | --- |
| `screener` | `market_scan` | Oui | Liste blanche |
| `analysis` | `analyze_symbol` | Oui | Liste blanche |
| `journal` | `query_journal` | Oui | Liste blanche |
| `status` | `cockpit_status` | Oui | Liste blanche |
| `help` | `static_help` | Oui | Liste blanche |
| `backtest_run` | `run_backtest` | Oui | Confirmation |
| `execute_trade` | BLOQUE | Non | Blocage permanent |

## Request Schema (Botpress → Adapter)

```json
{
  "botpress_event_id": "uuid",
  "telegram_chat_id": "string",
  "telegram_user_id": "string",
  "intent": "screener|analysis|journal|status|help|backtest_run",
  "original_message": "string",
  "parsed_params": {
    "symbol": "BTCUSDT",
    "timeframe": "1h",
    "limit": 10
  },
  "session_context": {
    "previous_intents": ["status"],
    "session_started_at": "ISO-8601"
  }
}
```

## Request Schema (Adapter → OpenClaw)

```json
{
  "intent": "screener",
  "context": {
    "user_id": "telegram_<chat_id>",
    "symbol": "BTCUSDT",
    "timeframe": "1h"
  },
  "payload": {
    "query": "market scan BTCUSDT 1h",
    "attachments": []
  },
  "options": {
    "dry_run": true,
    "max_symbols": 5,
    "timeout_ms": 30000
  }
}
```

## Response Schema (OpenClaw → Adapter)

```json
{
  "status": "ok|error|timeout|blocked",
  "intent": "screener",
  "result": {
    "data": {},
    "summary": "string (Markdown)",
    "actions_taken": [],
    "warnings": []
  },
  "trace_id": "uuid"
}
```

## Response Schema (Adapter → Botpress)

```json
{
  "botpress_event_id": "uuid",
  "status": "ok|error|timeout|blocked",
  "reply_text": "string (Markdown pour Telegram)",
  "reply_data": {},
  "safety_check": "passed|blocked|confirmed",
  "trace_id": "uuid",
  "duration_ms": 1234
}
```

## Timeout & Retry

| Scenario | Timeout | Retry | Fallback |
| --- | --- | --- | --- |
| Gateway OK | < 30s | 0 | — |
| Gateway timeout | > 30s | 1 | "Analyse en cours..." |
| Gateway error | — | 1 | "Erreur, reessaie" |
| Gateway blocked | — | 0 | "Action bloquee V1" |

## Journalisation

Chaque requete est loggee:

```json
{
  "timestamp": "ISO-8601",
  "botpress_event_id": "uuid",
  "telegram_user_id": "string",
  "intent": "screener",
  "gateway_status": "ok",
  "safety_status": "passed",
  "trace_id": "uuid",
  "duration_ms": 1234
}
```

Log destination: Airtable (`Botpress_Logs`) ou `~opt-trading/journal/` local.
