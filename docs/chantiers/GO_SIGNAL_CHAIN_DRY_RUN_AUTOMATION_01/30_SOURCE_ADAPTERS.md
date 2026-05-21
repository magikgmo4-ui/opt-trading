---
doc_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01_ADAPTERS
doc_type: signal_adapters
go_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01
status: draft
---

# 30_SOURCE_ADAPTERS.md

## Sources de signaux

| Source | Adapter | Format entrée | Traitement | Statut |
|---|---|---|---|---|
| **TradingView** | `tradingview/webhook_handler.py` | JSON POST (webhook) | Parse + valide + journal | Active |
| **Telegram** | `adapters/telegram_signal_reader.py` | Message texte structuré | Parse + extrait symbol/direction | Active |
| **Collecteur on-chain** | `data/collectors/onchain.py` | CSV/JSON via API | Agrège + formate | Active |
| **Collecteur market** | `data/collectors/market.py` | API REST (Binance, etc.) | OHLCV + indicateurs | Active |
| **Manual** | N/A | Fichier `data/signals/manual/` | Lecture fichier JSON | Active |

## Recroisement

```yaml
cross_validation:
  policy: "majority"
  min_sources: 2
  timeout: 30_000  # ms (30s pour recouper)
  sources:
    - tradingview
    - telegram
    - onchain
    - market
  confirmation:
    - 2/4 sources concordantes → confirmed
    - 1/4 → pending (attente 30s)
    - 0/4 → conflicting
```
