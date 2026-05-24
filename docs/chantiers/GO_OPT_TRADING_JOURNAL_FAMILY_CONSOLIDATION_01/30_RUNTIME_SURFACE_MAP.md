---
doc_id: GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01_RUNTIME_SURFACE_MAP
doc_type: runtime_surface_map
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - journal
  - runtime
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01/20_CALLERS_AUDIT.md
---

# 30_RUNTIME_SURFACE_MAP

## Carte runtime observee

```text
decision/risk/execution/position/perf outputs
  -> journal_engine
  -> journal_engine.json
  -> desk_pro_orchestrator run outputs
  -> shared artifacts copy
```

## Surfaces par role

| Role | Surface | Lecture |
| --- | --- | --- |
| moteur de journalisation | `modules/journal_engine/app/journal_engine.py` | implementation active |
| wrappers operateur module | `modules/journal_engine/scripts/*` | cmd/menu/sanity actifs |
| artefact de sortie | `journal_engine.json` | attendu par les flux Desk Pro |
| surface operateur historique | `modules/journal_de_bord/` | absente du parc courant |

## Runtime utile ou non

| Surface | Classement |
| --- | --- |
| `modules/journal_engine/` | runtime utile |
| `modules/journal_de_bord/` | runtime retire / hors parc courant |

## Lecture structurante

Le runtime journal utile n'est plus partage entre deux modules.

Le parc courant montre :

- un seul moteur present et consomme: `journal_engine`
- une ancienne surface operateur `journal_de_bord` deja retiree

Le probleme de famille n'est donc plus une coexistence vivante.
Le probleme restant est un realignement des preuves documentaires et de la registry sur cet etat.
