# result_tracker

Capture résultat trade, calcul P&L brut/net/fees, détermination d'outcome (win/loss/breakeven).

## Flow

```
TradeResult + close_price → CloseRequest → ResultTracker → TradeRecord
```

## Commands

```bash
cmd.sh sanity                        # validation complète
cmd.sh test                          # 26 tests unitaires
cmd.sh track --close-price 67000     # tracker un trade via CLI
cmd.sh status                        # vérifier le module
```

## TradeRecord outcome

| Outcome | Condition |
|---------|-----------|
| win | `net_pnl > 1e-8` |
| loss | `net_pnl < -1e-8` |
| breakeven | `\|net_pnl\| <= 1e-8` |

## P&L Calculation

- Gross = direction × (close - entry) × qty (direction: +1 BUY, -1 SELL)
- Fees = (entry × qty × fee_rate) + (close × qty × fee_rate)
- Net = gross - fees

## Env

| Variable | Default | Description |
|----------|---------|-------------|
| `GATE_APPROVAL_DIR` | `data/gate_approvals/` | Répertoire des fichiers d'approbation |

## Dépendances

- `modules/trade_executor` — fournit `TradeResult`
- `modules/notification_dispatcher` — notifications Telegram
