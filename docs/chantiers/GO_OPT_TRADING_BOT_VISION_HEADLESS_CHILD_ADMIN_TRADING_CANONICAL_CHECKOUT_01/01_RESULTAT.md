---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_ADMIN_TRADING_CANONICAL_CHECKOUT_01__RESULTAT
doc_type: resultat
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_ADMIN_TRADING_CANONICAL_CHECKOUT_01
status: delivered
owner: OpenCode
created_at: 2026-05-31
---

# Résultat

## Preuve distante

Checkout canonique créé sur `admin-trading` :

- chemin : `/home/ghost/opt-trading-mainline-clean`
- branche : `sot/mainline`
- HEAD local : `5d1ab214`
- HEAD remote : `5d1ab214`

État Git observé :

```text
## sot/mainline...origin/sot/mainline
```

## Surface bot vision présente

- `coinglass_ocr_analyzer.py`
- `news_sentiment_analyzer.py`
- `run_vision_pipeline.py`
- `schedule_orchestrator.py`
- `signal_validator.py`
- `telegram_filter.py`

## Séparation opératoire obtenue

### Runtime mutable

- `/opt/trading`
- checkout historique sale mais runtime stabilisé

### Checkout canonique propre

- `/home/ghost/opt-trading-mainline-clean`
- propre
- aligné sur `origin/sot/mainline`
- utilisable pour audit, diff, tests de référence, patchs propres

## Verdict

Le besoin "doit être propre" est rempli sans perturber le runtime opérateur actif.
