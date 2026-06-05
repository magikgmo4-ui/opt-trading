---
doc_id: GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01_API_CONTRACT
doc_type: api_contract
repo: opt-trading
go_id: GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01
status: open
lifecycle_stage: specification
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/00_cadrage_parent.md
---

# 04_API_CONTRACT — OpenClaw Gateway ← Botpress

## Endpoint OpenClaw Gateway

```
POST http://<openclaw_host>:<port>/api/v1/execute
```

## Auth

```
Header: Authorization: Bearer <OPENCLAW_TOKEN>
```

Le token est dans `.env` local, jamais committe.

## Request (Botpress → Gateway)

```json
{
  "intent": "screener|analysis|journal|status|help",
  "context": {
    "user_id": "telegram_<chat_id>",
    "symbol": "BTCUSDT",
    "timeframe": "1h"
  },
  "payload": {
    "query": "message utilisateur original ou parse",
    "attachments": []
  },
  "options": {
    "dry_run": true,
    "max_symbols": 5,
    "timeout_ms": 30000
  }
}
```

## Response (Gateway → Botpress)

```json
{
  "status": "ok|error|timeout|blocked",
  "intent": "screener",
  "result": {
    "data": {},
    "summary": "resume Markdown",
    "actions_taken": [],
    "warnings": []
  },
  "trace_id": "uuid"
}
```

## Intents V1

| Intent | Description | Gateway route |
| --- | --- | --- |
| `screener` | Market scan multi-symbols | student / Trading Labs |
| `analysis` | Analyse single symbol | LONA / opt-trading |
| `journal` | Consulter journal | Airtable / DB |
| `status` | Statut cockpit GO | ClickUp / GO_INDEX |
| `help` | Aide et commandes | Statique |

## Safety Gate (cote Botpress)

Toute request avec `options.dry_run = false` est bloquee par Botpress (pas transmise au Gateway) sauf si:
1. L'utilisateur a explicitement confirme en session
2. L'action est en liste blanche (journal read-only, help)
3. La session a un token de validation recent

## Timeout

- Gateway: 30s max
- Si timeout: Botpress repond "analyse en cours, je te tiens au courant"
- Retry: 1 tentative max, pas de boucle infinie

## RISKS

- À qualifier.
