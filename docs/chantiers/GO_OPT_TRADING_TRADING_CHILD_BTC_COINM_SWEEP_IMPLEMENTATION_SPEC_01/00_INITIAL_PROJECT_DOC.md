---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01
status: draft_for_user_validation
lifecycle_stage: child_opening_plan
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01
topic_keys:
  - opt-trading
  - trading
  - btc
  - coin-futures
  - sweep-implementation
  - integration
  - trading-lab
  - simulation-engine
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Specifier l'integration du sweep BTC COIN-M dans trading_lab_v1, sans lancer la grande serie de tests."
updated_at: 2026-05-08
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01/01_simulation_engine_contract.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01/02_integration_plan.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/01_param_space_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/02_simulation_result_schema.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/03_reality_classifier_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/04_ranking_method.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01/01_backtest_data_prep.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/01_formulas_source_lock.md
---

# GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01

## 1_MASTER_TARGET

Specifier l'integration du sweep parametrique BTC COIN-M dans `trading_lab_v1` en reutilisant au maximum ses patterns existants, sans lancer de simulation massive, sans nouveau backtest engine, et sans runtime.

## 2_INITIAL_PROJECT_DOC

`PARAM_SWEEP_FREE_SEARCH_01` (PR #299 merged) a fixe les contrats documentaires du free search :
- espace de 24 parametres modifiables
- schema de sortie par run (~40 champs)
- classifieur realite avec 6 classes primaires
- methode de ranking par `delta_btc_net`

Ce child `SWEEP_IMPLEMENTATION_SPEC_01` passe a l'etape suivante : specifier comment implementer le moteur de simulation sans le coder, en restant au niveau des contrats d'interface.

## 3_INITIAL_NEED

L'exploration du code (`trading_lab_v1`, docs de `BACKTEST_DATA_PREP`, `FORMULAS_SOURCE_LOCK`) a revele :

```text
- trading_lab_v1 = lab XAUUSD de feature-engineering (detection FVG/sweep)
- aucun moteur de simulation DCA/short/funding/liquidation n'existe
- le backtest_execution_v1 n'est pas implemente (pas de code)
- les 9 formules PAPER_LOCKED sont documentees avec contrats JSON
- les patterns JSONL, CLI dispatch, et test isolation sont directement reutilisables
```

Il manque un contrat clair sur comment batir le moteur de simulation manquant en l'integrant dans `trading_lab_v1` plutot qu'en creant un module separe.

## 4_MASTER_PROJECT_PLAN

### Phase 1 - Contrat du moteur de simulation

```text
- specifier la boucle principale candle-par-candle
- specifier les fonctions de calcul DCA, short, TP, funding, fees, liquidation
- specifier la machine d'etat interne (reserves, positions, PnL, drawdown)
```

### Phase 2 - Contrat d'integration

```text
- specifier les points d'extension de trading_lab_v1
- specifier les nouveaux modules et fichiers
- specifier les nouvelles commandes CLI
- specifier le plan de tests
```

## 6_FINAL_TARGET

Livrables de ce child :

```text
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01/
  00_INITIAL_PROJECT_DOC.md
  01_simulation_engine_contract.md
  02_integration_plan.md
```

## 12_INVARIANTS

```text
- simulation only
- pas de live
- pas d'ordre reel
- pas de cle API privee
- pas de runtime loop
- pas de nouvelle UI
- pas de nouveau backtest engine independant
- etendre trading_lab_v1, pas le remplacer
- toutes les formules sont PAPER_LOCKED dans l'etat actuel
- pas de simulation massive dans ce child
- pas d'implementation reelle dans ce child (spec uniquement)
```

## 15_REMAINING_GAP

Avant implementation reelle du sweep :

```text
1. Donnees historiques BTC COIN-M a telecharger (1h, 2024-2026)
2. Implementation des 9 formules PAPER_LOCKED en Python
3. Implementation de la boucle de simulation
4. Implementation du generateur de configs
5. Implementation du classifieur realite
6. Implementation du ranker
7. Tests unitaires et smoke
8. Lancement de la premiere campagne de sweep
```

## 16_TODO

```text
1. Relire et valider le present 00_INITIAL_PROJECT_DOC.md.
2. Valider 01_simulation_engine_contract.md.
3. Valider 02_integration_plan.md.
4. Ensuite seulement ouvrir le lot d'implementation reelle.
```

## GAP_INDEXATION

Ce lot ouvre un child de specification sur branche dediee.
Les index globaux ne sont pas modifies dans ce passage.

Trace canonique de reprise :

```text
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01/00_INITIAL_PROJECT_DOC.md
```

## 17_RESUME_POINT

```text
SWEEP_IMPLEMENTATION_SPEC_01 : specifier comment etendre trading_lab_v1
pour integrer le moteur de simulation BTC COIN-M, sans le coder.
Contracts only. Le code vient apres validation de cette spec.
```
