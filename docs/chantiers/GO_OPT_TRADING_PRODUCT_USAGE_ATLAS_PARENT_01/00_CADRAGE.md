---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01_CADRAGE
doc_type: cadrage
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_MANUAL_UI_COMPLETION_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md
  - docs/chantiers/GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
---

# 00_CADRAGE - GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01

## 1_MASTER_TARGET

Creer une couche canonique durable dans le repo pour presenter le projet, distinguer les produits reellement utilisables, et fournir des guides d'usage sans confondre PASS technique et produit fini.

## 2_INITIAL_PROJECT_DOC

Source de depart : bundle valide `product_usage_atlas_ide_bundle_v1_1.zip`.

Ce parent transforme le bundle en couche repo-first durable :

```text
Project Presentation
+ Product Usage Atlas
+ User Guides
```

## 3_INITIAL_NEED

Le besoin n'est plus seulement de dire qu'un chantier est PASS.

Le besoin est de dire, pour chaque surface importante :
- ce qu'elle est ;
- a quoi elle sert dans le setup ;
- si elle est finie ;
- si elle est utilisable maintenant ;
- si elle n'est utilisable qu'avec limites ;
- si elle est seulement documentee ;
- si elle est interdite en live ;
- quel gap reste a fermer ;
- quel NEXT_GO ouvre la suite.

## 4_MASTER_PROJECT_PLAN

Architecture cible de lecture :

```text
Repo opt-trading = source canonique
    -> docs, commits, PR, closeouts, index
    -> PROJECT_PRESENTATION.md
    -> PRODUCT_USAGE_ATLAS.md
    -> PRODUCT_USAGE_MATRIX.md
    -> FINAL_TARGET_GAPS.md
    -> guides utilisateurs bornes

Les apps externes peuvent afficher ou consommer ces etats.
Elles ne deviennent jamais source souveraine.
```

## 6_FINAL_TARGET

Livrer une couche doc-only stable :

```text
Project Presentation + Product Usage Atlas + User Guides
```

## 7_CANONICAL_STATE

| Surface | Etat actuel | Utilisable maintenant | Gap principal | NEXT_GO |
| --- | --- | --- | --- | --- |
| ClickUp Cockpit | `USABLE_LIMITED` | Oui | Limites plan gratuit sur statuses, dashboards et template | Ouvrir un child dedie seulement si upgrade plan ou besoin reel |
| Repo KG | `USABLE_NOW` | Oui | Ajouter une vue produit / usage reel au-dessus du bundle | `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01` |
| Airtable Orchestration Layer | `DOC_ONLY_READY / GO_LIMITED` | Non runtime | Creer le bridge repo `modules/airtable_bridge/` et finaliser les tables produit | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` |
| Botpress Adapter | `SIMULATED_PASS` | Test seulement | Telegram reel, webhook reel, credentials et smoke controle | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` |
| OpenClaw Docs Library | `DOC_ONLY_READY` | Lecture oui | Raffiner la cartographie puis produire une synthese unifiee | `GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01` |
| BTC COIN-M Accumulation Engine | `NOT_USABLE_YET / DO_NOT_USE_LIVE` | Non | Valider le cadre mathematique avant tout backtest, worker ou runtime | Validation utilisateur du parent puis child formules dedie |

## 8_VALIDATED_PLAN

Plan valide pour ce parent :
1. Creer le dossier chantier Product Usage Atlas.
2. Integrer la taxonomie de statuts produit.
3. Creer la couche `docs/product/`.
4. Suivre explicitement ClickUp, Repo KG, Airtable et Botpress.
5. Ajouter des guides seulement pour les surfaces deja utilisables ou lisibles sans risque live.
6. Ne toucher ni runtime, ni secrets, ni execution trading reelle.

## 11_KEY_DECISIONS

- Le repo reste la preuve canonique.
- Un `PASS` technique ne veut pas dire `PRODUCT_FINISHED`.
- Le Product Usage Atlas est une synthese utilisateur, pas une nouvelle source souveraine.
- Airtable, ClickUp et Botpress restent des couches d'usage, pas des couches de preuve.
- Aucun guide live ne sera ecrit pour un produit non valide.
- BTC COIN-M reste explicitement hors usage live.

## 12_INVARIANTS

- Doc-only uniquement.
- Aucun runtime trading modifie.
- Aucun secret expose.
- Aucun push automatique depuis une app externe.
- Aucun produit non valide ne doit etre presente comme fini.
- Tout gap doit pointer vers un NEXT_GO ou une condition d'ouverture explicite.
- Toute promotion de statut doit etre prouvee par une source repo.

## 16_TODO

1. Materialiser le parent Product Usage Atlas.
2. Creer `docs/product/*`.
3. Integrer `10_TRACKING_APPS_CORE_TABLE.md`.
4. Ajouter les guides ClickUp, Repo KG, Botpress simule et OpenClaw docs.
5. Verifier que le lot reste strictement doc-only.

## 17_RESUME_POINT

Reprendre depuis :

```text
docs/product/PRODUCT_USAGE_MATRIX.md
```

Puis maintenir :

```text
docs/product/PRODUCT_USAGE_ATLAS.md
docs/product/FINAL_TARGET_GAPS.md
docs/product/UPDATE_PROTOCOL.md
```
