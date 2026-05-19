---
doc_id: OPT_TRADING_GUIDE_BTC_COINM_DO_NOT_USE_LIVE
doc_type: do_not_use_notice
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
---

# Notice d'interdiction - BTC COIN-M Accumulation Engine

> **INTERDIT LIVE. AUCUN USAGE RUNTIME. AUCUN GUIDE LIVE.**

## Interdiction explicite

Le BTC COIN-M Accumulation Engine est classe `FORBIDDEN_LIVE`. Cela signifie :

- **Aucun usage live** n'est autorise a ce stade.
- **Aucun backtest fiable** n'est disponible.
- **Aucun worker runtime** n'est active.
- **Aucune connexion exchange** n'est autorisee.
- **Aucun trade reel** ne doit etre initie.

## Pourquoi cette interdiction

Le parent est en statut `draft_for_user_validation`. Les prerequis suivants ne sont pas remplis :

- les formules Bitget COIN-FUTURES ne sont pas validees ;
- la compatibilite des formules avec les modules existants n'est pas prouvee ;
- le backtest data prep n'est pas pret ;
- le worker n'est pas implemente ;
- les invariants mathematiques ne sont pas prouves.

## Condition de levee

Cette interdiction ne pourra etre levee que lorsque les etapes suivantes auront ete franchies :

1. Validation utilisateur du parent.
2. Validation des formules Bitget (child formules dedie).
3. Compatibilite prouvee avec l'existant.
4. Backtest data prep valide.
5. Worker implemente et teste en environnement controle.
6. Invariants mathematiques prouves.

## Ce qu'il est autorise de faire

- Lire le cadrage mathematique.
- Consulter les variables, bornes et relations.
- Preparer le terrain documentaire pour la validation future.
- **Rien d'autre.**

## Source canonique

- `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md`
- `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md`
- `docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md`

## NEXT_GO

Valider le parent, puis ouvrir le child formules dedie avant toute suite runtime.
