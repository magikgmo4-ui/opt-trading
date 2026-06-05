---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01_INBOX
doc_type: index/inbox_entry
repo: opt-trading
machine: admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01
status: pass_paper_test_executed
scope: paper_test_execution
---

# GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01

PAPER_TEST exécuté avec succès sur admin-trading.

Résultat:
- POST /tv HTTP 200, ok: true
- Execution: paper_BTC/USDT_123, filled 0.1 @ 65000.0
- Position: BTC/USDT BUY 0.1 OPEN (paper)
- Adapter: paper (simulation)
- Guards ok: true avant et après
- Aucun trade réel
- Aucun live trading

Payload envoyé:
```json
{
    "engine": "PAPER_TEST",
    "signal": "BUY",
    "symbol": "BTC/USDT",
    "tf": "1h",
    "price": 65000.0,
    "tp": 66000.0,
    "sl": 64000.0,
    "reason": "GO_PAPER_TEST_RETRY_01"
}
```

Prochaine suite:
Validation pipeline PAPER_TEST complète. Options: close position, additional scenarios, risk sizing tests.

## RISKS

- À qualifier.
