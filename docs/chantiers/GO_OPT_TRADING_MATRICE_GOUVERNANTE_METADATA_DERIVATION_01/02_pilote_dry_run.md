---
doc_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01_PILOTE_DRY_RUN
doc_type: chantier_pilote
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
  - dry_run
surface: chantier
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/03_decisions.md
---

# 02_pilote_dry_run

## Objet

Executer un pilote controle de derivation sur un perimetre borne, en dry-run seulement, afin de verifier que :
- un objet canonique principal peut etre attribue a chaque document
- un enrichissement frontmatter prouvable reste possible sans invention
- les `search_tags` restent derives, legers et non souverains
- un groupe d'objets principal suffit
- un registre derive peut etre forme sans taxonomie parallele

---

## Regle de lecture du pilote

- un document = un objet canonique principal
- les champs enrichis proposes n'ont de valeur qu'en presence d'une preuve textuelle ou canonique
- les `search_tags` sont des facettes de recherche et non une seconde doctrine
- le `group_bucket` principal est une vue derivee stable et non une nouvelle structure souveraine
- `GO_INDEX.md` reste la verite de liste

---

## Document 1 - `docs/governance/MATRICE_GOUVERNANTE_V2.md`

### Objet canonique principal

`matrice_gouvernante_v2`

### Frontmatter enrichi derivable et prouvable

```yaml
reference_canonique_principale: docs/governance/MATRICE_GOUVERNANTE_V2.md
point_de_reprise: "Section RESUME_POINT"
```

Justification :
- le document est lui-meme la reference canonique de gouvernance
- le point de reprise est explicitement porte par la section de resume final
- aucun champ parent, sous-GO, produit centre ou support Git supplementaire n'est ajoute car non necessaire ou non prouve a ce niveau

### `search_tags` autorises

- `surface:governance`
- `doc_role:regle_stable`
- `closeout:reference`

### Groupe d'objets principal

`governance_rules`

### Ligne de registre derive d'exemple

```yaml
doc_path: docs/governance/MATRICE_GOUVERNANTE_V2.md
doc_id: OPT_TRADING_MATRICE_GOUVERNANTE_V2
surface: governance
doc_type: governance_matrix
canonical_object: matrice_gouvernante_v2
group_bucket: governance_rules
authority_level: gouvernance_canonique
reference_canonique_principale: docs/governance/MATRICE_GOUVERNANTE_V2.md
topic_keys: [opt-trading, matrice_gouvernante, governance, continuity, git]
search_tags: [surface:governance, doc_role:regle_stable, closeout:reference]
is_derived: true
derived_from: docs/governance/MATRICE_GOUVERNANTE_V2.md
updated_at: 2026-04-22
```

### Check de non-regression

- coherence avec `MATRICE_GOUVERNANTE_V2.md` : oui, objet identique a la surface souveraine
- coherence avec `GO_INDEX.md` : oui, le document reste hors verite de liste mais y est reference comme surface canonique
- absence de seconde doctrine par les tags : oui, les tags ne portent ni parent, ni produit, ni support Git
- absence de taxonomie parallele : oui, `governance_rules` decrit un role documentaire stable deja prevu par la doctrine

---

## Document 2 - `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`

### Objet canonique principal

`metadata_derivation_doctrine`

### Frontmatter enrichi derivable et prouvable

```yaml
reference_canonique_principale: docs/governance/MATRICE_GOUVERNANTE_V2.md
objectif_local_go: "fixer une doctrine legere et controlee de derivation"
cible_locale_go: "frontmatter enrichi, search_tags, groupes d'objets et registre derive non souverain"
point_de_reprise: "Section Perimetre pilote"
```

Justification :
- la subordination a `MATRICE_GOUVERNANTE_V2.md` est explicite
- l'objectif local et la cible locale sont explicites dans l'objet et la doctrine
- aucun parent n'est ajoute car `GO_INDEX.md` ne prouve pas de parent pour ce GO

### `search_tags` autorises

- `surface:governance`
- `doc_role:regle_stable`
- `flow:go_simple`
- `closeout:reference`

### Groupe d'objets principal

`governance_rules`

### Ligne de registre derive d'exemple

```yaml
doc_path: docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
doc_id: OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
surface: governance
doc_type: governance_policy
canonical_object: metadata_derivation_doctrine
group_bucket: governance_rules
authority_level: gouvernance_canonique_subordonnee
reference_canonique_principale: docs/governance/MATRICE_GOUVERNANTE_V2.md
topic_keys: [opt-trading, matrice_gouvernante, metadata, search_tags, registry_derived]
search_tags: [surface:governance, doc_role:regle_stable, flow:go_simple, closeout:reference]
is_derived: true
derived_from: docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
updated_at: 2026-04-22
```

### Check de non-regression

- coherence avec `MATRICE_GOUVERNANTE_V2.md` : oui, la doctrine se declare explicitement posterieure et subordonnee
- coherence avec `GO_INDEX.md` : oui, le GO existe comme GO simple ouvert sans parent prouve
- absence de seconde doctrine par les tags : oui, les tags decrivent une surface et un role, sans remplacer la doctrine
- absence de taxonomie parallele : oui, `metadata_derivation_doctrine` reste un objet unique et `governance_rules` reste un bucket derive autorise

---

## Document 3 - `docs/index/GO_INDEX.md`

### Objet canonique principal

`go_index_truth_list`

### Frontmatter enrichi derivable et prouvable

```yaml
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Tableau canonique des chantiers"
```

Justification :
- le document se definit explicitement comme index operatoire et verite de liste
- aucun champ produit, parent, sous-GO ou support Git ne doit etre derive au niveau du document entier

### `search_tags` autorises

- `surface:continuite`
- `doc_role:index`
- `closeout:reference`

### Groupe d'objets principal

`continuity_indexes`

### Ligne de registre derive d'exemple

```yaml
doc_path: docs/index/GO_INDEX.md
doc_id: OPT_TRADING_GO_INDEX
surface: continuity
doc_type: reprise
canonical_object: go_index_truth_list
group_bucket: continuity_indexes
authority_level: index_canonique_de_liste
reference_canonique_principale: docs/index/GO_INDEX.md
topic_keys: [opt-trading, go_index, continuity, governance]
search_tags: [surface:continuite, doc_role:index, closeout:reference]
is_derived: true
derived_from: docs/index/GO_INDEX.md
updated_at: 2026-04-22
```

### Check de non-regression

- coherence avec `MATRICE_GOUVERNANTE_V2.md` : oui, la matrice reconnait explicitement `GO_INDEX.md` comme verite de liste
- coherence avec `GO_INDEX.md` : oui, aucune derivation n'etend sa portee au-dela de l'index de liste
- absence de seconde doctrine par les tags : oui, le tag `doc_role:index` n'ajoute aucune regle de structure
- absence de taxonomie parallele : oui, `continuity_indexes` ne remplace pas le tableau canonique des chantiers

### Point d'ajustement releve

- le `doc_type` actuel vaut `reprise` alors que le role reel est un index canonique de liste
- la derivation peut absorber ce role via `canonical_object` et `doc_role:index`, mais une clarification documentaire future serait plus propre

---

## Document 4 - `docs/index/NEXT_GO_CANDIDATES.md`

### Objet canonique principal

`next_go_parent_matrix`

### Frontmatter enrichi derivable et prouvable

```yaml
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Matrice - parent actif -> next GO primaire"
```

Justification :
- le document se presente comme une matrice de pilotage par parent actif
- sa dependance a `GO_INDEX.md` comme verite de liste est explicite
- aucun champ parent unique n'est derive car le document couvre plusieurs parents actifs

### `search_tags` autorises

- `surface:chantier`
- `doc_role:index`
- `flow:next_surface`
- `closeout:reference`

### Groupe d'objets principal

`continuity_indexes`

### Ligne de registre derive d'exemple

```yaml
doc_path: docs/index/NEXT_GO_CANDIDATES.md
doc_id: OPT_TRADING_NEXT_GO_CANDIDATES
surface: chantier
doc_type: next_candidate
canonical_object: next_go_parent_matrix
group_bucket: continuity_indexes
authority_level: index_operatoire_derive
reference_canonique_principale: docs/index/GO_INDEX.md
topic_keys: [opt-trading, next, continuity]
search_tags: [surface:chantier, doc_role:index, flow:next_surface, closeout:reference]
is_derived: true
derived_from: docs/index/NEXT_GO_CANDIDATES.md
updated_at: 2026-04-22
```

### Check de non-regression

- coherence avec `MATRICE_GOUVERNANTE_V2.md` : oui si le document reste une surface de navigation et non une verite de liste
- coherence avec `GO_INDEX.md` : partielle, car le document annonce encore `11 GO non clos` alors que `GO_INDEX.md` expose une structure plus large
- absence de seconde doctrine par les tags : oui, les tags restent purement descriptifs
- absence de taxonomie parallele : oui, `next_go_parent_matrix` decrit une fonction operatoire et non une nouvelle famille d'objets

### Point d'ajustement releve

- le pilote confirme un manque de synchronisation documentaire avec `GO_INDEX.md`
- ce document est derivable, mais sa future application devra rester explicitement subordonnee a `GO_INDEX.md` tant que la synchro reelle n'est pas traitee dans un autre lot

---

## Document 5 - `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`

### Objet canonique principal

`product_continuity_hierarchy`

### Frontmatter enrichi derivable et prouvable

```yaml
reference_canonique_principale: docs/governance/MATRICE_GOUVERNANTE_V2.md
intention_produit: "poser une continuite produit hierarchisee en 3 niveaux"
produit_final_voulu: "preserver la trajectoire produit et le paysage global du projet"
point_de_reprise: "Section 2. Modele de continuite"
```

Justification :
- le document porte explicitement la couche produit au-dessus des GO
- il couvre plusieurs centres de gravite ; aucun `produit_centre` unique n'est donc ajoute
- aucun parent ni support Git n'est derive car hors role reel du document

### `search_tags` autorises

- `surface:governance`
- `surface:continuite`
- `doc_role:regle_stable`

### Groupe d'objets principal

`product_continuity`

### Ligne de registre derive d'exemple

```yaml
doc_path: docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
doc_id: null
surface: governance
doc_type: product_continuity_note
canonical_object: product_continuity_hierarchy
group_bucket: product_continuity
authority_level: continuite_produit_canonique
reference_canonique_principale: docs/governance/MATRICE_GOUVERNANTE_V2.md
topic_keys: [opt-trading, product_continuity, hierarchy]
search_tags: [surface:governance, surface:continuite, doc_role:regle_stable]
is_derived: true
derived_from: docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
updated_at: 2026-04-22
```

### Check de non-regression

- coherence avec `MATRICE_GOUVERNANTE_V2.md` : oui, le document renforce le principe `produit d'abord`
- coherence avec `GO_INDEX.md` : oui, il reste au-dessus de la liste des GO et ne la concurrence pas
- absence de seconde doctrine par les tags : oui, aucun tag produit fin n'est utilise pour substituer la hierarchie
- absence de taxonomie parallele : oui, le bucket `product_continuity` correspond a une couche deja prevue dans la doctrine

### Point d'ajustement releve

- le document ne porte pas encore de frontmatter canonique minimal
- le pilote montre qu'une derivation est possible, mais qu'une application future devra d'abord choisir si ce document doit recevoir un `doc_id` avant tout registre derive stable

---

## ETABLI

- le pilote confirme qu'un objet canonique principal peut etre assigne aux 5 documents sans melanger produit, flux parent/sous-GO, support Git et indexation
- le frontmatter enrichi derivable reste tres limite et reste praticable sans invention pour les 5 documents
- les `search_tags` peuvent rester legers si on les borne a surface, role documentaire, flux operatoire minimal et statut documentaire
- un `group_bucket` principal suffit pour chaque document du pilote
- le registre derive peut etre alimente avec un schema simple et non souverain
- `MATRICE_GOUVERNANTE_V2.md` et `GO_INDEX.md` suffisent comme axes de non-regression du pilote

## A_AJUSTER

- `docs/index/NEXT_GO_CANDIDATES.md` doit rester explicitement subordonne a `GO_INDEX.md` tant que sa synchro reelle n'est pas traitee
- `docs/index/GO_INDEX.md` porte aujourd'hui un `doc_type: reprise` qui decrit imparfaitement son role reel d'index canonique de liste
- `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md` aurait besoin d'un noyau frontmatter minimal si une application reelle du registre derive est ouverte plus tard
- les valeurs d'`authority_level` devront etre figees une seule fois avant toute extension du registre derive, pour eviter des libelles flottants

## RISQUES

- risque principal : faire glisser `search_tags` vers une seconde taxonomie si on depasse ce petit set autorise
- risque documentaire : prendre `NEXT_GO_CANDIDATES.md` comme source de liste alors que sa valeur reste operatoire et dependante de `GO_INDEX.md`
- risque d'implementation : pousser un registre derive avant d'avoir fige une convention unique pour les documents sans frontmatter complet
- risque de regression : enrichir des champs produit trop fins sur des documents multi-produits, ce qui recrerait une taxonomie parallele

## VERDICT_PILOTE

`PASS_PILOTE_A_AJUSTER`

Motif :
- la doctrine tient sur le petit lot
- aucune taxonomie parallele n'apparait dans le pilote
- une extension est envisageable seulement apres bornage de quelques ajustements, principalement la relation `NEXT_GO_CANDIDATES.md` -> `GO_INDEX.md` et la gestion des documents encore sans frontmatter stabilise

## POINT_DE_REPRISE

Suite recommandee, sans campagne large :
- figer un mini vocabulaire unique pour `authority_level`
- decider si les documents sans frontmatter complet peuvent recevoir un `doc_id` minimal avant registre derive
- ouvrir ensuite un lot d'application controlee sur ces memes 5 documents, toujours sans sortir du perimetre borne ni ouvrir la synchronisation documentaire reelle
