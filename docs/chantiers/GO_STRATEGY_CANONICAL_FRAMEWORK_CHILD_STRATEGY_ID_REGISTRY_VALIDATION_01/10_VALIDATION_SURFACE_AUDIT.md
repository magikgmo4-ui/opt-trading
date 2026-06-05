---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_ID_REGISTRY_VALIDATION_01
doc_type: validation_surface_audit
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 10_VALIDATION_SURFACE_AUDIT

## Audit des surfaces utilisant strategy_id

---

## 1_SURFACES_PIPELINE

### 1.1_signal_router

| Fichier | Ligne | Usage |
|---------|-------|-------|
| `app/schema.py:21` | `SignalIn.strategy_id: str = ""` | Champ optionnel entrant |
| `app/schema.py:33` | `NormalizedSignal.strategy_id: str` | Champ requis normalisé |
| `app/router.py:44` | Fallback `raw.get("engine", "")` | Si strategy_id absent |
| `app/router.py:56` | `signal_in.strategy_id or signal_in.engine` | Fallback engine |
| `tests/test_router.py:18` | `"breakout_v2"` | Test value — non registré |
| `tests/test_router.py:77` | `"strat_v1"` | Test fallback — non registré |

**Verdict** : passage possible de strategy_id non registré.

### 1.2_proposition_engine

| Fichier | Ligne | Usage |
|---------|-------|-------|
| `app/schema.py:13` | `NormalizedSignal.strategy_id: str` | Requis |
| `app/builder_prompt.py:12` | `strategy={signal.strategy_id}` | Injecté dans prompt LLM |
| `app/__main__.py:29` | `--strategy-id` arg CLI | Entrée utilisateur |
| `tests/test_proposition.py:26` | `"test_v1"` | Test value — non registré |
| `tests/test_proposition.py:34` | `"s1"` | Test value — non registré |

**Verdict** : passage possible de strategy_id non registré.

### 1.3_notification_dispatcher

| Fichier | Ligne | Usage |
|---------|-------|-------|
| `app/events.py:38` | Template HTML Telegram avec `{strategy_id}` | Affichage |
| `tests/test_dispatcher.py:28` | `"v1"` | Test value — non registré |
| `tests/test_dispatcher.py:61` | `"t"` | Test value — non registré |

**Verdict** : passage possible de strategy_id non registré.

### 1.4_trading_realtime_v1

| Fichier | Ligne | Usage |
|---------|-------|-------|
| `app/runtime_loop_v1.py:13` | `STRATEGY_ID = "xau_session_open_v1"` | Hardcodé — **registré** |
| `app/event_bridge_v1.py:11` | `STRATEGY_ID = "xau_session_open_v1"` | Hardcodé — **registré** |

**Verdict** : conforme.

### 1.5_trading_lab_v1

| Fichier | Ligne | Usage |
|---------|-------|-------|
| `app/trading_lab_v1.py:396` | Fallback `"xau_session_open_v1"` | **Registré** |
| `tests/test_core_runner_v1.py:38` | `"xau_session_open_v1"` | **Registré** |

**Verdict** : conforme.

### 1.6_decision_engine

Aucune référence à `strategy_id`. Scope négatif.

### 1.7_tests / e2e

| Fichier | Usage |
|---------|-------|
| `tests/e2e/test_e2e_dry_run_pipeline.py:321` | `"test"` — non registré |

---

## 2_INVENTAIRE_DES_STRATEGY_ID_CONNUS

| Valeur | Source | Registré ? |
|--------|--------|-----------|
| `xau_session_open_v1` | runtime_loop, event_bridge, trading_lab | **Oui** |
| `SMC_ICT_CHOCH_BOS_RETEST` | child GO SMC/ICT (doc) | **Oui** |
| `breakout_v2` | signal_router test | Non (test) |
| `strat_v1` | signal_router test (fallback) | Non (test) |
| `test_v1` | proposition_engine test | Non (test) |
| `s1` | proposition_engine test | Non (test) |
| `v1` | notification_dispatcher test | Non (test) |
| `t` | notification_dispatcher test | Non (test) |
| `test` | e2e dry_run test | Non (test) |

**Total : 9 valeurs uniques. 2 registrées, 7 test-only non registrées.**

## RISKS

- À qualifier.
