---
doc_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01_MINI_RERUN_PILOTE
doc_type: chantier_pilote_rerun
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
status: open
lifecycle_stage: pilote
topic_keys:
  - opt-trading
  - matrice_gouvernante
  - metadata
  - search_tags
  - registry_derived
  - mini_rerun
surface: chantier
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/04_ajustement_doctrinal.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
---

# 05_mini_rerun_pilote

## Objet

Rejouer un mini pilote dry-run sur les trois points doctrinalement ajustes afin de verifier si le lot est maintenant pret a une extension controlee.

---

## Document 1 - `docs/index/GO_INDEX.md`

### Objet canonique principal retenu

`go_index_truth_list`

### Statut derivable retenu

- source canonique de liste
- index canonique de liste
- surface souveraine pour la cardinalite et la presence des GO

### Frontmatter enrichi derivable et prouvable

```yaml
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Tableau canonique des chantiers"
```

### Qualification derivee retenue

```yaml
doc_type_source: reprise
doc_type_fonctionnel: canonical_list_index
canonical_object: go_index_truth_list
group_bucket: continuity_indexes
authority_level: index_canonique_de_liste
```

### Check de non-regression

- coherence avec `MATRICE_GOUVERNANTE_V2.md` : oui, priorite conservee comme verite de liste
- coherence avec `GO_INDEX.md` : oui, aucune derivation ne depasse le role etabli par le document
- absence de seconde doctrine par les tags : oui, le role fonctionnel derive reste explicatif seulement
- absence de taxonomie parallele : oui, `canonical_list_index` ne cree pas de nouvelle famille d'objets, il clarifie seulement le role reel

### Statut final pilote

`stable_pour_extension_controlee`

---

## Document 2 - `docs/index/NEXT_GO_CANDIDATES.md`

### Objet canonique principal retenu

`next_go_parent_matrix`

### Statut derivable retenu

- matrice de navigation operatoire
- index secondaire derive
- surface non souveraine

### Frontmatter enrichi derivable et prouvable

```yaml
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Matrice - parent actif -> next GO primaire"
```

### Qualification derivee retenue

```yaml
doc_type_fonctionnel: operational_next_matrix
canonical_object: next_go_parent_matrix
group_bucket: continuity_indexes
authority_level: index_operatoire_derive
```

### Regle d'usage issue de l'ajustement

- le document peut guider la navigation operatoire
- il ne peut jamais fixer seul le nombre de GO non clos
- toute contradiction numerique locale est absorbee comme manque de synchronisation documentaire et non comme fait canonique

### Check de non-regression

- coherence avec `MATRICE_GOUVERNANTE_V2.md` : oui, tant que la surface reste navigationnelle et non souveraine
- coherence avec `GO_INDEX.md` : oui, si `GO_INDEX.md` garde la priorite sur toute liste et toute cardinalite
- absence de seconde doctrine par les tags : oui, aucun tag ne porte une verite structurelle
- absence de taxonomie parallele : oui, la qualification `operational_next_matrix` decrit un usage et non une nouvelle doctrine

### Statut final pilote

`stable_pour_extension_controlee_sous_priorite_go_index`

---

## Document 3 - `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`

### Objet canonique principal retenu

`product_continuity_hierarchy`

### Statut derivable retenu

- regle de continuite produit
- surface canonique de cadrage multi-produits
- document eligible a extension controlee sous condition de noyau minimal

### Frontmatter minimal decide pour une application reelle ulterieure

```yaml
doc_id: OPT_TRADING_PRODUCT_CONTINUITY_HIERARCHY_01
doc_type: product_continuity_hierarchy
status: reference
lifecycle_stage: governance
surface: governance
source_kind: canonical
topic_keys:
  - opt-trading
  - product_continuity
  - hierarchy
```

### Frontmatter enrichi derivable et prouvable

```yaml
reference_canonique_principale: docs/governance/MATRICE_GOUVERNANTE_V2.md
intention_produit: "poser une continuite produit hierarchisee en 3 niveaux"
produit_final_voulu: "preserver la trajectoire produit et le paysage global du projet"
point_de_reprise: "Section 2. Modele de continuite"
```

### Check de non-regression

- coherence avec `MATRICE_GOUVERNANTE_V2.md` : oui, le document reste dans la couche produit au-dessus des GO
- coherence avec `GO_INDEX.md` : oui, il ne concurrence pas la verite de liste
- absence de seconde doctrine par les tags : oui, aucun `product:*` fin n'est requis pour deriver le document
- absence de taxonomie parallele : oui, le document reste multi-produits sans reduction artificielle a un centre unique

### Statut final pilote

`stable_pour_extension_controlee_apres_noyau_minimal`

---

## ETABLI

- le blocage doctrinal sur `NEXT_GO_CANDIDATES.md` est leve en le bornant explicitement comme index secondaire de navigation sous priorite de `GO_INDEX.md`
- le blocage sur `GO_INDEX.md` est leve par la distinction claire entre `doc_type_source` et `doc_type_fonctionnel`
- le blocage sur `PRODUCT_CONTINUITY_HIERARCHY_01.md` est leve par la decision d'un noyau frontmatter minimal strict et non inflationniste
- aucun des trois ajustements n'ouvre une seconde doctrine par les tags
- aucun des trois ajustements ne cree de taxonomie parallele

## A_AJUSTER

- figer une petite convention de vocabulaire pour `doc_type_fonctionnel` et `authority_level` avant toute extension plus large que ce trio
- garder explicite dans tout futur lot la difference entre :
  - correction des sources documentaires
  - qualification derivee dans le dry-run ou le registre non souverain

## RISQUES

- si l'extension oublie la priorite de `GO_INDEX.md`, `NEXT_GO_CANDIDATES.md` pourrait etre relu trop fortement
- si le noyau minimal de `PRODUCT_CONTINUITY_HIERARCHY_01.md` est enrichi trop vite, on peut recreer une taxonomie produit inutilement fine
- si `doc_type_fonctionnel` prolifere sans vocabulaire borne, le registre derive peut devenir flou

## VERDICT_PILOTE

`PASS_PILOTE_EXTENSION_POSSIBLE`

Motif :
- les trois blocages identifies sont maintenant traites au niveau doctrinal
- l'extension peut rester controlee tant qu'elle demeure :
  - bornee
  - subordonnee a `GO_INDEX.md`
  - non souveraine
  - separee de toute synchronisation documentaire reelle

## POINT_DE_REPRISE

Prochain geste exact :
- ouvrir un lot d'extension controlee toujours dans ce GO, sur un petit sous-ensemble borne, en reutilisant les regles d'ajustement ci-dessus
- ne pas lancer de campagne large
- ne pas corriger encore les documents sources hors du strict noyau minimal si une application reelle est explicitement demandee
