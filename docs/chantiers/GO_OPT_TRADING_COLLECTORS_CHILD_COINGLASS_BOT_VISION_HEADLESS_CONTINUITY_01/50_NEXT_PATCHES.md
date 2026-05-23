---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01_NEXT_PATCHES
doc_type: next_patches
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 50_NEXT_PATCHES

## Roadmap

### PATCH-A1 : schema `vision_context.coinglass.v1` (priorité A)

Créer la dataclass Python `VisionContextCoinglassV1` avec `validate()` et `to_json()`.

Scope :
- `modules/vision/coinglass/vision_context_v1.py` (ou `packages/collectors_core/`)
- Dataclass : `VisionContextCoinglassV1`, `Detection`, `VisionRefs`
- Invariants : confidence threshold, null si non lisible, input_class check
- Tests : 6 test cases

Prerequis : aucun — peut démarrer immédiatement.

---

### PATCH-A2 : fixture + parser mock (priorité A)

Créer fixtures et parser mockable pour les tests.

Scope :
- `tests/fixtures/vision/coinglass/` — fixtures JSON + image synthétique
- `modules/vision/coinglass/parser.py` — parser mockable (pas d'OCR réel)
- Tests : 4 test cases

Prerequis : PATCH-A1 terminé.

---

### PATCH-A3 : Desk Pro read-only consumer (priorité A)

Desk Pro lit `data/deskpro/inputs/vision_context/coinglass/latest.json` en read-only.

Scope :
- `modules/desk_pro/service/vision_context_reader.py` — analogue à `market_metrics_reader.py`
- Intégration dans `aggregator.py` : `_augment_vision_context(snap)`
- Tests : 5 test cases

Prerequis : PATCH-A2 terminé.

---

### PATCH-B1 : headless capture runtime (priorité B — gated)

Activer le bot vision headless en staging.

Scope :
- `modules/vision/coinglass/headless_capture.py` — Playwright/Selenium + screenshot
- `modules/vision/coinglass/runner.py` — orchestrateur : capture → parse → write latest.json
- Gate : 3 runs PASS consécutifs en staging avant activation prod

Prerequis : PATCH-A3 terminé. Clé d'accès Coinglass non requise (interface publique).

---

### PATCH-B2 : Telegram/reporting summary (priorité B — optionnel)

Résumé read-only des données vision Coinglass vers Telegram.

Scope :
- Lecture `data/vision/coinglass/latest.json`
- Formatage message avec confidence et warnings
- Aucune valeur inventée

Prerequis : PATCH-B1 stable.

---

## Ordre recommandé

```
A1 → A2 → A3 → (B1 gated staging) → B2 optionnel
```

A1–A3 sont livrables sans headless actif — ils valident le contrat et le consumer.
B1 nécessite un environnement staging avec navigateur headless disponible.

---

## Child GO logique suivant

```text
GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_VISION_CONTEXT_SCHEMA_01
```

Ou, si la surface vision est élargie :

```text
GO_OPT_TRADING_VISION_CHILD_COINGLASS_CONTEXT_SCHEMA_01
```
