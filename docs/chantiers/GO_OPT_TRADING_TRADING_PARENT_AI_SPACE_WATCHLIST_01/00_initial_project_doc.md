---
doc_id: GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: market_watchlist
go_id: GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01
status: active
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - trading
  - ai
  - spatial
  - defense
  - stocks
  - watchlist
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01/00_initial_project_doc.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01/20_resume_point.md
updated_at: 2026-05-09
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/inbox/GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01/10_parent_plan.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01/BRANCH_STATE.md
---

# GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01 — Initial Project Doc

## 1_MASTER_TARGET

Construire une documentation canonique de recherche et de suivi pour les actions exposees aux themes :

- intelligence artificielle ;
- infrastructure IA ;
- spatial ;
- defense spatiale ;
- croisement IA + defense + spatial.

La finalite n'est pas de produire un signal d'achat automatique, mais de creer une base de travail structurée pour analyser, comparer, prioriser et suivre les titres.

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche de reference initiale du chantier parent. Il fige le plan initial approuve par l'utilisateur avant elaboration detaillee.

## 3_INITIAL_NEED

L'utilisateur a demande d'approfondir les actions deja sorties dans les recherches precedentes et d'identifier les titres qui profitent ou pourraient profiter des deux themes : IA et spatial.

Liste initiale approuvee :

### Coeur IA

- NVDA
- AMD
- AVGO
- TSM
- MU

### Infrastructure IA

- VRT
- ETN
- GEV
- PWR
- IREN

### Spatial pur

- RKLB
- ASTS
- PL
- LUNR

### Defense / spatial institutionnel

- LMT
- NOC
- LHX
- RTX

### Pont IA + defense + spatial

- PLTR
- RKLB
- NOC
- LHX

### Titres a ajouter a la watchlist

IA / semi / infrastructure :

- MRVL
- ARM
- ANET
- SMCI
- DELL
- HPE
- CEG
- VST
- APLD
- IREN

Spatial / satellite / defense :

- RKLB
- ASTS
- PL
- LUNR
- BKSY
- MDA.TO
- LHX
- NOC
- LMT
- AVAV

## 4_MASTER_PROJECT_PLAN

Plan valide :

1. Classer les titres par theme et par role economique reel.
2. Distinguer les leaders etablis, les beneficiaires indirects et les dossiers speculatifs.
3. Creer une watchlist priorisee.
4. Documenter les catalyseurs, les risques et les invalidations.
5. Construire ensuite une grille d'analyse comparable : prix actuel, market cap, revenus, croissance, marges, P/E ou absence de profit, dette, backlog, guidance, contrats defense, exposition IA/spatial.
6. Separer les paniers :
   - IA solide ;
   - IA infrastructure ;
   - spatial explosif ;
   - defense stable ;
   - pont IA + defense + spatial.
7. Elaborer ensuite une methode de suivi : earnings, guidance, contrats, backlog, annonces Neutron/RKLB, HBM/MU, data centers/VRT-ETN-GEV-PWR, gouvernement/PLTR, satellite-to-phone/ASTS.

## 5_GO_PLAN

Workstreams derives :

- GO_CHILD_RESEARCH_DATASET_01 : creer le dataset initial des tickers et metriques.
- GO_CHILD_CLASSIFICATION_MATRIX_01 : classer par theme, role, risque, horizon et catalyseur.
- GO_CHILD_SCORING_MODEL_01 : definir un score watchlist non automatique.
- GO_CHILD_DASHBOARD_OR_EXPORT_01 : preparer un export lisible, eventuellement CSV/Sheets plus tard si demande explicite.

## 6_FINAL_TARGET

Livrable vise : une documentation parent complete permettant de reprendre l'analyse IA + spatial sans dependance a la conversation initiale.

Le chantier doit rester documentaire et analytique pour l'instant. Aucun ordre, aucune execution trading, aucun runtime opt-trading ne doit etre modifie.

## 12_INVARIANTS

- Pas de conseil financier personnalise.
- Pas de signal automatique d'achat/vente.
- Pas de modification runtime.
- Pas d'integration broker.
- Pas de Google Drive sans demande explicite ou implicite.
- Les donnees de prix, earnings, guidance et contrats doivent etre reverifiees au moment des analyses futures.

## 17_RESUME_POINT

Reprendre depuis `10_parent_plan.md`, puis ouvrir le premier child documentaire : `GO_CHILD_RESEARCH_DATASET_01`.
