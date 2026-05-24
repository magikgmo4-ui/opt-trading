---
doc_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01_RUNTIME_SURFACE_MAP
doc_type: runtime_surface_map
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - perf
  - runtime
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/20_CALLERS_AUDIT.md
---

# 30_RUNTIME_SURFACE_MAP

## Carte runtime observee

```text
launchers ops / runtime
  -> modules.perf.app:app
  -> perf/perf_app.py
  -> /perf/* API
  -> perf/perf.db
  -> /desk mount

desk_pro_orchestrator
  -> modules.perf.engine.app.perf_engine
  -> modules.perf_engine.app.perf_engine
  -> data/perf/*.json
```

## Surfaces par role

| Role | Surface | Lecture |
| --- | --- | --- |
| facade famille FastAPI | `modules/perf/app.py` | chemin canonique actif |
| facade famille moteur | `modules/perf/engine/app/perf_engine.py` | chemin canonique actif |
| moteur logique reel | `modules/perf_engine/app/perf_engine.py` | implementation historique toujours executee |
| facade webhook | `modules/perf/webhook.py` | compatibilite de chemin |
| wrappers operateur | `modules/perf/scripts/*` | expose `menu-perf`, `cmd-perf`, `sanity-perf` |
| wrappers moteur historique | `modules/perf_engine/scripts/*` | expose `cmd.sh` interne du moteur |

## Runtime utile ou non

| Surface | Classement |
| --- | --- |
| `modules/perf/` | runtime utile + compat canonique |
| `modules/perf_engine/` | runtime utile historique |

## Lecture structurante

La famille `perf` a deja subi une consolidation partielle de chemins :

- les launchers se sont majoritairement deplaces vers `modules/perf/*`
- mais l'implementation moteur n'a pas ete physiquement absorbee sous `modules/perf/engine/`

Le resultat est un etat transitoire stable :

- canonicalite d'appel dans `perf`
- implementation moteur reelle dans `perf_engine`
