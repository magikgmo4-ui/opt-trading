---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01_INBOX
doc_type: index/inbox_entry
repo: opt-trading
machine: admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01
status: pass_config
scope: paper_flags_config
---

# GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01

Paper flags configurés sur admin-trading.

Résultat:
- `/api/paper/guards` retourne HTTP 200 avec `ok: true`
- Tous les guards PASS
- Aucun payload PAPER_TEST envoyé
- Aucun ordre réel
- Aucun live trading

Flags configurés:
- `RUNNER_MODE=PAPER`
- `SIMULATION_MODE=true`
- `TRADE_ALLOWED=false`
- `LEDGER_PATH=/opt/trading/state/ledger_paper.json`
- `active_engine` cleared to null

Prochaine suite:
`GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01` (controlled PAPER_TEST execution)
