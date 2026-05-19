---
go_id: GO_OPT_TRADING_GOVERNANCE_PARENT_MASTER_TARGET_CONTINUITY_01
doc_type: master_target_registry
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-19
---

# PRODUCT_FINAL_TARGET_REGISTRY_01

## Objectif

Lister tous les **master targets** (finalités produit ultimes) du projet opt-trading.
Chaque master target est un objectif de niveau supérieur qui peut être poursuivi
par plusieurs GOs successifs. La continuité est assurée par le champ
`master_target_id` dans chaque GO.

## Registry

| # | master_target_id | description | status | first_go | current_go |
|---|---|---|---|---|---|
| 1 | `MT_SIGNAL_CHAIN_PRODUCT` | Signal chain fiable et industrialisée | ACTIVE | `GO_SIGNAL_CHAIN_PRODUCT_ROOT_01` | `GO_OPT_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_BUNDLE_20260519` |
| 2 | `MT_STRICT_WORKERS_RUNNER` | Worker strict automatisé avec orchestration contrôlée | ACTIVE | `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | `GO_OPT_TRADING_STRICT_WORKERS_CHILD_EXTERNAL_APPS_ORCHESTRATION_RUNNER_01` |
| 3 | `MT_DCA_ON_FEAR` | Accumulation d'actions solides pendant les phases de peur | ACTIVE | `GO_OPT_TRADING_STOCKS_PARENT_DCA_ON_FEAR_SOLID_STOCKS_01` | `GO_OPT_TRADING_STOCKS_PARENT_DCA_ON_FEAR_SOLID_STOCKS_01` |
| 4 | `MT_STRATEGY_FRAMEWORK` | Cadre canonique des stratégies de trading | ACTIVE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| 5 | `MT_DESKPRO_UI` | Interface de pilotage desk pro | ACTIVE | `GO_DESKPRO_UI_ROOT_01` | `GO_OPT_TRADING_DESKPRO_UI_STATE_BADGES_HARDENING_01` |
| 6 | `MT_PRODUCT_GOVERNANCE` | Gouvernance produit, continuité et documentation | ACTIVE | `GO_PRODUCT_GOVERNANCE_ROOT_01` | `GO_OPT_TRADING_GOVERNANCE_PARENT_MASTER_TARGET_CONTINUITY_01` |

## Règles

- Un `master_target_id` est créé lors du premier GO qui l'initie.
- Tout GO qui contribue à ce target porte le `master_target_id` dans son frontmatter.
- Quand un GO est mergé, le `current_go` du registre est mis à jour.
- Un target est `RETIRED` quand plus aucun GO actif ne le poursuit.
