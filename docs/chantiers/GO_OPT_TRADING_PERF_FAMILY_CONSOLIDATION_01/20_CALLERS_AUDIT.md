---
doc_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01_CALLERS_AUDIT
doc_type: callers_audit
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - perf
  - callers
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/10_FAMILY_INVENTORY.md
---

# 20_CALLERS_AUDIT

## 1. Callers de `perf`

### Directs non-documentaires constates

| Caller | Type | Preuve | Lecture |
| --- | --- | --- | --- |
| `scripts/deskpro_api_daemon.sh` | launcher runtime | `uvicorn modules.perf.app:app` | point d'entree FastAPI canonique reel |
| `scripts/desk_pro_ui_toolbox_final_cmd.sh` | launcher/runtime ops | restart sur `modules.perf.app:app` | caller ops actif |
| `scripts/desk_pro_ui_toolbox_fix_cmd.sh` | launcher/runtime ops | restart sur `modules.perf.app:app` | caller ops actif |
| `modules/simex_bitget_bridge/cmd.sh` | launcher runtime | demarre `modules.perf.app:app` | dependance operative |
| `scripts/verify_all.sh` | verification | `py_compile modules/perf/app.py` et `modules/perf/engine/app/perf_engine.py` | chemin canonique surveille |
| `modules/desk_pro_orchestrator/app/desk_pro_orchestrator.py` | caller metier | registre `perf_engine -> modules.perf.engine.app.perf_engine` | le chemin canonique du moteur passe par `perf` |

### Conclusion

`perf` est reellement consomme aujourd'hui comme facade canonique et surface runtime utile.

## 2. Callers de `perf_engine`

### Directs non-documentaires constates

| Caller | Type | Preuve | Lecture |
| --- | --- | --- | --- |
| `modules/perf/engine/app/perf_engine.py` | shim Python | importe `modules.perf_engine.app.perf_engine` | `perf_engine` reste la source logique reellement executee |
| `modules/perf_engine/scripts/cmd.sh` | wrapper module | lance `python3 -m modules.perf_engine.app.perf_engine` | wrapper historique encore actif |
| `modules/perf_engine/scripts/sanity_check.sh` | sanity module | execute encore le chemin historique | compat active |
| `tests/e2e/test_perf_engine_strategy_score.py` | test e2e | reference `modules.perf_engine.app.perf_engine` | preuve de conso test/repo |

### Directs documentaires a valeur canonique

| Caller | Type | Lecture |
| --- | --- | --- |
| `registry/modules_registry.yaml` | registry | seul module de la famille encore indexe |
| `docs/index/inbox/GO_PERF_ENGINE_STRATEGY_SCORE_01.md` | chantier | confirme lecture recente de `modules/perf_engine/app/perf_engine.py` |

### Conclusion

`perf_engine` reste fortement consomme, mais surtout comme noyau historique conserve derriere la nouvelle facade `perf`.

## 3. Reponse callers

1. Les callers runtime actifs de la famille pointent majoritairement vers `modules.perf.app:app` et `modules.perf.engine.app.perf_engine`.
2. Les callers qui pointent encore explicitement vers `modules.perf_engine.app.perf_engine` sont surtout le wrapper historique, les sanity checks et certains tests.
3. Le registre canonique actuel est en retard sur l'etat reel de la famille, puisqu'il ne porte que `perf_engine`.
