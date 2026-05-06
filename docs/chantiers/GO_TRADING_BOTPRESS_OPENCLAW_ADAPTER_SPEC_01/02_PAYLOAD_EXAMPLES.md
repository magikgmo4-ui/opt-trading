---
doc_id: GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01_PAYLOADS
doc_type: payload_examples
repo: opt-trading
go_id: GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01/01_ADAPTER_CONTRACT.md
---

# 02_PAYLOAD_EXAMPLES — Adapter Botpress ↔ OpenClaw

## Example 1: Screener BTCUSDT

### Botpress → Adapter

```json
{
  "botpress_event_id": "evt-001",
  "telegram_chat_id": "123456789",
  "telegram_user_id": "987654321",
  "intent": "screener",
  "original_message": "/screener BTCUSDT 1h",
  "parsed_params": {"symbol": "BTCUSDT", "timeframe": "1h"},
  "session_context": {"previous_intents": [], "session_started_at": "2026-05-06T20:00:00Z"}
}
```

### Adapter → OpenClaw

```json
{
  "intent": "screener",
  "context": {"user_id": "telegram_123456789", "symbol": "BTCUSDT", "timeframe": "1h"},
  "payload": {"query": "market scan BTCUSDT 1h", "attachments": []},
  "options": {"dry_run": true, "max_symbols": 5, "timeout_ms": 30000}
}
```

### OpenClaw → Adapter

```json
{
  "status": "ok",
  "intent": "screener",
  "result": {
    "data": {
      "symbol": "BTCUSDT",
      "price": 67890,
      "rsi": 52,
      "macd": "bullish",
      "volume_24h": "1.2B",
      "trend": "neutral"
    },
    "summary": "**BTCUSDT** 1h: Price 67890 | RSI 52 neutral | MACD bullish | No clear signal",
    "actions_taken": ["market_scan"],
    "warnings": []
  },
  "trace_id": "trace-abc-001"
}
```

### Adapter → Botpress

```json
{
  "botpress_event_id": "evt-001",
  "status": "ok",
  "reply_text": "**BTCUSDT** 1h\nPrice: 67890\nRSI: 52 (neutral)\nMACD: bullish\nVolume 24h: 1.2B\nTrend: neutral\n\nNo clear signal.",
  "safety_check": "passed",
  "trace_id": "trace-abc-001",
  "duration_ms": 2340
}
```

---

## Example 2: Trade bloque

### Botpress → Adapter

```json
{
  "botpress_event_id": "evt-002",
  "telegram_chat_id": "123456789",
  "intent": "execute_trade",
  "original_message": "/trade buy BTCUSDT 0.01",
  "parsed_params": {"symbol": "BTCUSDT", "side": "buy", "qty": 0.01},
  "session_context": {"previous_intents": ["analysis"], "session_started_at": "2026-05-06T20:00:00Z"}
}
```

### Adapter → Botpress (blocage immediat)

```json
{
  "botpress_event_id": "evt-002",
  "status": "blocked",
  "reply_text": "Action bloquee: trading reel non autorise en V1. Utilise /analysis ou /screener.",
  "safety_check": "blocked",
  "trace_id": "trace-abc-002",
  "duration_ms": 5
}
```

Note: l adapter ne transmet JAMAIS `execute_trade` a OpenClaw Gateway.

---

## Example 3: Timeout Gateway

### Adapter → Botpress

```json
{
  "botpress_event_id": "evt-003",
  "status": "timeout",
  "reply_text": "Analyse en cours, delai depasse. Je te tiens au courant des que le resultat arrive.",
  "safety_check": "passed",
  "trace_id": "trace-abc-003",
  "duration_ms": 31000
}
```
