---
doc_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01_CONSOLIDATION_BORNEE
doc_type: chantier_consolidation
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
status: open
lifecycle_stage: consolidation
topic_keys:
  - opt-trading
  - matrice_gouvernante
  - metadata
  - search_tags
  - registry_derived
  - bounded_consolidation
surface: chantier
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/06_extension_controlee.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/06_registry_derived_pilot.yaml
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/07_surveillance_pilote.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/08_second_lot_borne.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/08_registry_derived_pilot_delta.yaml
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
  - docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md
  - docs/governance/DOC_LAYERS.md
---

# 09_consolidation_bornee

## Objet

Verifier, apres deux lots bornes, que la derivation reste :
- legere
- lisible
- reversible
- non intrusive
- non compensatoire d'une faiblesse documentaire reelle

Sans ouvrir automatiquement un troisieme lot.

---

## ETABLI

- les six documents enrichis portent un schema derive coherent :
  - `search_tags`
  - `reference_canonique_principale`
  - `point_de_reprise`
- la cardinalite des `search_tags` reste legere sur tout le lot :
  - 3 tags sur les surfaces de gouvernance stables
  - 3 a 4 tags sur les surfaces de continuite deja traitees
- `reference_canonique_principale` reste stable et lisible :
  - auto-reference pour les surfaces de reference ou d'index
  - reference a `MATRICE_GOUVERNANTE_V2.md` seulement pour les surfaces explicitement subordonnees a cette matrice
- `point_de_reprise` reste localise et humainement lisible, sans devenir une seconde navigation lourde
- aucun enrichissement ne tente de corriger une contradiction documentaire reelle
- les registres derives `06_registry_derived_pilot.yaml` et `08_registry_derived_pilot_delta.yaml` restent clairement non souverains

## DOCUMENTS_RECROISES

- `docs/index/GO_INDEX.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`
- `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`
- `docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md`
- `docs/governance/DOC_LAYERS.md`
- `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/06_extension_controlee.md`
- `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/06_registry_derived_pilot.yaml`
- `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/07_surveillance_pilote.md`
- `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/08_second_lot_borne.md`
- `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/08_registry_derived_pilot_delta.yaml`

## COHERENCE_DERIVEE

- homogeneite des champs derives : bonne
- stabilite des `search_tags` : bonne, avec un set encore court et repetable
- stabilite de `reference_canonique_principale` : bonne
- stabilite de `point_de_reprise` : bonne
- glissement de souverainete : non detecte
- proliferation de vocabulaire derive : sous controle, mais c'est le risque principal a surveiller

## RISQUES_RESIDUELS

- le vocabulaire `doc_type_fonctionnel` et `authority_level` commence a s'etendre ; il doit rester borne avant toute suite
- `NEXT_GO_CANDIDATES.md` reste structurellement subordonne, mais son compteur local peut toujours devenir stale
- une suite trop rapide pourrait transformer le schema actuel en reflexe de tagging plutot qu'en derivation motivee
- le worktree global reste charge de changements hors lot, ce qui renforce le besoin de gel local plutot que d'ouverture immediate d'un troisieme lot

## VERDICT_CONSOLIDATION

`CONSOLIDATION_OK_GEL_RECOMMANDE`

Motif :
- apres deux lots, la derivation reste saine et lisible
- aucun ajustement minimal supplementaire n'est requis sur les documents deja enrichis
- le risque residuel porte sur l'extension du vocabulaire derive, pas sur une incoherence du lot courant
- il est donc plus propre de geler ici plutot que d'ouvrir automatiquement un troisieme lot

## POINT_DE_REPRISE

Si une suite est un jour rouverte :
- ne pas partir d'un troisieme lot par inertie
- commencer par figer explicitement un mini lexique ferme pour `doc_type_fonctionnel` et `authority_level`
- reevaluer ensuite si un nouveau lot borne est vraiment necessaire
