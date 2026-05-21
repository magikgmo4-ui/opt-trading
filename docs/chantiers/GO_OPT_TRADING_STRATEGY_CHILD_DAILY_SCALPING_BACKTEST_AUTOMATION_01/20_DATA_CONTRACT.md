---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01_DATA_CONTRACT
doc_type: data_contract
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01
status: open
updated_at: 2026-05-20
---

# 20_DATA_CONTRACT

## Entrées attendues

### data/market/xauusd_m5.csv

```text
timestamp,open,high,low,close,volume
2024-01-02 08:00:00,2063.50,2065.10,2062.80,2064.30,1250
...
```

| Colonne | Type | Description |
|---|---|---|
| `timestamp` | ISO 8601 ou UNIX ms | Ouverture de la bougie |
| `open` | float | Prix open |
| `high` | float | Plus haut |
| `low` | float | Plus bas |
| `close` | float | Prix close |
| `volume` | int | Volume (peut être 0 si indispo) |

### data/market/xauusd_m15.csv

Même format. Utilisé pour contexte HTF (biais, swing high/low, VWAP M15).

## Colonnes produites par indicators.py

| Colonne | Description |
|---|---|
| `session` | `london` / `ny` / `overlap` / `asia` / `off` |
| `vwap` | VWAP session cumulatif |
| `atr` | ATR(14) en cours |
| `orb_high` | Plus haut des N premières minutes de session |
| `orb_low` | Plus bas des N premières minutes de session |
| `orb_complete` | Bool — ORB calculable pour cette bougie |
| `swing_high_n` | Plus haut local sur N bougies (défaut N=5) |
| `swing_low_n` | Plus bas local sur N bougies |

## Journal CSV produit (1 ligne = 1 trade simulé)

Colonnes minimales (subset du template parent) :

```text
trade_id, date, symbol, session, timeframe, variant, direction,
setup_type, setup_score, entry_price, stop_loss, tp1, tp2,
risk_pct, rr_planned, result_R, mae_R, mfe_R,
time_in_trade_bars, followed_plan, notes
```

## Contraintes

- Pas de lookahead : seules les données `<= timestamp` de la bougie courante sont visibles.
- Spread/slippage simulé selon `config.yaml`.
- Une seule position ouverte à la fois par variant.
