---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_AI_EXTRACTION_FN_01_REPRISE
doc_type: reprise_point
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_AI_EXTRACTION_FN_01
status: active
created_at: 2026-05-23
---

# 90_REPRISE_POINT

## Ordre robuste post-merge

```
1. merge ce PR
2. configurer VISION_BOT_ENABLED=true + VISION_AI_PROVIDER=openai + OPENAI_API_KEY sur staging
3. lancer 3 runs : python scripts/run_vision_capture.py
4. valider : python scripts/run_vision_capture.py --validate
5. si PASS → child Telegram sender réel (option B)
```

## Commande staging rapide

```bash
# Run unique
VISION_BOT_ENABLED=true VISION_AI_PROVIDER=openai OPENAI_API_KEY=sk-... \
  python scripts/run_vision_capture.py --symbol BTCUSDT --timeframe 1H

# Validation gate
VISION_BOT_ENABLED=true python scripts/run_vision_capture.py --validate --required 3
```

## Blocages potentiels

| Blocage | Cause | Fix |
|---|---|---|
| 0 détections | Playwright charge la page mais le contenu n'est pas rendu | augmenter `--wait-ms` |
| confidence toujours < 0.60 | Screenshot flou / mauvais viewport | ajuster viewport dans `make_playwright_browser_fn` |
| OpenAI erreur 429 | Rate limit | retry avec backoff ou changer model |
| Gate INSUFFICIENT | Moins de 3 runs dans events.jsonl | relancer jusqu'à 3 |
