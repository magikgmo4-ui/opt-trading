# 00_INITIAL_PROJECT_DOC

GO: `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_CAPTURE_FAILURE_CLASSIFICATION_01`

## Objectif

Ajouter au bot_vision_headless une classification explicite des captures bloquées ou visuellement invalides, afin d'éviter de promouvoir des screenshots inutilisables vers le pipeline runtime.

## Contexte

- Commit dynamic load strategy: `53df319e`
- BTC capture OK mais networkidle intermittent
- XAU produit PNG/JSON mais image spinner (inutilisable humainement)
- Coinglass timeout persistant
- Aucun restart, .env, trade

## Invariants

1. Ne pas modifier `profiles.example.json`
2. Ne pas promouvoir P0 vers timer
3. Ne pas redémarrer service/timer
4. Ne rien supprimer
5. Ne pas archiver/comprimer
6. Ne pas lire .env
7. Ne pas trader

## Livrables

1. `capture_headless.js` modifié : statuts ready/blocked/invalid_visual
2. `profiles.failure.classification.smoke.local.json`
3. Docs chantier (00-40)
4. Index inbox
