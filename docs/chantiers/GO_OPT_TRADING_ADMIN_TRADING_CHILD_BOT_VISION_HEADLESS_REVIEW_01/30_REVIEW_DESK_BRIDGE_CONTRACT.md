---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01_BRIDGE
doc_type: desk_bridge_contract_review
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_REVIEW_DESK_BRIDGE_CONTRACT

## desk_bridge

| Propriete | Valeur |
| --- | --- |
| Script | /opt/trading/scripts/desk_bridge/bridge_vision_to_desk_inbox.sh |
| Service | desk_bridge.service (oneshot) |
| Timer | desk_bridge.timer (every 10 min, enabled) |
| User | ghost |
| Langage | Bash + Python (PIL) |

## Pipeline interne

```
1. pick_latest(): chercher screen_*.png le plus recent
   a. vision_processed/ d'abord
   b. vision_inbox/ ensuite

2. parse_ts_from_name(): extraire timestamp du nom

3. crop_with_convert(): ImageMagick convert -crop 2x2@
   ou crop_with_python(): PIL Image.open() + crop

4. Renommer q_0.png..q_3.png dans /shared/inbox/

5. desk_snapshot_ingest (si disponible)
```

## Mapping symboles (2x2 grid)

| Position | Symbole |
| --- | --- |
| TL (q_0) | BTCUSDT.P |
| TR (q_1) | XAUUSD |
| BL (q_2) | SOLUSDT.P |
| BR (q_3) | ETHUSDT.P |

Le script attend un dashboard 2x2 et le decoupe en 4 quadrants.

## Contrat d'entree

| Parametre | Valeur |
| --- | --- |
| Format | PNG |
| Nom | screen_*.png |
| Dossier | vision_processed/ ou vision_inbox/ |
| Contenu attendu | Dashboard 2x2 (4 charts) |
| Taille min | > 0 (non verifie actuellement -> GO_GUARD a faire) |

## Contrat de sortie

| Parametre | Valeur |
| --- | --- |
| Format | PNG (quadrants) |
| Nom | q_0.png, q_1.png, q_2.png, q_3.png |
| Dossier | /shared/inbox/ |
| Naming | SYM_TF_TS.png (ex: BTCUSDT.P_H1_20260504_163000.png) |

## Compatibilite headless

| Aspect | Compatible | Note |
| --- | --- | --- |
| Format PNG | OUI | Playwright produit du PNG |
| Nom screen_*.png | OUI | Capture headless suit le meme format |
| Dossier vision_inbox | OUI | Meme dossier |
| Taille > 0 | A AJOUTER | Garde-fou manquant |
| Dashboard 2x2 | A VERIFIER | La capture headless doit produire un dashboard 2x2 |

## Modification necessaire

**Une seule**: ajouter `[ -s "$src" ]` avant `Image.open()` pour eviter PIL crash.
Le reste du contrat est compatible avec la capture headless.
