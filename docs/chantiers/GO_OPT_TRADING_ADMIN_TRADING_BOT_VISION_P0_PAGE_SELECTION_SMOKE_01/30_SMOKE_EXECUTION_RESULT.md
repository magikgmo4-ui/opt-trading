---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01
surface: ADMIN_TRADING
source_kind: smoke_result
updated_at: 2026-05-19
---

# 30_SMOKE_EXECUTION_RESULT

## Pre-check

`npm run check` dans `modules/bot_vision/headless_capture` :

```text
playwright:OK
```

## Fenetre d'execution

| Evenement | Horodatage |
| --- | --- |
| smoke start | `2026-05-19T03:28:31-04:00` |
| smoke end | `2026-05-19T03:29:45-04:00` |

## Sortie brute utile

```text
[2026-05-19_03-28-32] Capturing: tradingview BTCUSDT.P (https://www.tradingview.com/chart/?symbol=BTCUSDT.P)
OK: /srv/sftp/shared_files/shared/vision_inbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-28-32.png (38385B)
OK: /srv/sftp/shared_files/shared/vision_inbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-28-32.json (497B)
DONE: tradingview -> screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-28-32.png

[2026-05-19_03-28-45] Capturing: tradingview XAUUSD (https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD)
ERROR capturing tradingview: page.goto: Timeout 30000ms exceeded.
Call log:
  - navigating to "https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD", waiting until "networkidle"

[2026-05-19_03-29-15] Capturing: coinglass BTCUSDT.P (https://www.coinglass.com/pro/futures/LiquidationHeatMap?coin=BTC&type=symbol)
ERROR capturing coinglass: page.goto: Timeout 30000ms exceeded.
Call log:
  - navigating to "https://www.coinglass.com/pro/futures/LiquidationHeatMap?coin=BTC&type=symbol", waiting until "networkidle"

Capture cycle complete.
```

## Artefacts observes

| Page ID | PNG | JSON | PNG size | Ingestion | Extraction | Statut |
| --- | --- | --- | ---: | --- | --- | --- |
| `tv_btc_h1` | oui | oui | `38385` | `vision_processed` | `.txt` + `.md` | PASS |
| `tv_xau_h1` | non | non | n/a | n/a | n/a | BLOCKED |
| `cg_btc_flow` | non | non | n/a | n/a | n/a | BLOCKED |

## Fichiers BTC produits

```text
/srv/sftp/shared_files/shared/vision_processed/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-28-32.png
size=38385

/srv/sftp/shared_files/shared/vision_inbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-28-32.json
size=497

/srv/sftp/shared_files/shared/vision_outbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-28-32.txt
size=122

/srv/sftp/shared_files/shared/vision_outbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-28-32.md
size=273
```

## Controle `.uploading`

Recherche read-only dans `vision_inbox` : aucune sortie.

## Resultat par page

| Page ID | Capture | Ingestion | Extraction | Human readability | Verdict |
| --- | --- | --- | --- | --- | --- |
| `tv_btc_h1` | `PASS_CAPTURE` | `PASS_INGESTION` | `PASS_EXTRACTION` | `PASS_HUMAN_READABILITY` | PASS |
| `tv_xau_h1` | `BLOCKED_WITH_REASON_TIMEOUT_NETWORKIDLE_NO_ARTIFACT` | n/a | n/a | n/a | BLOCKED |
| `cg_btc_flow` | `BLOCKED_WITH_REASON_TIMEOUT_NETWORKIDLE_NO_ARTIFACT` | n/a | n/a | n/a | BLOCKED |

## Interpretation

Le profil P0 n'est pas pret pour activation runtime. Le pipeline fonctionne pour BTC H1, mais les pages XAU et Coinglass ne franchissent pas `page.goto(... waitUntil: 'networkidle')` dans le timeout actuel de 30 secondes.
