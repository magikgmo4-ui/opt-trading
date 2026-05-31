# 10_INPUT_SURFACES_INVENTORY

## Objectif

Cataloguer les surfaces d'entree que le pipeline headless doit couvrir avant la
validation capture/analyse.

## Colonnes canoniques

| URL / adresse source | Type de page | Type de contenu | Assets couverts | Charts / indices / screeners | Priorite | Besoins de capture |
|---|---|---|---|---|---|---|
| Coinglass dashboard headless | dashboard web | liquidations / OI / long-short / heatmap | BTC, ETH puis extension multi-assets | screener derive / heatmap / ratios | P1 | viewport stable, crop par zone, multi-capture possible |
| Trading chart dashboard headless | chart web | screenshot chart + overlays | BTC/ETH/XAU puis watchlist | charts par timeframe | P1 | full-page ou crop chart principal, timeframe visible |
| Indices / macro dashboard | dashboard web | contexte macro visuel | DXY, indices, correlations | indices / panneaux macro | P2 | section capturee ciblee, texte lisible |
| Multi-section screener page | screener web | tableaux, rankings, watchlists | liste d'assets variable | screeners | P2 | viewport long ou captures par section |
| Legacy ShareX fallback | capture locale | image brute fallback | selon usage operateur | hors headless primaire | P3 | compat vision_inbox, pas source canonique cible |

## Etat etabli du repo

- `modules/bot_vision/headless_capture/README.md` confirme un pipeline Playwright + Chromium
  destine a capturer des dashboards/charts trading.
- Les profils headless portent aujourd'hui `source`, `url`, et optionnellement
  `symbol`, `timeframe`.
- La sortie actuelle ecrit des couples `PNG + sidecar JSON` dans `vision_inbox/`.
- Une voie runtime Coinglass existe deja et alimente aussi
  `data/deskpro/inputs/vision_context/coinglass/latest.json`.

## Surfaces prioritaires candidates

### P1 — a figer d'abord

| Surface | Pourquoi |
|---|---|
| Coinglass headless | deja relie a `vision_context.coinglass.v1` et a un panel DeskPro |
| chart dashboard principal | candidat naturel pour screenshots exploitables en analyse / setup |

### P2 — expansion ensuite

| Surface | Pourquoi |
|---|---|
| macro / indices dashboard | enrichit le contexte DeskPro |
| screener multi-sections | utile pour rankings / scans mais capture plus complexe |

## Mapping minimal a figer par source

Pour chaque source retenue, documenter au minimum :

- identifiant source
- URL canonique
- type de page
- asset ou universe cible
- timeframe si applicable
- viewport attendu
- zones d'interet
- mode de capture : full-page / crop / multi-capture
- output attendu : raw only / analyse / setup / telegram / data center

## Sections a remplir

- URL / adresse source
- type de page
- type de contenu
- assets couverts
- charts / indices / screeners
- priorite
- besoins de capture

## TODO

- `INPUT_SURFACES_INVENTORY`
- figer le mapping URL -> viewport -> zones d'interet
- relier chaque source a un contrat de sortie DeskPro ou Data Center explicite
