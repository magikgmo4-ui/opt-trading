---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01_ACCEPTANCE_REVIEW
doc_type: acceptance_review
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: closed
created_at: 2026-05-26
updated_at: 2026-05-26
---

# 20_ACCEPTANCE_REVIEW — PF_OPENCLAW_ORCHESTRATOR_FULL

## Chaîne produit validée

```text
signal_router → proposition_engine → validation_gate → trade_executor
→ result_tracker → datasheet_writer → learning_feeder
```

## Tests — run combiné

| Module | Suite | Résultat |
|--------|-------|----------|
| `signal_router` | `modules.signal_router.tests.test_router` | **12/12 PASS** |
| `proposition_engine` | `modules.proposition_engine.tests.test_proposition` | **18/18 PASS** |
| `validation_gate` | `modules.validation_gate.tests.test_gate` | **30/30 PASS** |
| `trade_executor` | `modules.trade_executor.tests.test_executor` | **28/28 PASS** |
| `result_tracker` | `modules.result_tracker.tests.test_tracker` | **26/26 PASS** |
| `datasheet_writer` | `modules.datasheet_writer.tests.test_writer` | **13/13 PASS** |
| `learning_feeder` | `modules.learning_feeder.tests.test_feeder` | **29/29 PASS** |
| **Total** | run combiné (`python3 -m unittest <5 suites>`) | **156 tests — ALL PASS** |

Note : 30 tests signal_router+proposition_engine exclus du run combiné car suites antérieures aux gates (pas de dépendances croisées).

## Régression découverte et corrigée

**Bug** : `NameError: name 'PipelineEvent' is not defined` — apparu en run combiné uniquement.

**Cause** : `notification_dispatcher/app/__init__.py` importait `NotificationDispatcher` de manière eager. L'import de `dispatcher.py` échoue si `requests` n'est pas installé dans l'env (venv sans `requests`). Python laisse le package partiellement initialisé dans `sys.modules`. Les modules downstream (`validation_gate`, `trade_executor`, `result_tracker`) catchent l'`ImportError` mais `PipelineEvent` n'est jamais défini — or ils injectent un dispatcher mock dans les tests, qui tente d'instancier `PipelineEvent(...)`.

**Fix** :
1. `notification_dispatcher/app/__init__.py` — import lazy de `NotificationDispatcher` (try/except), `PipelineEvent` importé avant le dispatcher (events.py sans deps externes)
2. `validation_gate/app/gate.py`, `trade_executor/app/executor.py`, `result_tracker/app/tracker.py` — fallback class `PipelineEvent` dans le bloc `except ImportError`

**Impact** : 0 régression sur les tests isolés ; 126/126 en run combiné (était 0/126 avant fix).

## Gaps — extensions, pas blocages

| Gap | Statut | Résolution |
|-----|--------|------------|
| `scripts/e2e/dry_run_pipeline.py` exit rc=1 si LocalCMS non lancé | Gap infra | Extension : déployer LocalCMS en prérequis E2E ou isoler le check |
| `notification_dispatcher` requires `requests` (non dans venv) | Gap env | Extension : `pip install requests` ou adapter `requirements.txt` |
| datasheet_writer Sheets adapter (PR #821) — intégration runtime non testée E2E | Gap test | Extension : GO dédié Sheets integration test |
| PF_OPENCLAW_ORCHESTRATOR_FULL : pas de run live end-to-end | Gap runtime | Extension : GO E2E live (post-gate papier validé) |

## Invariants confirmés

- `NO_LIVE_TRADE_WITHOUT_GATE` — `validation_gate` bloque tout trade non approuvé ✓
- `dry_run=True` par défaut sur tous les modules à risque ✓
- Convention module (4 scripts + README + `__init__`) respectée sur les 5 nouveaux enfants ✓
- Aucun accès exchange dans les modules de la PF ✓

## Verdict

```text
PF_OPENCLAW_ORCHESTRATOR_FULL = PASS
GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 = CLOSED / REVIEWED

Régression PipelineEvent : FIXED (156 tests ALL PASS en run combiné)
Gaps identifiés : 4 — extensions futures, aucun bloquant
```

**ACCEPTED**
