---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_AI_EXTRACTION_FN_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_AI_EXTRACTION_FN_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_AI_EXTRACTION_FN_01

## Objectif

Remplacer le stub `extraction_fn` par une `extraction_fn` réelle injectable, gated par `VISION_AI_PROVIDER`.

Livrer `make_ai_extraction_fn()` : appel OpenAI vision (gpt-4o-mini) gated par env, testable offline avec `_call_fn` injectable, confiance < 0.60 → null enforced.

## Périmètre

- **IN** : `ai_extraction.py`, 14 tests, mise à jour `run_vision_capture.py`
- **OUT** : prod activation, send Telegram, adapter API Coinglass
- **Appel OpenAI** : uniquement si `VISION_AI_PROVIDER=openai` + `OPENAI_API_KEY` — jamais en tests CI

## Gates

| Env var | Effet |
|---|---|
| `VISION_AI_PROVIDER` non set | `make_ai_extraction_fn()` retourne [] sans erreur |
| `VISION_AI_PROVIDER=openai` | active le chemin OpenAI |
| `OPENAI_API_KEY` non set | retourne [] avec warning |
| `VISION_BOT_ENABLED=true` | requis en parallèle pour `run_capture` |

## Invariants extraction

1. Valeur illisible → `extracted_value = null` + note
2. `confidence < 0.60` → `extracted_value` forcé null même si AI renvoie une valeur
3. Aucune valeur inventée — seul le contenu du screenshot est source
4. Exception AI → liste vide, dégradation silencieuse

## Fichiers modifiés

| Fichier | Action |
|---|---|
| `modules/vision/coinglass/ai_extraction.py` | créé |
| `modules/vision/coinglass/tests/test_ai_extraction.py` | créé |
| `scripts/run_vision_capture.py` | mis à jour — stub → `make_ai_extraction_fn()` |
