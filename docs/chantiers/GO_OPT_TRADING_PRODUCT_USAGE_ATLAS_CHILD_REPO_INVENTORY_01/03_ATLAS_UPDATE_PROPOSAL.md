---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01_ATLAS_UPDATE_PROPOSAL
doc_type: atlas_update_proposal
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/product/PRODUCT_USAGE_GRAPH.mmd
---

# 03_ATLAS_UPDATE_PROPOSAL - Proposition d'ajout a l'Atlas

## Principe

Cette proposition liste les surfaces a ajouter au Product Usage Atlas avec un bucket d'usage et un NEXT_GO.
Elle ne modifie pas les fichiers `docs/product/*` dans ce child. La materialisation des entrees dans l'Atlas est laissee au child `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01` ou a une PR dediee apres validation de cet inventaire.

## Lecture par bucket (apres ajout propose)

### USABLE_NOW (1 surface existante)

| Produit | Usage operateur |
| --- | --- |
| Repo KG | Projection repo-first exploitable maintenant. |

### USABLE_LIMITED (1 existante + 5 nouvelles = 6)

| Produit | Usage operateur | NEXT_GO |
| --- | --- | --- |
| ClickUp Cockpit | Cockpit operateur avec limites plan gratuit. | Besoin reel ou upgrade plan seulement. |
| **Desk Pro** | Stack operationnelle Desk Pro avec runbooks, wrappers, dashboard. Survivant unique non fige. | `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01` |
| **Bot Vision** | Chaine vision transitoire active (`vision_bot` + `bot_vision_step2`). | `VISION_FAMILY_SURVIVOR_DECISION` |
| **TradingView / Telegram Alert Pipeline** | Pipeline d'alertes TradingView actif, alert webhook en continuite. | Poursuite GO alert webhook actif. |
| **OpenClaw Runtime** | Modules runtime installables, gateway, TMUX supervision en cours. | `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` |
| **derivatives_collector** | Collecteur canonique derives, convergence doctrinale en cours. | `GO_COLLECTORS_BASELINE_INVENTORY_01` |

### DOC_ONLY (2 existantes + 2 nouvelles = 4)

| Produit | Usage operateur | NEXT_GO |
| --- | --- | --- |
| Airtable Orchestration Layer | Cadrage et plan documentes, bridge a creer. | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` |
| OpenClaw Docs Library | Cartographie documentaire, pas de runtime. | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` |
| **Trading Dual Stack V1 / XAUUSD** | Framework documente, schemas/config V1 etablis. LAB operationnel mais sans broker reel. | `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` |
| **LocalCMS** | Consumer UI externe, cadrage et plan documentes. Usage reel a prouver. | `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` |

### SIMULATED_ONLY (1 existante)

| Produit | Usage operateur | NEXT_GO |
| --- | --- | --- |
| Botpress Adapter | Simulation et smoke seulement. | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` |

### FORBIDDEN_LIVE (1 existante)

| Produit | Usage operateur | NEXT_GO |
| --- | --- | --- |
| BTC COIN-M Accumulation Engine | Aucun usage live autorise. | Valider le parent puis child formules dedie. |

## Surfaces KEEP_CANDIDATE (non ajoutees a l'Atlas maintenant)

Ces surfaces restent candidates mais ne recoivent pas d'entree Atlas dans ce lot, faute de preuve suffisante ou parce qu'elles meritent un sous-lot dedie.

| Surface | Raison du report |
| --- | --- |
| derivatives_analyzer | Preuve d'usage moins documentee que le collector. |
| probability_engine | Manque closeout ou runbook explicite. |
| risk_engine | Preuve d'usage produit explicite manquante. |
| Deepseek Student | Survivant canonique final non fige. Merite un sous-lot dedie. |
| Collectors spot (CoinGecko, Binance) | Subordonnes a la doctrine famille. |
| Simex Bitget Bridge | Preuve d'usage operateur systematique a confirmer. |
| validated_prompt_factory | Integration incomplete (Registry + Wrapper). |

## Surfaces DO_NOT_PROMOTE / ARCHIVE_ONLY

| Surface | Raison |
| --- | --- |
| Git Fleet Guard | Outillage de support, pas un produit. |
| module_contextuals_shell | Aucun usage produit documente. |
| Ops wrappers / menus / registries | Wrappers generiques internes. |
| Surfaces historiques | Archivees ou gelees explicitement. |

## Impact sur les docs product

Si cette proposition est validee, les fichiers suivants devront etre mis a jour dans un child ou une PR dediee :

- `docs/product/PRODUCT_USAGE_MATRIX.md` : ajouter les 7 entrees ADD_TO_ATLAS, ajouter la section KEEP_CANDIDATE.
- `docs/product/PRODUCT_USAGE_ATLAS.md` : ajouter les descriptions des 7 nouveaux produits avec `usage_view`, `operator_read`, `canonical_sources`, `remaining_gaps`, `next_go`.
- `docs/product/FINAL_TARGET_GAPS.md` : ajouter les gaps des nouveaux produits.
- `docs/product/PRODUCT_USAGE_GRAPH.mmd` : ajouter les noeuds et buckets.

Le present child ne modifie pas ces fichiers. Il pose l'inventaire et la classification.
L'application effective dans l'Atlas releve du child `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USER_GUIDES_01` ou d'un sous-lot dedie.

## RISKS

- À qualifier.
