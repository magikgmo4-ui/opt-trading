---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01_INBOX
doc_type: index/inbox_entry
repo: opt-trading
machine: admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01
status: partial
scope: risk_limits_kill_switch_spec
---

# GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01

Risk limits et kill switch spécifiés pour admin-trading.

Résultat: PARTIAL (spécifié, non implémenté)

Risk limits définis:
- Max notional: 1000 USD
- Max position: 0.01 BTC / 0.1 ETH
- Max daily loss: 100 USD
- Max open positions: 3
- Max orders/hour: 10
- Allowed symbols: BTC/USDT, ETH/USDT

Kill switch niveaux:
- Level 1: Soft stop (TRADE_ALLOWED=false)
- Level 2: Service stop (systemctl)
- Level 3: Hard stop (clear state)

Rollback plan: documenté
Validation gates: 7 définis

Production NON ouverte.
Prochaine action: implémenter risk limits + kill switch.
