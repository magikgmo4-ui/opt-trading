---
doc_id: GO_OPT_TRADING_PARENT_NAMING_CANON_01_PARENT
doc_type: chantier_parent
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_NAMING_CANON_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - naming
  - canon
  - normalization
  - module
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Plan valide"
updated_at: 2026-04-22
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/NAMING_CANON_POLICY_01.md
  - docs/index/GO_INDEX.md
---

# GO_OPT_TRADING_PARENT_NAMING_CANON_01

## Classification
gouvernance + chantier parent + module durable audit-only de normalisation de nommage

## Role recommande
architecte de gouvernance repo + designer de module durable audit-first

## Besoin initial
Uniformiser le nommage pour l'avenir, sans dependre de la session, sans casser le repo existant, et sans concurrencer le canon GO deja publie.

## Cible finale
Avoir un cadre de nommage explicite, documente, outille et reutilisable ou :

- le canon GO du repo reste la source structurante pour les GO
- la politique de nommage par surface reste une couche transverse subordonnee
- les nouveaux objets suivent le canon sans ambiguite
- l'existant est audite avant toute application
- un module durable peut detecter les ecarts et proposer un nom canonique
- un futur GO pourra appliquer des renommages bornes si cela devient utile

## Source canonique
- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`

## ETABLI
- le repo contient deja des surfaces avec conventions implicites distinctes
- la normalisation transverse peut etre par surface
- les GO doivent respecter la forme `GO_<SCOPE>_<PRODUCT_OR_SURFACE>_<ROLE>_<OBJECT>_<NN>`
- le premier lot doit etre documentaire + module audit-only
- aucun renommage de l'existant n'est inclus dans ce parent
- aucun nouveau `<PRODUCT_OR_SURFACE>` n'est traite comme deja valide par defaut

## Plan valide

### Axe 1 - Politique canonique
Poser la politique transverse de nommage sans redefinir le canon GO.

### Axe 2 - Inventaire reel
Recenser les ecarts presents dans le repo par famille :
- `docs/chantiers`
- `docs/governance`
- `modules`
- scripts
- branches

### Axe 3 - Module durable
Creer `modules/naming_normalizer` en V1 audit-only :
- detection
- proposition encadree ou marquage review-required si la source canonique manque
- rapport lisible
- sortie machine

### Axe 4 - Application future
Preparer plus tard un GO separe pour les renommages reels bornes.

## Anti-cibles
Ne pas faire :
- renommage global immediat
- reecriture opportuniste du repo
- regle implicite non documentee
- melange entre inventaire et application

## Gap restant
Il reste a produire :
1. l'inventaire reel des ecarts
2. le rapport V1 du module
3. la qualification des exceptions legacy
4. le lot eventuel d'application borne

## GO suivants proposes

### GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01
Inventaire repo-first des ecarts de nommage et classement par surface.

### GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01
Creation du module durable audit-only `naming_normalizer`.

### GO_OPT_TRADING_CHILD_NAMING_APPLY_BATCH_01
Lot futur, optionnel, de renommage borne apres validation.

## TODO
- ouvrir le parent
- creer la politique canonique
- lancer l'inventaire
- executer le module sur le repo
- decider des exceptions
- differer l'apply a un lot separe

## REPRISE
Point de reprise recommande :
`GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01`

Sequence :
politique -> inventaire reel -> module audit-only -> eventuel apply borne
