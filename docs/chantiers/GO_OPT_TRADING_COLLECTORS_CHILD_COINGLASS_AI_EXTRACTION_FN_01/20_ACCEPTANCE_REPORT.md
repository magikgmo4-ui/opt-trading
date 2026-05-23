---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_AI_EXTRACTION_FN_01_ACCEPTANCE
doc_type: acceptance_report
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_AI_EXTRACTION_FN_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: accepted
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_ACCEPTANCE_REPORT

## Verdict : ACCEPTED

## Résultats tests

```
modules/vision/coinglass/tests/test_ai_extraction.py — 14 passed in 0.09s
```

| Test ID | Cas | Résultat |
|---|---|---|
| TC-AI-01 | Réponse valide → 2 détections | PASS |
| TC-AI-02 | Valeurs correspondent à la réponse | PASS |
| TC-AI-03 | confidence < 0.60 → extracted_value null | PASS |
| TC-AI-04 | null dans réponse → null préservé | PASS |
| TC-AI-05 | JSON malformé → liste vide | PASS |
| TC-AI-06 | Clé detections absente → liste vide | PASS |
| TC-AI-07 | evidence_ref propagé | PASS |
| TC-AI-08 | Provider non set → [] sans exception | PASS |
| TC-AI-09 | Provider inconnu → [] | PASS |
| TC-AI-10 | OpenAI sans API key → [] | PASS |
| TC-AI-11 | OpenAI avec mock _call_fn → 2 détections | PASS |
| TC-AI-12 | _call_fn exception → [] silencieux | PASS |
| TC-AI-13 | Provider depuis env VISION_AI_PROVIDER | PASS |
| TC-AI-14 | low conf via mock → null dans sortie | PASS |

## Fichiers livrés

| Fichier | Rôle |
|---|---|
| `modules/vision/coinglass/ai_extraction.py` | make_ai_extraction_fn() + _parse_ai_response() |
| `modules/vision/coinglass/tests/test_ai_extraction.py` | 14 tests offline |
| `scripts/run_vision_capture.py` | stub remplacé par make_ai_extraction_fn() |

## État gate staging

Avec `VISION_AI_PROVIDER=openai` + `OPENAI_API_KEY` + `VISION_BOT_ENABLED=true` :
- Playwright capture un screenshot
- `make_ai_extraction_fn()` appelle OpenAI vision
- Si ≥1 détection confidence ≥ 0.60 → run PASS au staging validator
- 3 runs PASS → gate prod franchissable

## Prochaine étape

Valider 3 runs PASS en staging, puis child Telegram sender réel (option B).
