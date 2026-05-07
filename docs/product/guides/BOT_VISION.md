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

# Guide - Bot Vision

## 1_MASTER_TARGET

Pipeline vision avec survivant unique, capture headless, artefacts Desk Pro/Telegram.

## FINAL_TARGET

Pipeline de capture screenshot -> analyse Vision -> artefacts Desk Pro / Telegram, avec un module unique standardise.

## CURRENT_STATE

`USABLE_LIMITED` -- Chaine transitoire active (`vision_bot` + `bot_vision_step2`). `bot_vision` est legacy. Survivant unique non fige.

## USAGE_ALLOWED_NOW

- Capturer des screenshots trading via `vision_bot`.
- Analyser via `bot_vision_step2`.
- Produire des artefacts pour Desk Pro ou Telegram.
- Pipeline headless operationnel (branches admin-trading).

## USAGE_FORBIDDEN_NOW

- Utiliser `bot_vision` (legacy) comme surface active.
- Traiter Bot Vision comme produit fini sans limites.
- Trading automatique sans validation humaine.

## IMPLEMENTATION_PATH

1. Figer le survivant unique (vision_bot + bot_vision_step2 -> module final).
2. Stabiliser la transition step2.
3. Archiver bot_vision legacy.
4. Produire un closeout produit.

## CONTINUITY_STATE

Actif -- `VISION_FAMILY_SURVIVOR_DECISION` en attente.

## MACHINE / SURFACE

`admin-trading` (pipeline headless).

## REPRISE_POINT

```text
docs/status/bot_vision_canonique.md
docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md
```

## TODO

1. Decider le survivant unique (VISION_FAMILY_SURVIVOR_DECISION).
2. Archiver bot_vision.
3. Documenter la chaine finale.

## REMAINING_GAP

Survivant unique non fige, transition step2 en cours de stabilisation structurelle.

## NEXT_GO

`VISION_FAMILY_SURVIVOR_DECISION`

## PROMOTION_CONDITIONS

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- survivant unique fige,
- chaine operationnelle stabilisee,
- closeout produit pose.

## Ce que c'est

Pipeline de capture screenshot -> analyse Vision -> artefacts Desk Pro / Telegram.

## A quoi ca sert

Capturer des screenshots trading, les analyser via Vision, produire des artefacts exploitables.

## Quand l'utiliser

- Capturer des screenshots de marches.
- Envoyer les resultats d'analyse vers Desk Pro ou Telegram.
- Surveiller un setup visuel via le pipeline headless.

## Quand ne pas l'utiliser

- Comme moteur de decision autonome.
- Comme produit fini sans limites.
- Pour du trading automatique.

## Prerequis

- Modules actifs : `vision_bot` (capture inbox-outbox), `bot_vision_step2` (analyse).
- Pipeline headless : `scripts/run_bot_vision_headless_capture.sh`.
- Connaissance de la chaine transitoire actuelle.

## Commandes / acces

- Capture : `modules/vision_bot/`
- Analyse : `modules/bot_vision_step2/`
- Pipeline headless : `scripts/run_bot_vision_headless_capture.sh`

## Procedure simple

1. Capturer un screenshot via `vision_bot`.
2. Lancer l'analyse via `bot_vision_step2`.
3. Verifier les artefacts dans Desk Pro ou Telegram.

## Verification PASS

- `vision_bot` capture correctement.
- `bot_vision_step2` produit des artefacts lisibles.
- `bot_vision` (legacy) n'est pas utilise.

## Limites

- Chaine transitoire, pas de survivant unique.
- `bot_vision` legacy a ne pas utiliser.
- Transition step2 en cours.

## Depannage

- `bot_vision` appele par erreur : utiliser `bot_vision_step2`.
- Capture echouee : verifier les logs de `vision_bot`.
- Analyse sans resultat : verifier le bridge Desk Pro/Telegram.

## Source canonique

- `docs/status/bot_vision_canonique.md`
- `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`
