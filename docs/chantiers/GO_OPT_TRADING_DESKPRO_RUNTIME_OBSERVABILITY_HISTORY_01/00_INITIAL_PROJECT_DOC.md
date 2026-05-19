---
go_id: GO_OPT_TRADING_DESKPRO_RUNTIME_OBSERVABILITY_HISTORY_01
doc_type: initial_project_doc
repo: opt-trading
status: DRAFT
created_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_RUNTIME_OBSERVABILITY_HISTORY_01

## 1_MASTER_TARGET

Étendre l'observabilité Desk Pro (PR #544) avec historique, erreurs récentes, statut source par endpoint, et UI structurée.

## 3_INITIAL_NEED

PR #544 a livré `/desk/status` brut (JSON) et une card Pipeline Status affichant le JSON.
Il manque : erreurs visibles, statut source par endpoint (live/fixture/mock), et une UI structurée.

## 5_AUDIT — ÉTAT AVANT

| Existant | Manquant |
|---|---|
| `/desk/status` avec raw JSON | Pas d'erreurs exposées |
| Pipeline Status card | Pas de badges vert/rouge |
| `_probe_url()` retourne None sur échec | Perte d'info d'erreur |
| Sources implicites (step2_mock) | Pas de distinction live/fixture/mock par endpoint |

## 7_CANONICAL_STATE

- `sot/mainline` jour avec PR #544 mergée
- Tests: 322/322 PASS
- Services: webhook:8000, perf+desk:8010

## 10_IMPLEMENTATION

### routes.py

1. `_desk_errors` — in-memory FIFO error log (max 50)
2. `_probe_url` modifiée — enregistre l'erreur + timestamp dans `_desk_errors`
3. `_source_mode(url_path)` — détermine live/fixture/mock par endpoint
4. `/desk/status` enrichi :
   - `sources` — objet source mode par endpoint
   - `error_count` — nombre total d'erreurs enregistrées
   - `recent_errors` — 10 dernières erreurs
   - `perf_open` — positions ouvertes
   - `webhook_metrics` — métriques webhook
5. Nouveau `GET /desk/errors` — historique erreurs

### page.py

1. Pipeline Status card remplacée par :
   - 3 badges Desk Pro / Webhook / Perf (vert/rouge)
   - Sources row (live/fixture/mock)
   - Error row si erreurs
   - Raw JSON disponible en `<details>` replié

## 13_ESTABLISHED

| Fait | Preuve |
|---|---|
| `_desk_errors` FIFO | routes.py L19-20 |
| `_probe_url` enregistre les erreurs | routes.py L30-35 |
| `_source_mode` distingue live/fixture/mock | routes.py L38-42 |
| Sources exposées dans `/desk/status` | routes.py L81-89 |
| `GET /desk/errors` endpoint | routes.py L100-104 |
| UI structurée avec badges | page.js refreshStatus |

## 16_TODO

1. ✅ routes.py modifié
2. ✅ page.py modifié
3. Tester les services
4. Tests 322/322 PASS
5. Créer PR
