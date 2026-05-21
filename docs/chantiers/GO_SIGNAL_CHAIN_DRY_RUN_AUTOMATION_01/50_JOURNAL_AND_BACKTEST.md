---
doc_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01_JOURNAL
doc_type: signal_journal
go_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01
status: draft
---

# 50_JOURNAL_AND_BACKTEST.md

## Journal des signaux

Stockage : `data/signals/journal/YYYY-MM-DD.jsonl`

```yaml
# Chaque ligne = 1 signal traité
- signal_id: uuid
  source: tradingview
  signal_type: entry
  symbol: BTCUSD
  direction: buy
  confidence: 0.82
  cross_validation:
    status: confirmed
    matched_sources: [tradingview, telegram]
  dry_run:
    order_blocked: true
    order_json:
      symbol: BTCUSD
      side: buy
      quantity: 0.01
      price: 12345.67
  journal:
    received_at: 2026-05-21T02:00:00Z
    processing_time_ms: 450
    status: logged
```

## Backtest stats

Calculées à partir du journal :

| Stat | Définition | Source |
|---|---|---|
| Signaux total | Nombre total de signaux reçus | Journal count |
| Taux confirmation | Confirmés / Total | Cross_validation.status == confirmed |
| Taux rejet | Rejetés / Total | status == rejected |
| Win rate (simulé) | Ordres simulés gagnants | Basé sur price à réception vs price à échéance |
| Drawdown max | Perte maximale simulée | Basé sur les dry-run orders |
| Temps traitement moyen | Moyenne processing_time_ms | Journal aggregation |

```bash
# Commande pour les stats
python3 scripts/ai/workers/signal_stats.py [--journal data/signals/journal/]
```
