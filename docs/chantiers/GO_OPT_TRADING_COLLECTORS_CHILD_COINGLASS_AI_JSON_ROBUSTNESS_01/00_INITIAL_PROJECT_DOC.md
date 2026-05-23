---
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_AI_JSON_ROBUSTNESS_01
doc_type: initial_project_doc
repo: opt-trading
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: accepted
created_at: 2026-05-23
branch: go/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_AI_JSON_ROBUSTNESS_01
surface: runtime — ai_extraction.py + tests
runtime_mutation: true
---

# 00_INITIAL_PROJECT_DOC
## GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_AI_JSON_ROBUSTNESS_01

---

## 1_MASTER_TARGET

```text
Éliminer les échecs intermittents "AI response JSON could not be parsed"
observés au run timer 08:00 EDT (2026-05-23).

Fix : response_format={"type": "json_object"} dans _call_openai()
→ OpenAI garantit une réponse JSON valide côté API.
```

---

## 2_CONTEXTE

Run timer 08:00 EDT → WARNING "AI response JSON could not be parsed" → 0 detections.
Run staging 07:51 → 5 detections, conf=1.00, PASS.

La divergence est due à une réponse OpenAI en prose (sans JSON) sur certains runs.
`response_format={"type": "json_object"}` force le modèle à retourner du JSON strict,
supporté par gpt-4o-mini.

---

## 3_DELIVERABLES

| Fichier | Changement |
|---|---|
| `modules/vision/coinglass/ai_extraction.py` | `response_format={"type": "json_object"}` dans `_call_openai()` |
| `tests/test_vision_ai_extraction.py` | 14 tests couvrant parse, provider, injection, edge cases |

---

## 4_CLOSEOUT

PASS : 14/14 tests, 768/768 suite complète. runtime_mutation=true, 1 ligne modifiée.
