---
doc_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01_SCHEMA
doc_type: signal_schema
go_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01
status: draft
---

# 20_SIGNAL_SCHEMA.md

## Format du signal

```yaml
signal_id: uuid                        # unique
source: string                         # tradingview | telegram | collector | manual
source_instance: string                # instance précise (ex: "TV_webhook_01", "tg_channel_trading")
signal_type: string                    # entry | exit | alert | heartbeat | anomaly
timestamp: ISO8601                     # moment de réception
payload:
  symbol: string                       # ex: "BTCUSD"
  direction: "buy" | "sell" | "neutral"
  price: float | null
  confidence: float                    # 0.0 - 1.0
  indicators: dict                     # indicateurs techniques
  metadata: dict                       # infos supplémentaires
cross_validation:
  required_sources: int                # nombre de sources requises
  matched_sources: list[string]        # sources qui concordent
  status: "pending" | "confirmed" | "conflicting" | "invalid"
dry_run:
  order_generated: boolean             # un ordre a-t-il été généré ?
  order_blocked: boolean               # l'ordre a-t-il été bloqué par le guard ?
  order_json: dict | null              # l'ordre qui aurait été émis
journal:
  received_at: ISO8601
  processed_at: ISO8601
  processing_time_ms: int
  status: "received" | "validated" | "cross_checked" | "logged" | "rejected"
```

## Validation rules

- `confidence >= 0.6` : seuil minimum pour traitement
- `required_sources >= 2` : recroisement obligatoire
- `price > 0` : prix valide
- `signal_type` dans liste autorisée : entry, exit, alert, heartbeat, anomaly
