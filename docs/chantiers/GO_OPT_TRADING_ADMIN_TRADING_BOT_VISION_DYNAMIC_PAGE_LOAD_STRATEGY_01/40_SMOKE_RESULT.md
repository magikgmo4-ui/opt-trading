---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01
surface: ADMIN_TRADING
source_kind: smoke_result
updated_at: 2026-05-19
---

# 40_SMOKE_RESULT

## Smoke A result

Commande :

```bash
BOT_VISION_OUT=/srv/sftp/shared_files/shared/vision_inbox   npm run capture -- --profile profiles.p0.dynamic.smoke.local.json --once
```

Fenetre : `2026-05-19T04:02:45-04:00` a `2026-05-19T04:05:12-04:00`.

### Artefacts

| Page ID | PNG | JSON | Ingestion | Extraction | Lisibilite | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `tv_btc_h1` | `38588` bytes | `639` bytes | PASS | PASS | PASS | PASS |
| `tv_xau_h1` | `11507` bytes | `639` bytes | PASS | PASS | BLOCKED spinner | PARTIAL |
| `cg_btc_flow` | non | non | n/a | n/a | n/a | BLOCKED timeout |

Fichiers observes :

```text
/srv/sftp/shared_files/shared/vision_processed/screen_tradingview_BTCUSDT.P_H1_2026-05-19_04-02-46.png
/srv/sftp/shared_files/shared/vision_inbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_04-02-46.json
/srv/sftp/shared_files/shared/vision_outbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_04-02-46.txt
/srv/sftp/shared_files/shared/vision_outbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_04-02-46.md

/srv/sftp/shared_files/shared/vision_processed/screen_tradingview_XAUUSD_H1_2026-05-19_04-03-10.png
/srv/sftp/shared_files/shared/vision_inbox/screen_tradingview_XAUUSD_H1_2026-05-19_04-03-10.json
/srv/sftp/shared_files/shared/vision_outbox/screen_tradingview_XAUUSD_H1_2026-05-19_04-03-10.txt
/srv/sftp/shared_files/shared/vision_outbox/screen_tradingview_XAUUSD_H1_2026-05-19_04-03-10.md
```

### XAU visual review

PNG stats :

```text
size=(1920,1080)
mean_luma=254.96
stddev_luma=2.4
```

Visual review : white page with loading spinner. Not acceptable as a human-readable chart.

## Smoke B result

Fenetre : `2026-05-19T04:07:22-04:00` a `2026-05-19T04:09:54-04:00`.

Profile changes before Smoke B :

- XAU `post_load_wait_ms`: `30000` ;
- Coinglass URL simplified to `https://www.coinglass.com/pro/futures/LiquidationHeatMap?coin=BTC` ;
- Coinglass `post_load_wait_ms`: `20000`.

Result :

| Page ID | Resultat |
| --- | --- |
| `tv_btc_h1` | timeout intermittent waiting until `networkidle` |
| `tv_xau_h1` | timeout waiting until `domcontentloaded` |
| `cg_btc_flow` | timeout waiting until `domcontentloaded` |

## `.uploading`

Recherche read-only dans `vision_inbox` : aucune sortie.

## Conclusion smoke

Le contrat de chargement par profil fonctionne et le sidecar enrichi est produit quand une page est capturee. Le GO reste bloque pour activation P0 car XAU n'est pas lisible et Coinglass ne produit aucun artefact.
