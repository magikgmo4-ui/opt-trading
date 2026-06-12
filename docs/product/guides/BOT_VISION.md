---
doc_id: OPT_TRADING_GUIDE_BOT_VISION
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/status/bot_vision_canonique.md
  - docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md
  - docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/90_CLOSEOUT.md
---

# Guide - Bot Vision

## 1_MASTER_TARGET

Pipeline vision avec survivant unique, capture headless, artefacts Desk Pro/Telegram.

## FINAL_TARGET

Pipeline de capture screenshot -> analyse Vision -> artefacts Desk Pro / Telegram, avec un module unique standardise.

## CURRENT_STATE

`USABLE_LIMITED` -- Paire canonique stable (`vision_bot` + `bot_vision_step2`) avec wrappers unifies, timers et systemd. `bot_vision` reste legacy preserve.

## USAGE_ALLOWED_NOW

- Capturer des screenshots trading via `vision_bot`.
- Analyser via `bot_vision_step2`.
- Produire des artefacts pour Desk Pro ou Telegram.
- Utiliser les wrappers `cmd-vision`, `menu-vision`, `sanity-vision`.
- Pipeline headless operationnel cote `admin-trading`.

## USAGE_FORBIDDEN_NOW

- Utiliser `bot_vision` (legacy) comme surface active.
- Traiter Bot Vision comme produit fini sans limites.
- Trading automatique sans validation humaine.

## IMPLEMENTATION_PATH

1. Verifier l'integrite des timers et services.
2. Tester le flux inbox -> outbox.
3. Valider la route Telegram `/analyze`.
4. Produire le closeout de stabilisation runtime.

## CONTINUITY_STATE

Actif -- `GO_OPT_TRADING_VISION_RUNTIME_STABILIZATION_01` est le prochain point de stabilisation.

## MACHINE / SURFACE

`admin-trading` (pipeline headless).

## REPRISE_POINT

```text
docs/status/bot_vision_canonique.md
docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md
docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/90_CLOSEOUT.md
```

## TODO

1. Verifier timers et services.
2. Tester inbox -> outbox.
3. Valider `/analyze`.
4. Garder `bot_vision` en legacy preserve tant que la stabilisation n'est pas closee.

## REMAINING_GAP

Timers, inbox/outbox et route Telegram `/analyze` a stabiliser ; `bot_vision` legacy reste preserve.

## NEXT_GO

`GO_OPT_TRADING_VISION_RUNTIME_STABILIZATION_01`

## PROMOTION_CONDITIONS

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- stabilisation runtime closee,
- timers et flux inbox/outbox verifies,
- route `/analyze` validee,
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
- Wrappers : `cmd-vision`, `menu-vision`, `sanity-vision`.
- Pipeline headless : `scripts/run_bot_vision_headless_capture.sh`.
- Connaissance de la paire canonique actuelle.

## Commandes / acces

- Capture : `modules/vision_bot/`
- Analyse : `modules/bot_vision_step2/`
- Wrappers : `cmd-vision`, `menu-vision`, `sanity-vision`
- Pipeline headless : `scripts/run_bot_vision_headless_capture.sh`

## Procedure simple

1. Verifier l'etat avec `sanity-vision`.
2. Capturer un screenshot via `vision_bot`.
3. Lancer l'analyse via `bot_vision_step2`.
4. Verifier les artefacts dans Desk Pro ou Telegram.

## Verification PASS

- `vision_bot` capture correctement.
- `bot_vision_step2` produit des artefacts lisibles.
- `bot_vision` (legacy) n'est pas utilise.

## Limites

- Stabilisation runtime encore ouverte.
- `bot_vision` legacy a ne pas utiliser.
- Timers et route `/analyze` a verifier.

## Depannage

- `bot_vision` appele par erreur : utiliser `bot_vision_step2`.
- Capture echouee : verifier les logs de `vision_bot`.
- Analyse sans resultat : verifier le bridge Desk Pro/Telegram.

## Source canonique

- `docs/status/bot_vision_canonique.md`
- `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`
 - `docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/90_CLOSEOUT.md`

## RISKS

- À qualifier.
