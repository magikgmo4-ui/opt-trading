---
doc_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01_SURVEILLANCE_PILOTE
doc_type: chantier_surveillance
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
status: open
lifecycle_stage: surveillance
topic_keys:
  - opt-trading
  - matrice_gouvernante
  - metadata
  - search_tags
  - registry_derived
  - pilot_surveillance
surface: chantier
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/06_extension_controlee.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/06_registry_derived_pilot.yaml
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
---

# 07_surveillance_pilote

## Objet

Verifier, apres extension controlee, que le pilote reste borne, non souverain et sans derive documentaire avant toute ouverture d'un second lot borne.

---

## ETABLI

- `GO_INDEX.md` reste la verite de liste et n'a recu que des ajouts legers :
  - `search_tags`
  - `reference_canonique_principale`
  - `point_de_reprise`
- `NEXT_GO_CANDIDATES.md` reste une surface de navigation operatoire derivee et subordonnee :
  - le frontmatter pointe deja vers `GO_INDEX.md`
  - un rappel explicite de priorite a ete ajoute dans le corps pour lever l'ambiguite de souverainete
- `PRODUCT_CONTINUITY_HIERARCHY_01.md` n'a recu que le noyau minimal autorise plus des champs produit macroscopiques :
  - pas de parent
  - pas de sous-GO
  - pas de support Git
  - pas de `produit_centre` force
- `06_registry_derived_pilot.yaml` reste clairement non souverain :
  - `registry_kind: derived_non_sovereign`
  - `is_derived: true`
  - `derived_from` renseigne pour chaque record

## DOCUMENTS_RELUS

- `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/00_cadrage.md`
- `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/03_decisions.md`
- `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/06_extension_controlee.md`
- `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/06_registry_derived_pilot.yaml`
- `docs/index/GO_INDEX.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`

## RISQUES_DE_DERIVE

- le compteur local de `NEXT_GO_CANDIDATES.md` reste potentiellement stale ; il ne doit jamais etre relu comme cardinalite canonique
- le couple `doc_type_fonctionnel` / `authority_level` du registre derive doit rester a vocabulaire tres borne
- une extension trop rapide pourrait pousser `search_tags` a compenser des ecarts documentaires reels, ce qui est interdit
- le worktree global contient d'autres changements hors lot ; ils ne doivent pas etre melanges a la suite du present GO

## VERDICT_PILOTE

`SECOND_LOT_BORNE_AUTORISABLE`

Motif :
- le pilote reste borne et doctrinalement propre apres audit repo-first
- l'ambiguite principale de souverainete sur `NEXT_GO_CANDIDATES.md` a ete reduite par un patch minimal
- aucun signal n'impose un gel complet
- aucun retour au pilote amont n'est necessaire a ce stade

## POINT_DE_REPRISE

Si une suite est ouverte :
- rester dans ce GO
- choisir un second lot borne compose uniquement de surfaces deja stabilisees doctrinalement
- exclure `REPRISE.md`, `BRANCH_STATE.md` et toute synchronisation documentaire reelle
- conserver `06_registry_derived_pilot.yaml` comme support derive local, non comme source canonique
