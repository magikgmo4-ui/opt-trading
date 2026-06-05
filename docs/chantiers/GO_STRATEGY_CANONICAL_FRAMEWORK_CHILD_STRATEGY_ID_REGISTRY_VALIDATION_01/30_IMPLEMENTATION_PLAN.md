---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_ID_REGISTRY_VALIDATION_01
doc_type: implementation_plan
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 30_IMPLEMENTATION_PLAN

## Plan d'implémentation du validateur

---

## 1_VALIDATEUR

Fichier : `tools/strategy/validate_strategy_registry.py`

### Rôle

```text
1. Lire 95_STRATEGY_REGISTRY.md
2. Extraire les strategy_id registrés (section 2_REGISTRY)
3. Scanner les fichiers pipeline contenant strategy_id
4. Comparer les valeurs trouvées vs registre
5. Signaler les inconnues en WARNING
6. Code retour 0 si OK / warning, 1 si erreur
```

### Surfaces scannées

```text
modules/signal_router/app/schema.py
modules/signal_router/app/router.py
modules/proposition_engine/app/schema.py
modules/proposition_engine/app/builder_prompt.py
modules/proposition_engine/app/__main__.py
modules/notification_dispatcher/app/events.py
modules/trading_realtime_v1/app/runtime_loop_v1.py
modules/trading_realtime_v1/app/event_bridge_v1.py
modules/trading_lab_v1/app/trading_lab_v1.py
tests/e2e/test_e2e_dry_run_pipeline.py
tests/test_kill_switch_telegram_validation.py
```

Les fichiers de test (`tests/`, `**/tests/`) sont scannés mais les valeurs
trouvées sont marquées `TEST_CONTEXT`.

### Mode de détection

```text
- Regex : strategy_id\s*=\s*["']([^"']+)["']
- Regex : STRATEGY_ID\s*=\s*["']([^"']+)["']
- Regex : "strategy_id":\s*["']([^"']+)["']
- Variable : toute valeur string assignée à strategy_id ou STRATEGY_ID
```

---

## 2_EXÉCUTION

```bash
python tools/strategy/validate_strategy_registry.py
```

### Sortie attendue

```text
=== Strategy ID Registry Validation ===
Registry: docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md
Registered: xau_session_open_v1, SMC_ICT_CHOCH_BOS_RETEST

[TARGET FILES]
  ✓ modules/trading_realtime_v1/app/runtime_loop_v1.py  → xau_session_open_v1 (REGISTERED)
  ✓ modules/trading_realtime_v1/app/event_bridge_v1.py  → xau_session_open_v1 (REGISTERED)
  WARNING: modules/signal_router/tests/test_router.py   → breakout_v2 (NOT REGISTERED — test context)
  WARNING: modules/signal_router/app/router.py          → [dynamic fallback scan]
  ...

=== Result: WARNINGS=3, UNKNOWN=0 ===
```

---

## 3_NON_COUVERT

```text
- Pas de validation des strategy_id dans les JSONL runtime (state/)
- Pas de validation des events produits (post-hoc)
- Pas de pre-commit hook (futur phase 4)
- Pas de blocage CI (futur phase 2-3)
```

## RISKS

- À qualifier.
