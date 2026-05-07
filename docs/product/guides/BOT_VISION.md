---
doc_id: OPT_TRADING_GUIDE_BOT_VISION
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/status/bot_vision_canonique.md
  - docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md
---

# Guide utilisateur - Bot Vision

## Ce que c'est

Bot Vision est un pipeline de capture screenshot -> analyse Vision -> artefacts Desk Pro / Telegram.

## A quoi ca sert

Il sert a capturer des screenshots trading, les analyser via Vision, et produire des artefacts exploitables par Desk Pro et Telegram.

## Quand l'utiliser

- pour capturer des screenshots de marches et les faire analyser ;
- pour envoyer les resultats d'analyse vers Desk Pro ou Telegram ;
- pour surveiller un setup visuel via le pipeline headless.

## Quand ne pas l'utiliser

- comme moteur de decision autonome ;
- comme produit fini sans limites (le survivant unique n'est pas fige) ;
- pour du trading automatique sans validation humaine.

## Prerequis

- acces au pipeline vision (capture, analyse, artefacts) ;
- modules actifs : `vision_bot` (capture inbox-outbox), `bot_vision_step2` (analyse Vision/Telegram) ;
- connaissance de la chaine transitoire actuelle.

## Commandes / acces

- Capture : `modules/vision_bot/`
- Analyse : `modules/bot_vision_step2/`
- Pipeline headless : `scripts/run_bot_vision_headless_capture.sh`
- Synthese : `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`

## Procedure simple

1. Capturer un screenshot via `vision_bot`.
2. Lancer l'analyse via `bot_vision_step2`.
3. Verifier les artefacts produits dans Desk Pro ou Telegram.
4. En cas de doute, relire la fiche statut canonique.

## Verification PASS

- `vision_bot` capture les screenshots correctement ;
- `bot_vision_step2` produit des artefacts lisibles ;
- les artefacts arrivent bien dans Desk Pro ou Telegram ;
- `bot_vision` (legacy) n'est pas utilise comme surface active.

## Limites

- la chaine est transitoire : `vision_bot` + `bot_vision_step2` forment le survivant actuel, mais aucun module unique n'est fige ;
- `bot_vision` est explicitement legacy et ne doit pas etre utilise ;
- la transition vers un survivant unique est en cours.

## Depannage

- Si `bot_vision` est appele par erreur : utiliser `bot_vision_step2` a la place.
- Si la capture echoue : verifier les logs de `vision_bot`.
- Si l'analyse ne produit rien : verifier le bridge vers Desk Pro/Telegram.

## Source canonique

- `docs/status/bot_vision_canonique.md`
- `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`

## NEXT_GO

`VISION_FAMILY_SURVIVOR_DECISION`
