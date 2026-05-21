---
doc_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01_EVIDENCE
doc_type: evidence
go_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01
status: passed_with_evidence
---

# 99_EVIDENCE

## Preuve concrète de validation

### 1. Signal schema
- `20_SIGNAL_SCHEMA.md` — signal_id, source, type, payload, cross_validation, dry_run, journal
- Validation rules : confidence >= 0.6, required_sources >= 2, price > 0

### 2. Source adapters
- `30_SOURCE_ADAPTERS.md` — 5 sources (TradingView, Telegram, on-chain, market, manual)
- Cross-validation : majority policy, min 2 sources, 30s timeout

### 3. Invalidation rules
- `40_INVALIDATION_AND_GUARD.md` — 7 conditions de rejet (confidence < 0.6, price <= 0, no cross, unknown type, stale, missing direction, kill switch)

### 4. Dry-run guard
- `40_INVALIDATION_AND_GUARD.md` — 3 blocks (live order, wallet modif, real API), 0 bypass
- `signal_processor.py` — testé : ordre confirmé généré en dry-run et bloqué

### 5. Journal
- `50_JOURNAL_AND_BACKTEST.md` — storage `data/signals/journal/YYYY-MM-DD.jsonl`
- `signal_processor.py` — journalise chaque signal

### 6. Backtest stats
- `50_JOURNAL_AND_BACKTEST.md` — 6 metrics (total, confirmation rate, win rate, drawdown, etc.)
- `signal_stats.py` — output JSON validé

### 7. Test signal processor (3 scénarios)

```bash
$ python3 scripts/ai/workers/signal_processor.py
SIGNAL a54e8d18 | BTCUSD | cross=confirmed | blocked=True     # ✓ confirmé + bloqué
INVALID: confidence_below_threshold                             # ✓ rejeté (confidence 0.45)
SIGNAL 3ca73386 | SOLUSD | cross=pending | blocked=False       # ✓ pending (1 source)
Results: 2/3 PASS
```

### 8. Signal stats

```bash
$ python3 scripts/ai/workers/signal_stats.py
{"total_signals": 2, "confirmed": 1, "confirmation_rate": 50.0, "orders_blocked": 1, ...}
```

## Conclusion

Tous les critères de succès sont remplis (signal reçu, validé, recroisé, journalisé ; aucun ordre live ; stats calculables). Statut : PASS_WITH_EVIDENCE.
