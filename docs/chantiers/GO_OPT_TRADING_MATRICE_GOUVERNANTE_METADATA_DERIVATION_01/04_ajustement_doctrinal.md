---
doc_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01_AJUSTEMENT_DOCTRINAL
doc_type: chantier_adjustment
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
status: open
lifecycle_stage: adjustment
topic_keys:
  - opt-trading
  - matrice_gouvernante
  - metadata
  - search_tags
  - registry_derived
  - doctrinal_adjustment
surface: chantier
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/02_pilote_dry_run.md
  - docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
---

# 04_ajustement_doctrinal

## Objet

Traiter les trois ajustements bornes identifiés par le pilote, sans elargir le perimetre, sans campagne large et sans modifier les documents sources du repo.

---

## Point 1 - Statut derivable exact de `docs/index/NEXT_GO_CANDIDATES.md`

### Constat

- le document porte une utilite reelle de navigation operatoire
- il reste explicitement subordonne a `GO_INDEX.md`
- il presente encore un decalage de synchro sur le nombre de GO non clos

### Decision doctrinale

`NEXT_GO_CANDIDATES.md` est derivable comme :
- surface operatoire derivee
- matrice de navigation par parent actif
- index secondaire non souverain

Il n'est pas derivable comme :
- verite de liste
- source de cardinalite systeme
- surface d'arbitrage canonique des chantiers

### Regle de derivation

Pour `NEXT_GO_CANDIDATES.md` :
- `reference_canonique_principale` doit pointer vers `docs/index/GO_INDEX.md`
- `canonical_object` doit decrire une fonction de navigation et non une fonction de liste canonique
- `authority_level` doit rester inferieur a celui de `GO_INDEX.md`
- aucune valeur derivee ne doit reprendre comme verite autonome un compteur global ou une cardinalite de GO

### Effet bloquant leve

Le blocage n'est plus doctrinal.
Il reste documentaire seulement, et reporte hors du present lot.

---

## Point 2 - Clarification du `doc_type` reel de `docs/index/GO_INDEX.md`

### Constat

- le frontmatter source porte aujourd'hui `doc_type: reprise`
- le role reel etabli par le document et par la matrice est celui d'un index canonique de liste

### Decision doctrinale

Sans modifier le document source a ce stade :
- le `doc_type` source est conserve tel quel dans le repo
- le role reel retenu pour la derivation est `canonical_list_index`

### Regle de derivation

Pour `GO_INDEX.md` :
- le registre derive peut conserver `doc_type_source: reprise` si le schema l'autorise plus tard
- la qualification fonctionnelle a utiliser dans les vues derivees est `canonical_list_index`
- `canonical_object` reste `go_index_truth_list`
- cette clarification ne vaut pas requalification documentaire du fichier source

### Effet bloquant leve

Le desalignement entre type source et role reel n'empeche plus l'extension controlee tant que la distinction :
- type source
- role fonctionnel derive

reste explicite.

---

## Point 3 - Noyau frontmatter minimal de `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`

### Constat

- le document porte deja une fonction canonique claire sur la couche produit
- il ne porte pas encore de frontmatter
- le pilote a montre qu'une derivation est possible, mais encore fragile pour le registre derive stable

### Decision doctrinale

Le noyau frontmatter minimal requis si une application reelle est ouverte plus tard est borne a :

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

### Regle doctrinale

- aucun champ parent, sous-GO ou support Git ne doit etre ajoute a ce document
- aucun `produit_centre` unique ne doit etre force, car le document couvre plusieurs centres de gravite
- les champs enrichis doivent rester macroscopiques et limites a :
  - `reference_canonique_principale`
  - `intention_produit`
  - `produit_final_voulu`
  - `point_de_reprise`

### Effet bloquant leve

L'absence actuelle de frontmatter n'interdit plus l'extension controlee :
- si l'on reste en dry-run
- ou si toute application reelle commence par ce noyau minimal et rien de plus

---

## Resume de doctrine ajustee

- `GO_INDEX.md` reste la seule verite de liste
- `NEXT_GO_CANDIDATES.md` est derivable comme navigation operatoire secondaire et non comme liste
- le `doc_type` source de `GO_INDEX.md` ne suffit pas a decrire son role reel ; la derivation doit distinguer type source et role fonctionnel
- `PRODUCT_CONTINUITY_HIERARCHY_01.md` peut entrer dans une extension controlee si son eventuelle application reelle commence par un noyau frontmatter minimal strict

---

## Point de reprise

Rejouer un mini pilote dry-run sur :
- `docs/index/GO_INDEX.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`
