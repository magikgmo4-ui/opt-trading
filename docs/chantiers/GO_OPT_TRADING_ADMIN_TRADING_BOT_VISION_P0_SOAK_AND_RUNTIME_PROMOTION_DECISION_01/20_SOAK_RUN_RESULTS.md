# 20_SOAK_RUN_RESULTS

## Verdict brut

- cycles exécutés : `3`
- captures observées : `12`
- `ready/pass` : `12 / 12`
- `blocked` : `0`
- `invalid_visual` : `0`

## Cycle 1

| page_id | status | visual_status | png_created | json_sidecar | vision_processed | vision_outbox | human_readability |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `tv_btc_h1_strat_a` | `ready` | `pass` | oui (`171909 B`) | oui | oui | oui | oui |
| `tv_btc_h1_strat_b` | `ready` | `pass` | oui (`171300 B`) | oui | oui | oui | oui |
| `tv_xau_h1_strat_a` | `ready` | `pass` | oui (`181518 B`) | oui | oui | oui | oui |
| `cg_btc_flow_strat_a` | `ready` | `pass` | oui (`341495 B`) | oui | oui | oui | oui |

## Cycle 2

| page_id | status | visual_status | png_created | json_sidecar | vision_processed | vision_outbox | human_readability |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `tv_btc_h1_strat_a` | `ready` | `pass` | oui (`172833 B`) | oui | oui | oui | oui |
| `tv_btc_h1_strat_b` | `ready` | `pass` | oui (`172426 B`) | oui | oui | oui | oui |
| `tv_xau_h1_strat_a` | `ready` | `pass` | oui (`181707 B`) | oui | oui | oui | oui |
| `cg_btc_flow_strat_a` | `ready` | `pass` | oui (`343856 B`) | oui | oui | oui | oui |

## Cycle 3

| page_id | status | visual_status | png_created | json_sidecar | vision_processed | vision_outbox | human_readability |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `tv_btc_h1_strat_a` | `ready` | `pass` | oui (`171534 B`) | oui | oui | oui | oui |
| `tv_btc_h1_strat_b` | `ready` | `pass` | oui (`172419 B`) | oui | oui | oui | oui |
| `tv_xau_h1_strat_a` | `ready` | `pass` | oui (`181411 B`) | oui | oui | oui | oui |
| `cg_btc_flow_strat_a` | `ready` | `pass` | oui (`348611 B`) | oui | oui | oui | oui |

## Notes d’extractibilité

- OCR `tesseract` produit du bruit mais restitue bien les éléments de structure utiles : ticker, OHLC, watchlist, labels marché.
- Exemples confirmés :
  - BTC : `Bitcoin / TetherUS PERPETUAL CONTRACT`
  - XAU : `Gold Spot / U.S. Dollar`
  - Coinglass : `24h Volume`, `Open Interest`, `24h Liquidation`, `Liquidation Data`
