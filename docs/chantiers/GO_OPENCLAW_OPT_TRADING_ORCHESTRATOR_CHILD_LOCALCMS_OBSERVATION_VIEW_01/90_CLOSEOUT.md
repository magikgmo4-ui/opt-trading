---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01
doc_type: closeout
repo: opt-trading
status: draft
created_at: 2026-05-17
verdict: DRAFT — à valider après lecture opérateur
---

# 90_CLOSEOUT

---

## Statut

```text
DRAFT — child GO documenté, pas encore fermé.
```

---

## Objectif atteint

```text
Spécifier l'extension LocalCMS pour exposer ObservationSummary V1 complet.
Identifier les gaps précis dans _build_metrics() et le dashboard HTML.
Proposer le mapping champ par champ pour le GO d'implémentation suivant.
```

---

## Livrables produits

| Fichier | Contenu | Statut |
| --- | --- | --- |
| `00_INITIAL_PROJECT_DOC.md` | Cadrage et contexte | DONE |
| `10_LOCALCMS_CURRENT_EXPOSURE.md` | État réel `_build_metrics()` prouvé dans source | DONE |
| `20_OBSERVATION_VIEW_SPEC.md` | JSON cible + HTML cible — spec complète | DONE |
| `30_FIELD_MAPPING_OBSERVATION_EVENT_SUMMARY.md` | Pseudocode de chaque calcul ajouté | DONE |
| `40_GAPS_AND_IMPLEMENTATION_OPTIONS.md` | 3 gaps, 3 options, scope GO impl | DONE |
| `90_CLOSEOUT.md` | Ce document | DRAFT |

---

## Décisions documentées

| Décision | Valeur |
| --- | --- |
| Option retenue | A — extension `_build_metrics()` (minimal, rétrocompatible) |
| Option souhaitable | C — extension dashboard HTML (progressions Phase 1) |
| Endpoint dédié | non retenu |
| Scope impl GO | `_build_metrics()` + `last_run` + HTML optionnel |
| Timing implémentation | maintenant recommandé (pas après seuil) |

---

## GO suivant recommandé

```text
GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_IMPL_01
```

Scope :
- Modifier `_build_metrics()` — bloc `observation` + extensions `last_run`
- Étendre `_metrics_html()` — progressions Phase 1 + alerte closeout
- Test : `curl localhost:8700/metrics/daily` + `/metrics` HTML

---

## Invariants post-closeout

- Aucune modification de `modules/localcms/app/main.py` dans ce child GO (doc-only)
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` reste l'ancre
- Phase 1 observation continue sans dépendance à cette extension

---

## Verdict

```text
À compléter par l'opérateur :
[ ] PASS — spec validée, child GO peut être fermé
[ ] HOLD — attendre validation
[ ] AMEND — corrections requises
```
