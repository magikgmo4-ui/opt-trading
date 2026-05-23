---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE_POINT

## Etat au moment de ce GO

- Parent `GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01` : **ACCEPTED** (PR #707)
- binance_derivatives : FULL (6/6)
- bitget : FULL (6/6)
- coinglass : NOT_PROVEN_RUNTIME_ADAPTER (permanent — payant)

## Ce GO

Doc-only. Aucun runtime modifié. Cadrage de la voie Coinglass → bot vision headless.

## Prochaine session

Reprendre par PATCH-A1 : créer `VisionContextCoinglassV1` dataclass dans `modules/vision/coinglass/`.

Commandes de vérification rapide :

```bash
ls docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01/
git log --oneline -5
git diff --name-only origin/sot/mainline...HEAD
```

## Invariants à ne pas oublier

- `vision_context.coinglass.v1` ≠ `market_metrics.v1`
- Bot vision = source visuelle externe, pas adapter API
- Coinglass reste `NOT_PROVEN_RUNTIME_ADAPTER` dans tout rapport collectors
- Aucune valeur Coinglass inventée ou interpolée
- Confidence < 0.60 → `extracted_value = null`
