---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01
surface: ADMIN_TRADING
source_kind: canonical
updated_at: 2026-05-19
---

# 30_NAMING_CLASSIFICATION_CONTRACT

## Objectif

Stabiliser le nommage et le classement des screenshots sans casser le flux existant.

## Nommage cible

Format recommande :

```text
screen_<page_id>_<symbol>_<timeframe>_<YYYYMMDD_HHMMSSZ>_<hash8>.png
screen_<page_id>_<symbol>_<timeframe>_<YYYYMMDD_HHMMSSZ>_<hash8>.json
```

Exemples :

```text
screen_tv_btc_h1_BTCUSDT.P_H1_20260519_143000Z_a1b2c3d4.png
screen_cg_btc_flow_BTCUSDT.P_FLOW_20260519_143000Z_9f8e7d6c.json
```

## Compatibilite actuelle

Le module actuel produit :

```text
screen_<source>_<symbol>_<timeframe>_<YYYY-MM-DD_HH-MM-SS>.png
screen_<source>_<symbol>_<timeframe>_<YYYY-MM-DD_HH-MM-SS>.json
```

Le passage au nommage cible doit etre traite comme evolution explicite, car les consommateurs downstream peuvent dependre du format actuel.

## Champs sidecar cibles

```json
{
  "producer": "bot_vision_headless",
  "capture_mode": "playwright_chromium",
  "page_id": "tv_btc_h1",
  "source": "tradingview",
  "symbol": "BTCUSDT.P",
  "timeframe": "H1",
  "url": "REDACTED_OR_PUBLIC_URL",
  "viewport": { "width": 1920, "height": 1080 },
  "created_at_utc": "2026-05-19T14:30:00.000Z",
  "hash8": "a1b2c3d4",
  "output_png": "screen_tv_btc_h1_BTCUSDT.P_H1_20260519_143000Z_a1b2c3d4.png",
  "output_json": "screen_tv_btc_h1_BTCUSDT.P_H1_20260519_143000Z_a1b2c3d4.json",
  "status": "ready"
}
```

## Classement cible

```text
/shared/vision_inbox/
  incoming raw temporaire

/shared/vision_processed/
  fichiers traites OCR

/shared/vision_outbox/
  extraction texte/md/json

/shared/desk/snapshots/
  images consommables Desk Pro

/shared/vision_archive/
  YYYY/MM/DD/<page_id>/
    canonical/
    rejected/
    compressed/
```

## Regles

- `vision_inbox` ne doit pas devenir archive longue duree.
- `processed` conserve court terme.
- `desk/snapshots` expose uniquement les surfaces consommables.
- `vision_archive` recoit uniquement des fichiers listes dans un manifest.
- Aucun fichier `.uploading` ne doit entrer dans l'archive.

