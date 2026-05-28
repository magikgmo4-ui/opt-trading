---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01_DEDUP_QUALIFICATIONS
doc_type: dedup_audit
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01
status: open
lifecycle_stage: registry_v1_complete
topic_keys: [dedup, duplicates, code_ops, audit_first]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 10_DEDUP_QUALIFICATIONS

Qualification des 6 doublons suspects identifiés dans
`GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/40_RISK_MAP.md`.

---

## D01 — modules/perf/engine/ vs modules/perf_engine/

| Champ | Valeur |
|---|---|
| Suspect | `modules/perf/engine/app/perf_engine.py` (12 lignes) |
| Canonique | `modules/perf_engine/app/perf_engine.py` (444 lignes) |
| Type | FAUX DOUBLON — wrapper de compatibilité |

**Preuve** : `modules/perf/engine/app/perf_engine.py` contient seulement :

```python
"""Compatibility wrapper around the historical PERF engine entrypoint.
This keeps the old module path working while exposing a canonical family path:
`modules.perf.engine.app.perf_engine`.
"""
```

**Verdict** : `modules/perf_engine/` est la source canonique. `modules/perf/engine/` est un
wrapper de rétrocompatibilité intentionnel. Aucune suppression sans identifier les
consommateurs de l'ancien chemin.

**Action registre** : `modules/perf_engine/app/perf_engine.py` → `ACTIVE` / `KEEP`.
`modules/perf/engine/app/perf_engine.py` → `CANDIDATE` / `REGISTER_ONLY` (wrapper compat).

---

## D02 — execution_engine/executor.py vs trade_executor/executor.py

| Champ | Valeur |
|---|---|
| Path A | `modules/execution_engine/executor.py` |
| Path B | `modules/trade_executor/app/executor.py` |
| Type | FAUX DOUBLON — deux executors pour deux flux distincts |

**Preuve** :

- `webhook_server.py:15` importe `from modules.execution_engine.executor import Executor`
  → flux production TradingView → risk → execution
- `scripts/e2e/dry_run_pipeline.py:415` importe `from modules.trade_executor.app.executor import TradeExecutor`
  → flux dry_run / validation_gate → trade_executor

**Verdict** : rôles distincts, flux distincts. Pas de doublon.

**Action registre** :
- `modules/execution_engine/executor.py` → `ACTIVE` / `KEEP` (webhook runtime)
- `modules/trade_executor/app/executor.py` → `ACTIVE` / `KEEP` (dry_run pipeline)

---

## D03 — modules/engines/router.py vs modules/router/

| Champ | Valeur |
|---|---|
| Path A | `modules/engines/router.py` |
| Path B | `modules/router/` (scripts only — aucun code Python) |
| Type | FAUX DOUBLON — implémentation vs module shell vide |

**Preuve** :

- `modules/engines/router.py` importe `from modules.engines.registry import get_engine, list_engines`
  et est importé par `modules/health/checker.py`
- `modules/router/` ne contient que `__init__.py`, `README.md`, `scripts/` — aucun code applicatif

**Verdict** : `modules/engines/router.py` est le router réel. `modules/router/` est un module
shell (wrapper ou placeholder). Pas de doublon fonctionnel.

**Action registre** :
- `modules/engines/router.py` → `ACTIVE` / `KEEP`
- `modules/router/` → `CANDIDATE` / `BLOCKED_NEEDS_OWNER` (qualifier usage réel)

---

## D04 — bitget_bridge.py vs modules/simex_bitget_bridge/

| Champ | Valeur |
|---|---|
| Path A | `bitget_bridge.py` (racine repo) |
| Path B | `modules/simex_bitget_bridge/app/simex_bitget_bridge.py` |
| Type | FAUX DOUBLON — entrypoint wrapper vs implémentation |

**Preuve** : `bitget_bridge.py:1` contient :

```python
from modules.simex_bitget_bridge.app.simex_bitget_bridge import main
```

**Verdict** : `bitget_bridge.py` est un entrypoint shell qui délègue à `simex_bitget_bridge`.
`simex_bitget_bridge` est l'implémentation canonique.

**Action registre** :
- `modules/simex_bitget_bridge/app/simex_bitget_bridge.py` → `ACTIVE` / `KEEP`
- `bitget_bridge.py` → `ACTIVE` / `KEEP` (entrypoint CLI canonique)

---

## D05 — scripts doublés dans execution_engine/scripts/

| Champ | Valeur |
|---|---|
| Scripts A (canoniques) | `cmd.sh`, `menu.sh`, `sanity_check.sh` |
| Scripts B (doublés) | `execution_engine_cmd.sh`, `execution_engine_menu.sh`, `execution_engine_sanity_check.sh` |
| Type | ANOMALIE — scripts différents, pas identiques |

**Preuve** : diff entre `cmd.sh` et `execution_engine_cmd.sh` confirme des différences
structurelles (chemins, logique de dispatch différente).

**Verdict** : Les scripts doublés coexistent sans être des alias. L'un des deux ensembles
est probablement l'ancien format. À qualifier dans un batch de nettoyage dédié.

**Action registre** : `modules/execution_engine/scripts/cmd.sh` → KEEP (canonique).
Scripts `execution_engine_*` → `DUPLICATE_SUSPECT` / `BLOCKED_NEEDS_CONSUMER_AUDIT`.

**Lot requis** : `GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01`.

---

## D06 — répertoires .bak dans modules/

| Champ | Valeur |
|---|---|
| Path A | `modules/install_module_openclaw.bak_20260314/` |
| Path B | `modules/ops_wrappers.bak/` |
| Type | REMNANTS — backups commitées dans le repo |

**Preuve** : présents dans `git ls-files`. Noms explicitement datés (.bak_20260314) ou
suffixés .bak.

**Verdict** : DELETE_CANDIDATE. Pas de consommateur connu. Mais la suppression nécessite
une preuve explicite (grep import) avant tout commit de suppression.

**Action registre** : `DELETE_CANDIDATE` / `DELETE_AFTER_PROOF`.

**Lot requis** : batch nettoyage dédié après grep import négatif confirmé.

---

## Tableau récapitulatif

| id | verdict | status registre | action | lot requis |
|---|---|---|---|---|
| D01 | FAUX DOUBLON — wrapper compat | CANDIDATE | REGISTER_ONLY | non |
| D02 | FAUX DOUBLON — flux distincts | ACTIVE (×2) | KEEP | non |
| D03 | FAUX DOUBLON — impl vs shell | ACTIVE + CANDIDATE | KEEP + BLOCKED | non |
| D04 | FAUX DOUBLON — entrypoint vs impl | ACTIVE (×2) | KEEP | non |
| D05 | ANOMALIE — scripts différents | DUPLICATE_SUSPECT | BLOCKED_NEEDS_CONSUMER_AUDIT | DEDUP_AUDIT_01 |
| D06 | DELETE_CANDIDATE — .bak commitées | DELETE_CANDIDATE | DELETE_AFTER_PROOF | batch nettoyage |
