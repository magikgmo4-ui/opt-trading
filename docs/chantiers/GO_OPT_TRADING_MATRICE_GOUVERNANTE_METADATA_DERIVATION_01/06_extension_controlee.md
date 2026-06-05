---
doc_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01_EXTENSION_CONTROLEE
doc_type: chantier_extension
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
status: open
lifecycle_stage: extension
topic_keys:
  - opt-trading
  - matrice_gouvernante
  - metadata
  - search_tags
  - registry_derived
  - controlled_extension
surface: chantier
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/04_ajustement_doctrinal.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/05_mini_rerun_pilote.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/06_registry_derived_pilot.yaml
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
---

# 06_extension_controlee

## Lot d'extension retenu

Lot borne et non souverain applique reellement sur 3 documents seulement :
- `docs/index/GO_INDEX.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`

Ce lot n'ouvre :
- ni campagne large
- ni tagging massif
- ni synchronisation documentaire reelle

---

## Document 1 - `docs/index/GO_INDEX.md`

- objet canonique principal : `go_index_truth_list`
- frontmatter derive applique :
  - `search_tags`
  - `reference_canonique_principale`
  - `point_de_reprise`
- `search_tags` retenus :
  - `surface:continuite`
  - `doc_role:index`
  - `closeout:reference`
- groupe d'objets : `continuity_indexes`
- ligne de registre derive : see `06_registry_derived_pilot.yaml`
- check de non-regression :
  - `GO_INDEX.md` reste la verite de liste
  - aucune requalification du `doc_type` source dans le document
  - aucune concurrence avec la matrice

## Document 2 - `docs/index/NEXT_GO_CANDIDATES.md`

- objet canonique principal : `next_go_parent_matrix`
- frontmatter derive applique :
  - `search_tags`
  - `reference_canonique_principale`
  - `point_de_reprise`
- `search_tags` retenus :
  - `surface:chantier`
  - `doc_role:index`
  - `flow:next_surface`
  - `closeout:reference`
- groupe d'objets : `continuity_indexes`
- ligne de registre derive : see `06_registry_derived_pilot.yaml`
- check de non-regression :
  - `GO_INDEX.md` garde la priorite de liste et de cardinalite
  - le document reste une matrice de navigation operatoire derivee
  - aucune elevation de `REPRISE.md`

## Document 3 - `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`

- objet canonique principal : `product_continuity_hierarchy`
- frontmatter derive applique :
  - noyau minimal strict
  - `search_tags`
  - `reference_canonique_principale`
  - `intention_produit`
  - `produit_final_voulu`
  - `point_de_reprise`
- `search_tags` retenus :
  - `surface:governance`
  - `surface:continuite`
  - `doc_role:regle_stable`
- groupe d'objets : `product_continuity`
- ligne de registre derive : see `06_registry_derived_pilot.yaml`
- check de non-regression :
  - aucune reduction a un produit unique
  - aucun champ parent, sous-GO ou Git ajoute
  - aucune modification de `MATRICE_GOUVERNANTE_V2.md`

---

## Mini registre derive pilote reel

Fichier produit :
- `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/06_registry_derived_pilot.yaml`

Statut :
- registre derive
- non souverain
- scope controle
- strictement subordonne aux documents sources et a `GO_INDEX.md`

---

## ETABLI

- l'extension tient reellement sur un sous-ensemble borne de 3 documents
- les enrichissements appliques restent petits, prouvables et compatibles avec la doctrine
- `GO_INDEX.md` reste intact dans son role canonique de verite de liste
- `NEXT_GO_CANDIDATES.md` peut porter des derives reels sans remonter au niveau de la liste canonique
- `PRODUCT_CONTINUITY_HIERARCHY_01.md` entre dans le lot sans inflation, grace au noyau frontmatter minimal strict
- le registre derive pilote est exploitable sans concurrencer les sources

## A_SURVEILLER

- la cardinalite et les compteurs globaux de `NEXT_GO_CANDIDATES.md` ne doivent jamais etre relus comme source canonique
- le vocabulaire de `doc_type_fonctionnel` et `authority_level` doit rester tres petit si l'extension continue
- les `search_tags` doivent rester des facettes courtes et stables, pas un substitut au frontmatter

## LIMITES

- le present lot ne corrige aucune desynchronisation documentaire reelle
- il ne couvre ni `REPRISE.md`, ni `BRANCH_STATE.md`, ni les autres surfaces du repo
- il ne lance aucune campagne large de derivation
- le registre derive produit reste un pilote local au GO courant

## VERDICT_EXTENSION

`PASS_EXTENSION_CONTROLEE_A_SURVEILLER`

Motif :
- l'application reelle fonctionne sur le lot borne
- aucune regression canonique n'apparait
- quelques garde-fous doivent rester explicites avant toute extension supplementaire

## POINT_DE_REPRISE

Si une suite est ouverte :
- rester dans ce GO
- etendre a un autre sous-ensemble borne de documents deja stabilises doctrinalement
- conserver un registre derive non souverain par petits lots
- ne pas ouvrir de synchronisation documentaire reelle sans lot distinct

## RISKS

- À qualifier.
