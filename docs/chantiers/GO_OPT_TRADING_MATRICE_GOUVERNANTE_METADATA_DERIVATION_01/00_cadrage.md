---
doc_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - matrice_gouvernante
  - metadata
  - search_tags
  - registry_derived
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
  - docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md
  - docs/index/GO_INDEX.md
---

# 00_cadrage — GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01

## Objet

Ouvrir un GO doc-only separe, post-publication de `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, dedie a la derivation controlee des metadonnees, tags de recherche, groupes d'objets et registry derive.

---

## Besoin initial

La matrice maitre DOC OPS est maintenant fixee comme doctrine de structure.
`docs/governance/MATRICE_GOUVERNANTE_V2.md` reste une annexe stable secondaire utile au recroisement.
Il faut ouvrir un lot distinct pour definir ce qui peut etre derive de ce cadre, sans :
- modifier la matrice
- rouvrir la synchronisation documentaire reelle
- remonter les tags / metadata au-dessus du noyau canonique

---

## Intention

Definir une doctrine legere, stable et controlee pour les derives documentaires, subordonnee a la matrice maitre DOC OPS, avec V2 conservee comme annexe stable secondaire et sans effet de bord sur la souverainete canonique.

---

## Produits finaux voulus / objectifs du chantier

- une doctrine canonique de derivation legere
- une frontiere claire entre frontmatter enrichi, `search_tags`, groupes d'objets et registry derive
- un lot strictement doc-only
- aucune ouverture du chantier de synchronisation documentaire reelle

---

## Cible finale

Disposer d'une base de doctrine qui permette ensuite de deriver des enrichissements documentaires de maniere controlee, sans concurrencer la matrice ni les surfaces souveraines.

---

## ETAT_DEPART_RETENU

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` est le maitre canonique souverain pour ce lot
- `docs/governance/MATRICE_GOUVERNANTE_V2.md` reste une annexe stable secondaire
- `GO_INDEX.md` reste la verite de liste
- `REPRISE.md` reste operatoire seulement
- `BRANCH_STATE.md` reste limite a la surface branches
- `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` reste hors perimetre du present lot

---

## Hors-scope

- modifier la doctrine de la matrice
- lancer la synchronisation documentaire reelle
- traiter le cas AI team
- requalifier `REPRISE.md` ou `BRANCH_STATE.md`
- ouvrir un chantier d'implementation outillee

---

## REPRISE

Point de reprise local :
- `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`
