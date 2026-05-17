---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01
doc_type: initial_project_doc
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
created_at: 2026-05-17
surface: doc-only
scope: db-layer / LocalCMS observation view spec
---

# 00_INITIAL_PROJECT_DOC
## GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01

---

## 1_MASTER_TARGET

```text
Spécifier l'extension LocalCMS nécessaire pour exposer l'ObservationSummary V1
complet (seuils Phase 1, éligibilité, alertes) sans modifier le runtime en phase
doc-only.
```

---

## 2_CONTEXTE_ETABLI

| Fait | Valeur |
| --- | --- |
| `PR #522` | MERGED — roadmap observation → product |
| `PR #524` | MERGED — ObservationEvent V1 + ObservationSummary établis |
| Décision PR #524 | B — LOCALCMS_OBSERVATION_VIEW |
| Observation Phase 1 | active — 14/30 runs, 2/14 jours |
| LocalCMS source | `modules/localcms/app/main.py` |
| Endpoint actuel | `GET /metrics/daily` → JSON `_build_metrics()` |
| Dashboard actuel | `GET /metrics` → HTML |
| Parent | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` |

---

## 3_INITIAL_NEED

```text
Le schéma ObservationSummary V1 est documenté (PR #524).
LocalCMS expose déjà les métriques de base.
Mais il manque les champs Phase 1 :
  - runs_to_threshold
  - days_to_threshold
  - eligible
  - observation_start
  - days_elapsed
  - closeout_required_count
```

Sans ces champs, l'opérateur ne peut pas lire l'éligibilité directement
depuis LocalCMS. Il doit calculer manuellement depuis les totaux.

---

## 4_SCOPE

Ce child GO est **doc-only**.

| Axe | Objet |
| --- | --- |
| A — État actuel | Ce que `_build_metrics()` retourne aujourd'hui |
| B — Vue cible | Ce que `ObservationSummary` V1 nécessite de plus |
| C — Mapping champs | Champ par champ — source → transformation → output |
| D — Gaps et options | Options pour combler le gap (extension, endpoint dédié) |
| E — Décision | Recommandation pour le GO d'implémentation suivant |

---

## 5_CONTRAINTES

- Doc-only
- Aucune modification de `modules/localcms/app/main.py`
- Aucun runtime
- Aucun SSH réel
- Aucun trade
- Ne pas modifier `GO_INDEX.md`
- Ne pas modifier `ACTIVE_STREAMS.md`

---

## 6_FICHIERS

| Fichier | Contenu |
| --- | --- |
| `00_INITIAL_PROJECT_DOC.md` | Ce document |
| `10_LOCALCMS_CURRENT_EXPOSURE.md` | Ce que `_build_metrics()` retourne aujourd'hui (source prouvée) |
| `20_OBSERVATION_VIEW_SPEC.md` | Spec de la vue cible — champs requis, format, comportement |
| `30_FIELD_MAPPING_OBSERVATION_EVENT_SUMMARY.md` | Mapping champ par champ source → output |
| `40_GAPS_AND_IMPLEMENTATION_OPTIONS.md` | Gaps identifiés et options d'implémentation |
| `90_CLOSEOUT.md` | Closeout draft — décision pour le GO suivant |
