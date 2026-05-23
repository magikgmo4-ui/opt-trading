---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01_VALIDATION_AND_EVIDENCE_PLAN
doc_type: validation_plan
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 40_VALIDATION_AND_EVIDENCE_PLAN

## Objectif

Définir les critères de validation pour chaque patch du child. Aucun test n'est exécuté dans ce child (doc-only). Les tests sont des specs pour les patches futurs.

---

## PATCH-A1 : schema `vision_context.coinglass.v1`

### Tests attendus

| ID | Description | Critère PASS |
|---|---|---|
| TC-SCHEMA-01 | Payload minimal valide | `validate()` PASS sans erreur |
| TC-SCHEMA-02 | `extracted_value = null` si non lisible | PASS — null autorisé |
| TC-SCHEMA-03 | `confidence < 0.5` sans warning → BLOCKED | ValueError levée |
| TC-SCHEMA-04 | `input_class` ≠ `vision_context.coinglass.v1` → BLOCKED | ValueError levée |
| TC-SCHEMA-05 | `extracted_value` non-null mais `confidence = 0` → BLOCKED | ValueError levée |
| TC-SCHEMA-06 | Sérialisation JSON roundtrip | Payload reconstruit identique |

---

## PATCH-A2 : fixture + parser mock

### Fixtures requises

```text
tests/fixtures/vision/coinglass/
  screenshot_mock_liquidations.png   — image synthétique avec valeurs lisibles
  vision_coinglass_v1_valid.json     — payload vision_context.coinglass.v1 valide
  vision_coinglass_v1_low_conf.json  — payload avec confidence < 0.5 et warning
  vision_coinglass_v1_null_vals.json — payload avec extracted_value null
```

### Tests attendus

| ID | Description | Critère PASS |
|---|---|---|
| TC-PARSER-01 | Mock extraction depuis fixture image | 2+ détections retournées |
| TC-PARSER-02 | Confidence threshold appliqué | valeur < 0.6 → null + warning |
| TC-PARSER-03 | Fichier absent → dégradation silencieuse | liste vide, pas d'exception |
| TC-PARSER-04 | Freshness state `stale` si screenshot > 4h | `freshness_state = "stale"` |

---

## PATCH-A3 : Desk Pro read-only consumer

### Tests attendus

| ID | Description | Critère PASS |
|---|---|---|
| TC-DESKPRO-01 | Lecture `vision_context/coinglass/latest.json` | Métriques injectées dans Snapshot |
| TC-DESKPRO-02 | Fichier absent → Snapshot sans métriques vision | Pas d'exception |
| TC-DESKPRO-03 | `input_class` incorrect → ignoré | Pas d'injection |
| TC-DESKPRO-04 | Confidence < seuil → Metric.quality bas | quality ≤ 0.5 |
| TC-DESKPRO-05 | Aucun write dans `market_metrics/latest.json` | Fichier inchangé après lecture |

---

## PATCH-B1 : headless capture runtime (gated)

### Critères de gate

| Critère | Condition PASS |
|---|---|
| Screenshot produit | Fichier PNG non vide dans `data/vision/coinglass/raw/` |
| Parsing non vide | Au moins 1 détection avec confidence ≥ 0.6 |
| `latest.json` mis à jour | `screenshot_ts` = run_ts ± 60s |
| Aucun write hors vision/ | Vérification `git diff` sur data/ |
| Smoke Desk Pro | `GET /desk/snapshot` → métriques vision présentes dans output |

### Gate bloquante

Ne pas activer PATCH-B1 en production sans au moins 3 runs consécutifs PASS en staging.

---

## PATCH-B2 : Telegram/reporting summary

### Critères

| Critère | PASS |
|---|---|
| Message formaté sans hallucination | Valeurs = valeurs extraites uniquement |
| Confidence signalée si < 0.85 | Warning explicite dans message |
| Aucune valeur inventée | Vérification manuelle sur 5 runs |

---

## Critères de confiance globaux

| Niveau | Seuil | Comportement attendu |
|---|---|---|
| Haute confiance | ≥ 0.85 | Valeur utilisable pour context Desk Pro |
| Confiance partielle | 0.60 – 0.84 | Valeur signalée avec warning |
| Confiance basse | < 0.60 | `extracted_value = null` recommandé |

---

## Evidence requise pour PASS du child

- [ ] Schéma `vision_context.coinglass.v1` validé sur fixture (PATCH-A1)
- [ ] Parser mock passe 4 tests fixture (PATCH-A2)
- [ ] Desk Pro consumer read-only passe 5 tests (PATCH-A3)
- [ ] Aucun write hors `data/vision/coinglass/` et `data/deskpro/inputs/vision_context/coinglass/`
