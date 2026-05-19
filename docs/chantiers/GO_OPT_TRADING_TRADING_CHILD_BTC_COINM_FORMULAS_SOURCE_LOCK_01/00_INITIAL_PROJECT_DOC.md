---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01
status: draft_for_user_validation
lifecycle_stage: child_opening_plan
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01
topic_keys:
  - opt-trading
  - trading
  - bitcoin
  - btc
  - bitget
  - coin-futures
  - formulas
  - source-lock
  - unknown-resolution
  - contract-spec
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Lever les UNKNOWN de formules Bitget par sources documentaires et calculs papier, pour débloquer BACKTEST_DATA_PREP."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/02_professional_variable_impact_review.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/04_math_formulas.md
---

# GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01

## 1_MASTER_TARGET

Lever les `UNKNOWN` bloquants identifiés dans `FORMULAS_COMPAT_REVIEW` (#239 merged PASS) pour débloquer `BACKTEST_DATA_PREP_01`.

Objectif strict :

```text
Figer chaque formule par une source documentaire Bitget vérifiable
ou par un calcul papier démontrable, sans implémentation runtime.
```

## 2_INITIAL_PROJECT_DOC

Ce document est le transporteur initial validé pour ouvrir le child de verrouillage des formules.

Règle : aucun sous-chantier opérationnel, aucun worker, aucun backtest, aucune connexion exchange et aucune UI nouvelle ne sont autorisés avant validation explicite de ce document.

## 3_INITIAL_NEED

Problème :

```text
PR #239 (FORMULAS_COMPAT_REVIEW) = MERGED PASS
BACKTEST_DATA_PREP = encore bloqué
Cause = 8 UNKNOWN sur les formules Bitget, 3 PARTIAL sur les signes
```

Besoin immédiat :

```text
Ouvrir un child intermédiaire FORMULAS_SOURCE_LOCK_01
pour lever documentairement chaque UNKNOWN par source Bitget / calcul papier.
```

Objectif :

```text
- réduire la liste UNKNOWN à zéro ;
- figer chaque formule par une référence source vérifiable ;
- ne rien implémenter ;
- ne rien backtester ;
- ne pas connecter d'exchange ;
- autoriser BACKTEST_DATA_PREP seulement après PASS complet du child.
```

## 4_MASTER_PROJECT_PLAN

1. Relire les documents parent `FORMULAS_COMPAT_REVIEW_01` (00/01/02) et grand-parent `ACCUMULATION_ENGINE_01` (01/02/03/04).
2. Consolider la liste exacte des UNKNOWN et PARTIAL.
3. Pour chaque UNKNOWN, rechercher la source Bitget (doc officielle, API response snapshot, whitepaper).
4. Forger le calcul papier quand une source API n'est pas accessible.
5. Documenter chaque formule avec son contrat d'entrée/sortie.
6. Produire des test vectors papier de cohérence.
7. Statuer chaque formule : `LOCKED` / `SOURCE_VERIFIED` / `PAPER_LOCKED`.
8. Produire verdict final : `PASS` si tous les UNKNOWN sont levés.
9. Autoriser alors `BACKTEST_DATA_PREP_01`.

## 6_FINAL_TARGET

Ce child doit produire :

```text
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/01_formulas_source_lock.md
```

Contenu attendu :

```text
1. Table des UNKNOWN hérités de FORMULAS_COMPAT_REVIEW avec leur statut actuel.
2. Pour chaque formule :
   a. Source documentaire Bitget ou calcul papier démontré.
   b. Formule exacte figée.
   c. Convention de signe explicite.
   d. Mapping prix (mark/index/last/execution) pour cette formule.
   e. Contrat d'entrée/sortie JSON.
   f. Test vector papier.
   g. Statut final (LOCKED / SOURCE_VERIFIED / PAPER_LOCKED).
3. Table de résolution complète des UNKNOWN.
4. Verdict : PASS ou PATCH_REQUIRED.
5. Si PASS : autorisation explicite de BACKTEST_DATA_PREP_01.
```

## 8_VALIDATED_PLAN — Séquence

```text
1. Valider le présent 00_INITIAL_PROJECT_DOC.md.
2. Créer 01_formulas_source_lock.md.
3. Y figer les 6 groupes de formules.
4. Produire verdict.
5. Si PASS → BACKTEST_DATA_PREP_01 débloqué.
6. Si PATCH_REQUIRED → corriger et re-soumettre.
```

## 12_INVARIANTS

```text
- aucune connexion exchange
- aucune exécution live
- aucun backtest réel
- aucun worker runtime
- aucune nouvelle UI
- aucune implémentation de code
- documentation et contrats uniquement
- les formules doivent être vérifiables par une source Bitget ou un calcul papier démontrable
- les 6 groupes sont : qty/notional, PnL inverse short, funding signed, liquidation/maintenance, usage des prix, risk tier
- BACKTEST_DATA_PREP reste bloqué tant que ce child n'est pas PASS
- les blocages account-level et execution-level hérités de 02_professional_variable_impact_review restent actifs
```

## 10_SELECTED_SETUP — Sources à exploiter

| Groupe de formules | Source primaire | Source secondaire |
|---|---|---|
| qty_to_notional_fn / notional_to_qty_fn | Bitget API contract spec (`contractSize`, `sizeMultiplier`, `minTradeNum`, `volumePlace`) | Calcul papier inverse contract mapping |
| PnL inverse short | Formule générique inverse COIN-M | Vérification cohérence avec test vectors papier |
| Funding signed formula | Bitget funding rate doc + convention longs-pay-shorts | Test vector par signe de fundingRate |
| Liquidation / maintenance cross margin | Bitget liquidation doc cross margin | Modèle conservatif papier avec risk tiers |
| Mark / index / last / execution price usage | Bitget price indices doc | Mapping explicite à chaque fonction |
| Risk tier / maintenance margin rate | Bitget risk tier table BTCUSD | Extrapolation linéaire papier entre paliers |

## 15_REMAINING_GAP

```text
- accès direct à la doc Bitget officielle (PDF, help center, API spec)
- snapshot API réel du contract spec (contractSize, maintenance margin tiers)
- historique funding pour corrélation (pas nécessaire dans ce child)
- ces gaps doivent être contournés par calcul papier vérifiable
```

## 16_TODO

```text
1. Commit + push du présent document.
2. Validation utilisateur.
3. Créer 01_formulas_source_lock.md avec les 6 groupes figés.
4. Après PASS du child complet, ouvrir BACKTEST_DATA_PREP_01.
```

## GAP_INDEXATION

Ce lot ouvre un child documentaire sur branche dédiée. Les index globaux (`GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE`, `BRANCH_STATE`) ne sont pas modifiés dans ce commit initial.

Trace canonique de reprise :

```text
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/00_INITIAL_PROJECT_DOC.md
```

## 17_RESUME_POINT

```text
PR #239 mergée : FORMULAS_COMPAT_REVIEW = PASS.
BACKTEST_DATA_PREP encore bloqué par les UNKNOWN de formules.
Child FORMULAS_SOURCE_LOCK_01 ouvert pour lever chaque UNKNOWN.
Portée : documentation + contrats + calculs papier uniquement.
Prochaine action : validation utilisateur, puis création 01_formulas_source_lock.md.
BACKTEST_DATA_PREP_01 ne sera ouvert qu'après PASS de ce child.
```
