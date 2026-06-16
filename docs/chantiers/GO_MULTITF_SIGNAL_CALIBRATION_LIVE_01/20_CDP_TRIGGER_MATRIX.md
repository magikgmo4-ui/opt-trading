# 20_CDP_TRIGGER_MATRIX — Événements CDP et leur impact sur le scoring

## Événements CDP supportés (22 types)

Source : `modules/tradingview/cdp_normalizer.py`

| Catégorie | Événements | Impact scoring |
|---|---|---|
| VWAP | `vwap_reclaim`, `vwap_loss` | +13 pts VWAP quality, +15 pts LTF trigger |
| ORB | `orb_break_high`, `orb_break_low` | +15 pts LTF trigger, +10 pts levels |
| Volume | `volume_spike`, `volume_on_breakout`, `relative_volume_gt_2`, `relative_volume_gt_3` | +8 pts volume/orderflow |
| Structure | `bos_bull`, `bos_bear`, `choch_bull`, `choch_bear` | +10 pts HTF alignment |
| FVG | `fvg_created`, `fvg_filled` | +5 pts LTF trigger |
| Liquidité | `liquidity_sweep_high`, `liquidity_sweep_low` | +12 pts LTF trigger |
| Breakout | `breakout_high`, `breakdown_low` | +10 pts levels |
| Macro | `dxy_breakout`, `dxy_breakdown`, `vix_spike`, `qqq_risk_on`, `qqq_risk_off` | +5 pts macro alignment |

## Événements actuellement dans signal_event.v1

| Symbole | Événement | Prix | Timestamp | Fraîcheur |
|---|---|---|---|---|
| SPCX | vwap_reclaim | 171.5 | 2026-06-15T12:30Z | ~5h old |

## Triggers manquants pour monter de C à B+

Pour que BTC/ETH/SOL/XAUUSD passent de C/34 à B+/62, il faut au moins :
- 1 événement VWAP (`vwap_loss` ou `vwap_reclaim`) OU
- 1 événement ORB (`orb_break_high/low`) + volume_spike OU
- 1 événement liquidity_sweep + reclaim
