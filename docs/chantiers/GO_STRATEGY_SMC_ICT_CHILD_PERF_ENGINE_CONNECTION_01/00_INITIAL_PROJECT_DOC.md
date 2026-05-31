---
doc_id: GO_STRATEGY_SMC_ICT_CHILD_PERF_ENGINE_CONNECTION_01_INITIAL
doc_type: initial_project_doc
go_id: GO_STRATEGY_SMC_ICT_CHILD_PERF_ENGINE_CONNECTION_01
parent_go: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01
status: OPEN
created_at: 2026-05-30
---

# GO_STRATEGY_SMC_ICT_CHILD_PERF_ENGINE_CONNECTION_01

## 1_CONTEXTE

`SMC_ICT_CHOCH_BOS_RETEST` est en `ACTIVE_PAPER` depuis 2026-05-30.
La promotion vers `ACTIVE_LIVE` requiert une `perf_engine_evidence` (définie dans
`30_ACTIVATION_SUMMARY.md` du GO parent).

Gap G04 du parent GO :

> Les métriques Perf Engine ne sont pas encore produites pour cette stratégie.
> Requis pour la promotion ACTIVE_LIVE.

### État actuel

| Couche | État |
|--------|------|
| `score_strategy_events()` dans `perf_engine.py` | EXISTS — filtre par `strategy_id`, évalue promotion gate |
| Callers de `score_strategy_events()` | AUCUN — fonction non branchée |
| Stockage ObservationEvents | ABSENT — ni JSONL, ni DB table |
| Endpoint `POST /perf/observation_event` | ABSENT |
| Endpoint `GET /perf/strategy/{id}/promotion_gate` | ABSENT |

---

## 2_OBJECTIF

Brancher le Perf Engine sur les ObservationEvents SMC_ICT :

1. **Stockage** — `state/observation_events.jsonl` (JSONL append-only, même pattern que `state/events.jsonl`)
2. **POST endpoint** — `POST /perf/observation_event` dans `perf/perf_app.py`
3. **GET endpoint** — `GET /perf/strategy/{strategy_id}/promotion_gate` qui appelle `score_strategy_events()`

Le format ObservationEvent attendu est défini dans
`docs/chantiers/GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01/30_ACTIVATION_SUMMARY.md` section 3.

---

## 3_PÉRIMÈTRE

### In scope

- `perf/perf_app.py` — ajouter 2 endpoints
- `state/observation_events.jsonl` — créer + persister via POST
- Tests unitaires pour les 2 nouveaux endpoints
- `docs/API.md` — documenter les 2 nouveaux endpoints

### Out of scope

- Automatisation du posting ObsEvents (→ `OBS_EVENT_AUTOMATION_01`)
- Telegram watch signal scoring (→ G03, futur GO)
- Modifier `score_strategy_events()` — la fonction existante est suffisante
- Modifier le schéma de `perf.db`

---

## 4_LIVRABLES

| Fichier | Action | Description |
|---------|--------|-------------|
| `perf/perf_app.py` | MODIFY | Ajouter `POST /perf/observation_event` + `GET /perf/strategy/{strategy_id}/promotion_gate` |
| `state/observation_events.jsonl` | CREATE (runtime) | Créé au premier POST, append-only |
| `tests/test_perf_observation_endpoints.py` | CREATE | Tests unitaires ≥ 10 |
| `docs/API.md` | MODIFY | Documenter les 2 nouveaux endpoints |
| `docs/chantiers/GO_STRATEGY_SMC_ICT_CHILD_PERF_ENGINE_CONNECTION_01/20_ACCEPTANCE_REPORT.md` | CREATE | Verdict final |

---

## 5_VALIDATIONS

```bash
python3 -m pytest tests/test_perf_observation_endpoints.py -q
git diff --check
./scripts/verify_all.sh
```

Critères PASS :
- `POST /perf/observation_event` persiste en `state/observation_events.jsonl`
- `GET /perf/strategy/SMC_ICT_CHOCH_BOS_RETEST/promotion_gate` retourne `promotion_verdict`
- Tous les tests passent
- `git diff --check` = clean

---

## 6_CONTRAINTES

- Ne pas modifier `score_strategy_events()` — interface publique stable
- Ne pas modifier le schéma de `perf.db`
- Ne pas toucher `secrets/`
- Ne pas faire de live trading
- Suivre le pattern JSONL de `state/events.jsonl` pour le stockage

---

## 7_VERDICT_CIBLE

```
PASS_PERF_ENGINE_CONNECTED
ou
BLOCKED_WITH_REASON
```
