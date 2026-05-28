---
doc_id: GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_OPEN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: perf_engine
go_id: GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_OPEN_01
parent_go_id: null
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
PF_ID: PF_PERF_ENGINE_TRADING_LAB
MASTER_PROJECT_PLAN_ID: MPP_PERF_ENGINE_TRADING_LAB
MASTER_TARGET_ID: MT_PERF_ENGINE_TRADING_LAB
PARENT_GO_ID: null
BUNDLE_TARGET: null
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_CHILD_EVENT_TRACKER_01
topic_keys:
  - opt-trading
  - perf_engine
  - trading_lab
  - event_tracker
  - strategy_scoring
  - master_project_plan
links:
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01_MASTER_PROJECT_PLAN_CREATION_RULE_01.md
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_OPEN_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Perf Engine / Trading Lab opérationnel : les events de trading sont trackés,
les performances sont calculées, les stratégies sont scorées, et les résultats
sont exposés via l'API perf.

La règle centrale est :

```text
webhook event -> perf event -> position tracker -> metrics -> API
```

Composants identifiés :
- `perf/perf_app.py` — API FastAPI port 8010, persistance SQLite
- `modules/perf_engine/` — position tracker (candidate → active → closed)
- `adapters/webhook_to_perf.py` — normalisation des events webhook
- `GO_PERF_ENGINE_STRATEGY_SCORE_01` — strategy scoring

## 2_INITIAL_PROJECT_DOC

Ce document ouvre le parent canonique `PF_PERF_ENGINE_TRADING_LAB` pour la première fois.

Il fige la structure de continuité du parent : `1_MASTER_TARGET`, `4_MASTER_PROJECT_PLAN`
et `CLOSE_GATE_MASTER_TARGET` déclarés, rattachement à `PF_PERF_ENGINE_TRADING_LAB`
et `MPP_PERF_ENGINE_TRADING_LAB`.

Il ne ferme pas le parent. Il ne modifie pas les index globaux.

## 3_INITIAL_NEED

`PF_PERF_ENGINE_TRADING_LAB` est référencé dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md`
comme surface finale P1 avec statut "partiellement couvert — parent à ouvrir".

Des composants existent déjà (`perf_app.py`, `modules/perf_engine/`, strategy scoring)
mais aucun parent canonique `GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN` n'a été ouvert.

L'ouverture est nécessaire avant tout child GO d'implémentation afin que les child GOs
puissent être rattachés à un parent canonique réel.

## 4_MASTER_PROJECT_PLAN

`MPP_PERF_ENGINE_TRADING_LAB`

1. **Event tracker** : tracker les events de trading (entry, exit, PnL) dans perf_db.
2. **Position tracker** : gérer le cycle de vie des positions (candidate → active → closed) — base existante dans `modules/perf_engine/`.
3. **Metrics engine** : calculer les métriques de performance (PnL, Sharpe, drawdown, win rate).
4. **Strategy scoring** : scorer les stratégies selon leurs performances — base existante `GO_PERF_ENGINE_STRATEGY_SCORE_01`.
5. **Perf API** : exposer les résultats via l'API perf (port 8010) — base existante `perf/perf_app.py`.
6. **Tests de compatibilité** : valider le tracking et le calcul des métriques par tests smoke.
7. **Documentation reprise** : documenter les gaps, les métriques disponibles, les stratégies scorées.

## 5_GO_PLAN

Chantier parent structurel. Cette ouverture est doc-first : aucun runtime modifié.

Sous-GO proposés (à ouvrir séquentiellement selon priorité opératoire) :

| GO_ID | Cible |
|---|---|
| `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_CHILD_EVENT_TRACKER_01` | Formaliser le tracking des events de trading |
| `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_CHILD_METRICS_ENGINE_01` | Implémenter/migrer le calcul de métriques |
| `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_CHILD_API_EVOLUTION_01` | Faire évoluer l'API perf |

Premier child recommandé : `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_CHILD_EVENT_TRACKER_01`.

## 6_FINAL_TARGET

Livrable de cette ouverture : un parent canonique `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_OPEN_01`
structuré avec `1_MASTER_TARGET`, `4_MASTER_PROJECT_PLAN` et `CLOSE_GATE_MASTER_TARGET`
déclarés, rattaché à `PF_PERF_ENGINE_TRADING_LAB` et `MPP_PERF_ENGINE_TRADING_LAB`,
prêt à recevoir les child GOs d'implémentation.

## 7_CANONICAL_STATE

- `PF_PERF_ENGINE_TRADING_LAB` dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md` comme surface finale P1 "partiellement couvert".
- `perf/perf_app.py` existe comme service FastAPI (port 8010, SQLite).
- `modules/perf_engine/` existe comme tracker de positions intermédiaires.
- `adapters/webhook_to_perf.py` normalise les events webhook vers perf.
- `GO_PERF_ENGINE_STRATEGY_SCORE_01` existe comme chantier strategy scoring.
- Aucun parent canonique n'existait avant cette ouverture.

## 8_VALIDATED_PLAN

Plan validé pour cette ouverture :
- créer uniquement les documents de structure du parent ;
- ne pas modifier le runtime ;
- ne pas écrire dans les index globaux ;
- créer l'entrée inbox locale courte.

## 9_SELECTED_SOLUTION

Perf Engine / Trading Lab est le hub de mesure de performance. Il consomme les events
de trading et produit des métriques et scores. La stack existante (`perf_app.py`,
`modules/perf_engine/`, strategy scoring) est conservée et sera progressivement
encapsulée dans la structure parent/child.

## 10_SELECTED_SETUP

Structure cible :

```text
perf/
  perf_app.py              <- API existante
  perf.db                  <- SQLite (WAL)
modules/perf_engine/
  position_tracker.py      <- cycle de vie des positions
  metrics/
    pnl_calculator.py
    sharpe_calculator.py
    drawdown_analyzer.py
  scoring/
    strategy_scorer.py
  tests/
```

## 11_KEY_DECISIONS

- Le chantier est parent structurel ; aucun runtime modifié à l'ouverture.
- La stack existante est conservée ; les child GOs encapsuleront progressivement.
- Les child GOs d'implémentation seront `GO_CHILD_ATTACHED_TO_PARENT`.
- Pas de fermeture parent avant que `CLOSE_GATE_MASTER_TARGET` soit satisfait.

## 12_INVARIANTS

- Ne pas fermer le parent à l'ouverture.
- `GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN` — permanent.
- Aucun runtime modifié.
- Pas de modification des index globaux.

## 13_ESTABLISHED

- `PF_PERF_ENGINE_TRADING_LAB` identifié comme surface finale P1 dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md`.
- `MPP_PERF_ENGINE_TRADING_LAB` référencé dans `GO_INDEX.md` comme plan maître cible.
- `perf/perf_app.py` opérationnel avec API REST et persistance SQLite.
- `modules/perf_engine/` opérationnel comme position tracker.
- `GO_PERF_ENGINE_STRATEGY_SCORE_01` en cours comme chantier strategy scoring.

## 14_HYPOTHESIS

À valider par les child GOs :
- Le tracking d'events peut être renforcé sans casser l'existant.
- Les métriques de performance (Sharpe, drawdown) peuvent être ajoutées au pipeline existant.
- L'API perf peut évoluer sans breaking change pour les consommateurs existants.

## 15_REMAINING_GAP

- Tracking d'events non formalisé.
- Métriques de performance avancées absentes (Sharpe, drawdown).
- Stratégies scorées mais pas encore intégrées dans un pipeline continu.
- Tests de compatibilité incomplets.

## 16_TODO

1. Ouvrir `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_CHILD_EVENT_TRACKER_01` — formaliser le tracking.
2. Ajouter les métriques avancées (Sharpe, drawdown).
3. Intégrer le strategy scoring dans le pipeline continu.

## 17_RESUME_POINT

Reprendre sur le premier child GO :

```text
GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_CHILD_EVENT_TRACKER_01
```

---

## CLOSE_GATE_MASTER_TARGET

Le parent peut être fermé uniquement si toutes les conditions suivantes sont satisfaites :

```text
1. PF_PERF_ENGINE_TRADING_LAB utilisable :
   - tracking d'events opérationnel
   - métriques de base calculées (PnL, win rate)
   - API perf fonctionnelle

2. Métriques avancées :
   - au moins 2 métriques avancées implémentées (Sharpe, drawdown)

3. Strategy scoring :
   - au moins 1 stratégie scorée et accessible via l'API

4. Tests de compatibilité :
   - tests smoke du pipeline perf passant en local ou CI

5. Documentation reprise :
   - gaps, métriques disponibles et stratégies scorées documentés

6. Aucun gap bloquant non documenté.
```
