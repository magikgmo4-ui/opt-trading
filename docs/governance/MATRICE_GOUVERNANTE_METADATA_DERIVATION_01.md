---
doc_id: OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
doc_type: governance_policy
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - matrice_gouvernante
  - metadata
  - search_tags
  - registry_derived
search_tags:
  - surface:governance
  - doc_role:regle_stable
  - closeout:reference
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_GOUVERNANTE_V2.md
point_de_reprise: "Section Perimetre pilote"
updated_at: 2026-04-22
links:
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md
  - docs/governance/DOC_LAYERS.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/01_plan.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/03_decisions.md
  - docs/index/GO_INDEX.md
---

# MATRICE_GOUVERNANTE_METADATA_DERIVATION_01

## Objet

Fixer une doctrine legere et controlee de derivation pour :
- le frontmatter enrichi
- les `search_tags`
- les groupes d'objets
- le registry derive

Cette doctrine vient apres la matrice gouvernante V2.
Elle ne modifie pas la doctrine de la matrice.

---

## Priorite canonique

La matrice gouvernante V2 prime sur cette doctrine.

Regles de priorite :
- `GO_INDEX.md` reste la verite de liste
- `REPRISE.md` reste une surface operatoire seulement
- `BRANCH_STATE.md` reste limite a la surface branches
- les derives metadata / tags / registry ne remplacent jamais une verite canonique

---

## Perimetre

La doctrine couvre seulement :
- quels champs enrichis peuvent etre derives du noyau canonique
- comment produire des `search_tags` controles
- comment former des groupes d'objets stables
- comment maintenir un registry derive non souverain

Hors perimetre :
- synchronisation documentaire reelle
- correction des contradictions locales de fond
- modification de la matrice gouvernante V2
- promotion de `REPRISE.md` ou `BRANCH_STATE.md` au-dessus de leur role retenu
- cas `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`

---

## Doctrine de derivation

### 1. Frontmatter enrichi

Le frontmatter enrichi est derive a partir :
- du noyau canonique deja etabli
- de la matrice gouvernante V2
- du document source reel

Le frontmatter enrichi ne doit pas :
- inventer un parent
- inventer un sous-GO
- deduire un support Git non prouve
- deduire un etat produit non etabli

Champs enrichissables si et seulement si prouvables :
- `chantier_parent`
- `sous_chantier`
- `intention_parent`
- `cible_finale_parent`
- `objectif_local_go`
- `cible_locale_go`
- `produit_centre`
- `famille_produit`
- `intention_produit`
- `produit_final_voulu`
- `point_de_reprise`
- `reference_canonique_principale`

Schema de preuve :
- un champ enrichi n'est ecrit que si sa source canonique est identifiable
- si la preuve manque, le champ est omis et non rempli par une valeur par defaut decorative
- un enrichissement n'a pas le droit de "completer" la structure d'un document si cette structure n'est pas deja etablie dans le repo

Source attendue par famille :
- parent / sous-GO : `GO_INDEX.md`, dossier chantier prouve, ou matrice gouvernante V2
- produit : matrice gouvernante V2, fiche produit canonique, ou document source qui porte explicitement cette couche
- reprise / reference : document source lui-meme ou reference canonique explicite

Forme recommandee du frontmatter enrichi :

#### Bloc structure
- `chantier_parent`
- `sous_chantier`
- `reference_canonique_principale`
- `point_de_reprise`

#### Bloc flux local
- `intention_parent`
- `cible_finale_parent`
- `objectif_local_go`
- `cible_locale_go`

#### Bloc produit
- `produit_centre`
- `famille_produit`
- `intention_produit`
- `produit_final_voulu`

#### Bloc etat produit
- `plan_macro_valide`
- `jalons_clos`
- `etat_global_courant`
- `gap_global_restant`
- `suite_logique`

Regles d'ecriture :
- ne jamais dupliquer un champ deja canonique sous un autre nom
- ne jamais ecrire un champ produit sur un document qui ne porte aucune couche produit prouvable
- ne jamais ecrire un champ parent sur un document dont le parent n'est pas prouve
- un document de support peut rester avec le frontmatter noyau seul si l'enrichissement ne serait qu'inferentiel

### 2. Search tags

Les `search_tags` sont des facettes derivees et controlees.

Ils doivent :
- etre stables
- etre courts
- rester secondaires face au frontmatter
- servir la recherche, non la gouvernance

Ils ne doivent pas :
- porter seuls une regle de structure
- remplacer `topic_keys`
- transformer une hypothese en classification persistante

Familles de tags autorisables a terme :
- surface
- role documentaire
- produit
- flux
- support Git
- etat de closeout

Taxonomie autorisee :
- `surface:<valeur>`
- `doc_role:<valeur>`
- `product:<valeur>`
- `flow:<valeur>`
- `git_support:<valeur>`
- `closeout:<valeur>`

Valeurs autorisables seulement si prouvables :
- `surface:governance`, `surface:chantier`, `surface:continuite`, `surface:architecture`, `surface:registry`
- `doc_role:regle_stable`, `doc_role:index`, `doc_role:cadrage`, `doc_role:decision`, `doc_role:closeout`, `doc_role:carte`
- `product:desk_pro`, `product:trading_dual_stack_v1`, `product:bot_vision` si la couche produit est explicitement portee
- `flow:parent`, `flow:subgo`, `flow:go_simple`, `flow:next_surface`, `flow:operational_support`
- `git_support:trunk`, `git_support:branche_dediee`, `git_support:herite_parent` seulement si ce support est etabli
- `closeout:open`, `closeout:active`, `closeout:reference`, `closeout:closed`, `closeout:pass` selon le statut documentaire etabli

Regles de construction :
- pas de tag libre hors taxonomie autorisee
- pas de tag compose qui melange produit et Git dans une meme cle
- pas de tag qui remplace un champ frontmatter deja existant
- pas de tag pour compenser une contradiction documentaire reelle

Cardinalite legere recommande :
- 0 a 2 tags `surface`
- 0 a 2 tags `doc_role`
- 0 a 2 tags `product`
- 0 a 2 tags `flow`
- 0 a 1 tag `git_support`
- 0 a 1 tag `closeout`

Cette cardinalite vise a garder des facettes lisibles et non un nuage de tags opportuniste.

### 3. Groupes d'objets

Un groupe d'objets est une vue derivee de recroisement.

Il peut agreger par exemple :
- regles stables
- parents chantiers
- sous-GO
- index operatoires
- supports branches
- cartes humaines

Un groupe d'objets ne doit pas :
- devenir une seconde taxonomie souveraine
- concurrencer la matrice ou `GO_INDEX.md`
- melanger produit et Git dans une meme etiquette de base

Regle de construction :
- un groupe d'objets se construit a partir du role canonique principal de l'objet
- le groupe doit etre stable a travers plusieurs sessions
- un objet n'est groupe qu'une fois dans son groupe principal
- des vues secondaires peuvent exister dans le registry derive, mais pas comme seconde appartenance souveraine

Buckets autorises :
- `governance_rules`
- `product_continuity`
- `chantier_parents`
- `chantier_subgo`
- `continuity_indexes`
- `branch_supports`
- `placement_maps`
- `derived_registry_supports`

Regle de rattachement :
- `governance_rules` : regles stables et matrices de gouvernance
- `product_continuity` : documents qui portent explicitement la couche produit
- `chantier_parents` : dossiers parents ou GO simples structurants
- `chantier_subgo` : sous-GO reels et bornes
- `continuity_indexes` : `GO_INDEX`, `NEXT_GO_CANDIDATES`, `ACTIVE_STREAMS`, `REPRISE`
- `branch_supports` : surfaces branches et housekeeping
- `placement_maps` : cartes humaines de placement
- `derived_registry_supports` : objets purement derives non souverains

Interdit :
- creer un bucket ad hoc pour un seul cas problematique
- utiliser les buckets pour contourner l'absence de parent prouve

### 4. Registry derive

Le registry derive sert :
- a exposer une indexation machine-readable
- a consolider la recherche
- a faciliter des vues derivees

Le registry derive ne sert pas :
- a gouverner la structure
- a remplacer le frontmatter canonique
- a contredire la matrice

Regle :
- frontmatter canonique d'abord
- puis `topic_keys`
- puis `search_tags`
- puis registry derive

Schema minimal de record derive :
- `doc_path`
- `doc_id`
- `surface`
- `doc_type`
- `canonical_object`
- `group_bucket`
- `authority_level`
- `reference_canonique_principale`
- `topic_keys`
- `search_tags`
- `is_derived`
- `derived_from`
- `updated_at`

Regles de schema :
- `is_derived` doit toujours valoir vrai
- `derived_from` doit pointer vers le document source reel
- le record derive peut resumer un objet, pas le requalifier
- le registry derive ne doit jamais porter une valeur plus forte que le document source

Formats possibles plus tard :
- yaml
- json
- table markdown exportee

Le choix de format n'est pas la doctrine.
La doctrine est la non-souverainete et la tracabilite de derivation.

---

## Controles

Toute derivation doit rester compatible avec :
- `docs/governance/MATRICE_GOUVERNANTE_V2.md`
- `docs/index/GO_INDEX.md`
- la surface documentaire reelle du document source

Checks minimaux :
- parent prouve ou absent
- sous-GO prouve ou absent
- role produit explicite ou non renseigne
- surface documentaire correcte
- indexation minimale compatible avec la matrice

Checks de derivation :
- aucun champ enrichi sans preuve source
- aucun `search_tag` hors taxonomie autorisee
- un seul `group_bucket` principal par objet
- record registry derive marque explicitement comme derive
- aucun usage de `REPRISE.md` comme verite de liste
- aucun usage de `BRANCH_STATE.md` comme doctrine structurelle

---

## Perimetre pilote

Avant toute application plus large, la doctrine doit etre testee sur un petit perimetre pilote.

Documents pilotes retenus :
- `docs/governance/MATRICE_GOUVERNANTE_V2.md`
- `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`
- `docs/index/GO_INDEX.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`

But du pilote :
- verifier qu'un enrichissement prouvable est possible
- verifier que la taxonomie `search_tags` reste legere
- verifier qu'un `group_bucket` principal suffit
- verifier qu'un record registry derive peut etre forme sans concurrence avec le noyau

Livrables pilotes attendus plus tard :
- une proposition d'enrichissement frontmatter pour chaque document pilote
- une proposition de `search_tags` controles
- un `group_bucket` principal par document
- un exemple de record registry derive

Garde pilote :
- aucun tagging massif
- aucune campagne repo-wide
- aucun traitement du cas `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- aucun chantier de synchronisation documentaire reelle
- priorite au dry-run documentaire ou a la proposition structuree

---

## Invariants

- les derives viennent apres la structure
- le frontmatter prime sur les tags
- `topic_keys` priment sur les `search_tags`
- le registry derive n'est pas souverain
- aucune derivation ne corrige une contradiction documentaire reelle
- aucune derivation n'ouvre le chantier de synchronisation documentaire reelle
- aucun pilote ne doit etre elargi en campagne globale sans GO dedie ou decision explicite

---

## Reprise

Point de reprise recommande :
- `GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01`

Condition de reprise :
- rester strictement dans le lot doc-only de derivation controlee
