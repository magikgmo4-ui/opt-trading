---
doc_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01
status: pass
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - governance
  - matrice_gouvernante
  - canonization
  - doc_only
surface: chantier
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/index/GO_CLOSED_INDEX.md
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
  - matrice_gouvernante_bundle_v1/matrice_gouvernante_bundle_v1/12_BUNDLE_CLOSEOUT_MODELE.md
---

# 00_cadrage — GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01

## Objet

Ouvrir un GO doc-only borne pour promouvoir la matrice gouvernante V2 redigee hors bundle vers sa surface canonique du repo, sans rouvrir les passes du bundle clos.

---

## Besoin initial

Sortir la matrice gouvernante V2 du bundle clos `matrice_gouvernante_bundle_v1` afin de :
- l'ancrer dans `docs/governance/`
- conserver `GO_INDEX.md` comme verite de liste
- conserver `REPRISE.md` comme surface operatoire seulement
- conserver `BRANCH_STATE.md` limite a la surface branches
- ne pas relancer le chantier metadata / tags / recherche

---

## Intention

Canoniser la matrice V2 dans le repo par un lot doc-only minimal, transmissible, et referme dans le meme passage.

---

## Produits finaux voulus / objectifs du chantier

- une surface canonique `docs/governance/MATRICE_GOUVERNANTE_V2.md`
- les references minimales de gouvernance / index mises a jour
- un mini closeout de canonisation
- aucune reouverture du bundle

---

## Cible finale

Disposer dans le repo d'une matrice gouvernante V2 canonique, lisible sans le bundle, tout en gardant les limites bornees deja retenues.

---

## Plan valide

1. prendre le bundle clos comme source de reference seulement
2. promouvoir la matrice V2 vers `docs/governance/`
3. creer un GO doc-only de canonisation
4. mettre a jour les references minimales d'index / gouvernance
5. produire un mini closeout et sortir le GO en `pass`

---

## ETABLI

- le bundle `matrice_gouvernante_bundle_v1` est clos
- la matrice V2 y a ete redigee
- le verdict bundle retenu est compatible avec une promotion repo canonique
- les limites suivantes restent stables et non bloquees :
  - `GO_INDEX.md` comme verite de liste
  - `REPRISE.md` comme surface operatoire seulement
  - `BRANCH_STATE.md` limite a la surface branches
  - `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` comme limite reportee

---

## Hors-scope

- rouvrir PASS 1 a PASS 6 du bundle
- lancer le chantier metadata / tags / recherche
- corriger les docs sources hors besoin minimal de canonisation
- requalifier les arbitrages du bundle

---

## REPRISE

Point de reprise unique :
- `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01/90_closeout.md`
