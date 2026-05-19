---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01
surface: ADMIN_TRADING
source_kind: closeout
updated_at: 2026-05-19
---

# 50_CLOSEOUT

## Verdict final

`BLOCKED_WITH_REASON_DYNAMIC_LOAD_PARTIAL_XAU_SPINNER_COINGLASS_TIMEOUT`

## Ce qui est valide

- `capture_headless.js` supporte une strategie de chargement configurable par profil.
- Les defaults historiques sont conserves pour les profils existants.
- `profiles.example.json` n'a pas ete modifie.
- Le profil dynamic smoke separe est cree et valide JSON.
- Le sidecar JSON est enrichi avec les options de chargement.
- `npm run check` retourne `playwright:OK`.
- Aucun restart service/timer.
- Aucun `.env` lu.
- Aucun trade.

## Ce qui reste bloque

- `tv_xau_h1` peut produire un PNG dans une configuration, mais la capture est un spinner et echoue la lisibilite humaine.
- `cg_btc_flow` reste bloque avant screenshot, meme avec l'URL Coinglass simplifiee et `domcontentloaded`.
- `tv_btc_h1` a montre un timeout intermittent avec `networkidle` pendant Smoke B, ce qui confirme que le profil P0 ne doit pas dependre de `networkidle` sans fallback.

## Decision

Ne pas promouvoir P0 vers le timer. La strategie configurable est un prerequis utile, mais elle ne suffit pas a rendre XAU/Coinglass stables.

## Next GO recommande

```text
GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_TIMEOUT_FALLBACK_AND_SKIP_JSON_01
```

Objectif : ajouter un comportement explicite quand `goto` timeout :

1. option de profil pour capturer apres timeout si la page a un DOM utilisable ;
2. option de profil pour ecrire un JSON sidecar `status=blocked` avec `blocked_reason` sans PNG ;
3. validation visuelle automatique minimale pour detecter les spinners ou pages quasi blanches ;
4. nouveau smoke manuel XAU/Coinglass.

## Resume point

```text
Dynamic load strategy implemented, defaults preserved.
BTC remains generally capturable but networkidle is intermittent.
XAU produced spinner, not readable.
Coinglass timeout persists.
Do not promote P0 to timer.
```
