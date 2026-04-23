---
doc_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01_SECOND_LOT_BORNE
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
  - second_lot
surface: chantier
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/07_surveillance_pilote.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/08_registry_derived_pilot_delta.yaml
  - docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
  - docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md
  - docs/governance/DOC_LAYERS.md
---

# 08_second_lot_borne

## Lot retenu

Second lot borne compose uniquement de surfaces de gouvernance deja stables :
- `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`
- `docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md`
- `docs/governance/DOC_LAYERS.md`

Justification :
- role documentaire clair
- souverainete non ambiguë
- enrichissement leger possible
- aucune dependance a une cardinalite mouvante
- pas de collision directe avec `GO_INDEX.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md` ou `BRANCH_STATE.md`

---

## Criteres d'eligibilite

### `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`

- role documentaire clair : oui, doctrine locale de derivation
- souverainete non ambiguë : oui, explicitement subordonnee a `MATRICE_GOUVERNANTE_V2.md`
- enrichissement leger possible : oui
- dependance a une cardinalite mouvante : non
- risque de collision doctrinale : faible

### `docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md`

- role documentaire clair : oui, fiche de methode canonique
- souverainete non ambiguë : oui, surface de reference et non index operatoire
- enrichissement leger possible : oui
- dependance a une cardinalite mouvante : non
- risque de collision doctrinale : borne si les tags restent purement descriptifs

### `docs/governance/DOC_LAYERS.md`

- role documentaire clair : oui, regle stable de couches documentaires
- souverainete non ambiguë : oui
- enrichissement leger possible : oui
- dependance a une cardinalite mouvante : non
- risque de collision doctrinale : faible

---

## Application minimale realisee

### `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`

- objet canonique principal : `metadata_derivation_doctrine`
- frontmatter derive applique :
  - `search_tags`
  - `reference_canonique_principale`
  - `point_de_reprise`
- `search_tags` :
  - `surface:governance`
  - `doc_role:regle_stable`
  - `closeout:reference`
- groupe d'objets : `governance_rules`
- ligne de registre derive : see `08_registry_derived_pilot_delta.yaml`
- check de non-regression :
  - la subordination a `MATRICE_GOUVERNANTE_V2.md` est conservee
  - aucune promotion du registre derive

### `docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md`

- objet canonique principal : `extracteur_tags_canonical_method`
- frontmatter derive applique :
  - `search_tags`
  - `reference_canonique_principale`
  - `point_de_reprise`
- `search_tags` :
  - `surface:governance`
  - `doc_role:regle_stable`
  - `closeout:reference`
- groupe d'objets : `governance_rules`
- ligne de registre derive : see `08_registry_derived_pilot_delta.yaml`
- check de non-regression :
  - aucun tag ne remplace la methode de routage
  - aucune extension du vocabulaire au-dela du set deja employe

### `docs/governance/DOC_LAYERS.md`

- objet canonique principal : `doc_layers_rule`
- frontmatter derive applique :
  - `search_tags`
  - `reference_canonique_principale`
  - `point_de_reprise`
- `search_tags` :
  - `surface:governance`
  - `doc_role:regle_stable`
  - `closeout:reference`
- groupe d'objets : `governance_rules`
- ligne de registre derive : see `08_registry_derived_pilot_delta.yaml`
- check de non-regression :
  - aucune confusion avec les couches operatoires vivantes
  - aucune dependance a `REPRISE.md` ou `BRANCH_STATE.md`

---

## RISQUES_DE_DERIVE

- risque faible d'uniformisation trop large si `search_tags` deviennent un reflexe automatique sur toute gouvernance
- risque de prolifération si `doc_type_fonctionnel` est etendu sans borne au-dela des quelques valeurs deja posees
- risque de melange avec d'autres changements du worktree si le lot n'est pas garde strictement separe

## VERDICT_SECOND_LOT

`SECOND_LOT_APPLIQUE`

Motif :
- les trois documents retenus sont eligibles sans ambiguite
- l'application est minimale et non intrusive
- aucune derive de souverainete n'est introduite
- aucun nouveau front documentaire n'est ouvert

## POINT_DE_REPRISE

Si une suite est ouverte :
- rester sur des surfaces de gouvernance stables ou references explicites deja citees par le GO
- exclure toujours les surfaces operatoires vivantes
- conserver le registre derive comme support local non souverain
