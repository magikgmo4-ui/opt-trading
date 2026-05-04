---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01_SMOKE
doc_type: capture_smoke
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_CAPTURE_SMOKE — Resultat

## Commande

```bash
cd /opt/trading/modules/bot_vision/headless_capture
node capture_headless.js --profile profiles.example.json --once
```

## Verdict

**PASS**

## Fichiers produits

| Fichier | Taille | Statut |
| --- | --- | --- |
| screen_tradingview_BTCUSDT.P_H1_2026-05-04_17-00-35.png | 94,569 B (94 KB) | VALIDE |
| screen_tradingview_BTCUSDT.P_H1_2026-05-04_17-00-35.json | 497 B | VALIDE |

## Verifications

| Check | Resultat |
| --- | --- |
| PNG > 0 | OUI (94 KB) |
| PNG > 1 KB minimum | OUI |
| JSON sidecar present | OUI |
| Aucun .uploading restant | OUI (0 fichiers) |
| Aucun fichier 0-byte | OUI (0 fichiers) |
| vision_bot a traite | OUI (deplace vers processed + outbox) |
| vision_outbox .md produit | OUI (516 B) |
| vision_outbox .txt produit | OUI (365 B) |
| Services critiques actifs | OUI (5/5) |
| macro-xau disabled | OUI |

## Pipeline complet valide

```
capture_headless.js (94 KB PNG + JSON) 
  -> vision_inbox
  -> vision_bot (OCR, deplace, .md/.txt)
  -> vision_processed + vision_outbox
  -> desk_bridge (timer, prochain cycle)
```

Le pipeline end-to-end est fonctionnel.
