---
doc_id: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: memory_bricks
module: memory_bricks
go_id: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01
chantier_parent: opt_trading_memory_bricks_localcms_consumer
sous_chantier: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01
intention_parent: aligner proprement le canon memory_bricks de opt-trading avec un consumer reel LocalCMS, sans melanger spec, implementation et adaptation UI, et sans sauter directement a un patch technique non cadre
cible_finale_parent: obtenir une chaine producer consumer claire, stable et documentee entre opt-trading et LocalCMS, avec contrat minimal valide, ordre d'implementation explicite, fallback assume si necessaire, et reprise propre par GO successifs
objectif_sous_chantier: figer le contrat minimal cible entre la spec memory_bricks de opt-trading et la surface consumer reelle de LocalCMS
objectif_local_go: produire un cadrage canonique du contrat producer consumer avant toute implementation
cible_locale_go: inventaire des ecarts + matrice canon/consumer + decisions de contrat + ordre des GO suivants + reprise
reference_canonique_principale: modules/memory_bricks/docs/SPEC_MEMORY_BRICKS_API_V2_READONLY.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01/00_cadrage.md
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - memory_bricks
  - localcms
  - contract_alignment
  - consumer
  - readonly_api
surface: governance
source_kind: canonical
updated_at: 2026-04-17
links:
  - modules/memory_bricks/docs/SPEC_MEMORY_BRICKS_API_V2_READONLY.md
  - docs/governance/MEMORY_BRICKS_MAPPING.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/index/REPRISE.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONSUMER/00B_parent_scope_and_structure.md
---

# GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01 — Cadrage

## Objet

Ouvrir le premier sous-chantier de convergence entre :

- le canon `memory_bricks` porté par `opt-trading`
- la surface consumer réelle portée par `LocalCMS`

Ce GO ne met en oeuvre ni endpoint, ni patch UI.
Il cadre d'abord le contrat.

---

## Besoin initial

Éviter une implémentation prématurée d'une API ou d'un patch consumer sans avoir figé :

- le contrat minimal réellement utile
- le niveau d'alignement attendu
- le mode de transition retenu

---

## Intention

Rendre la trajectoire producer/consumer plus sûre et plus rejouable en figeant d'abord :

- le canon de référence
- la surface consumer réelle
- les écarts importants
- les confirmations nécessaires
- l'ordre de travail

---

## Produits finaux voulus / objectifs du chantier parent

Le chantier parent vise une trajectoire complète de convergence producer/consumer avec :

- un contrat minimal lisible et stable
- une séparation explicite entre V1 fichier local et V2 HTTP read-only
- une décision claire sur le mode principal et le fallback
- un ordre d'implémentation sûr
- une continuité documentaire propre entre `opt-trading` et `LocalCMS`

---

## Cible finale du chantier parent

Obtenir une chaîne producer/consumer claire, stable et documentée entre `opt-trading` et `LocalCMS`, sans rouvrir un audit global à chaque étape et sans patch technique prématuré.

---

## Plan validé

### GO_1 — présent cadrage
- inventorier le canon réellement fixé côté `opt-trading`
- inventorier la surface consumer réellement établie côté `LocalCMS`
- lister les écarts structurels utiles
- décider le contrat minimal cible
- décider l'ordre des GO suivants
- ne rien implémenter dans ce GO

### GO_2 — implémentation minimale producer
GO candidat :
`GO_OPT_TRADING_MEMORY_BRICKS_API_V2_MINIMAL_IMPL_01`

But :
- implémenter seulement le plus petit sous-ensemble read-only validé par le cadrage

### GO_3 — adoption consumer
GO candidat :
`GO_LOCALCMS_MEMORY_BRICKS_HTTP_CONSUMER_ADOPT_01`

But :
- faire adopter le contrat minimal côté consumer, sans casser le chemin existant si un fallback est retenu

### GO_4 — fallback / transition / hardening
GO candidat :
`GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_TRANSITION_HARDENING_01`

But :
- figer le mode cible final et fermer la transition

---

## ETABLI

- la source canonique côté repo est `opt-trading`
- `MEMORY_BRICKS_MAPPING.md` fixe que `memory_bricks` est une forme compacte dérivée
- la spec V2 read-only existe comme spec de contrat
- `LocalCMS` est déjà un consumer réel
- le lot `memory_view` côté `LocalCMS` a déjà été stabilisé et ne doit pas être rouvert par défaut
- un cadrage producer/consumer explicite manquait encore

---

## Périmètre du présent GO

### Inclus
- comparaison canon `opt-trading` vs consumer `LocalCMS`
- matrice de contrat
- décisions d'alignement
- séquencement des GO suivants

### Exclus
- implémentation FastAPI ou équivalent
- patch runtime de `memory_bricks`
- patch UI `LocalCMS`
- migration de données
- bascule de mode en production

---

## Matrice à produire dans ce GO

Le GO doit figer au minimum :

- format de liste :
  - array plat
  - ou envelope `{items,total,limit,offset}`
- besoin réel de pagination
- besoin réel de `content_markdown`
- besoin réel de `links`
- besoin réel des indexes bruts
- stratégie de fallback :
  - V1 fichier
  - V2 HTTP
  - hybride

---

## Rôles séparés

### Rôle repo / produit
- `opt-trading` = canon producer
- `LocalCMS` = consumer

### Rôle IA / IDE
- cadrer le contrat
- séparer confirmé / à confirmer
- ordonner les prochains GO

### Rôle machine
- aucun runtime engagé à ce stade
- docs-only

---

## Gap restant

Il manque encore avant toute implémentation :

- une matrice canon vs consumer figée
- une décision sur le contrat minimal réellement requis
- une décision sur la stratégie de transition
- une priorisation explicite des GO techniques

---

## Next GO

Sous réserve du cadrage confirmé, la suite naturelle est :

`GO_OPT_TRADING_MEMORY_BRICKS_API_V2_MINIMAL_IMPL_01`

puis :

`GO_LOCALCMS_MEMORY_BRICKS_HTTP_CONSUMER_ADOPT_01`

---

## REPRISE

### Reprise globale
- `docs/index/REPRISE.md`

### Reprise chantier parent
- `docs/chantiers/GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONSUMER/00B_parent_scope_and_structure.md`

### Point de reprise local
- `docs/chantiers/GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01/00_cadrage.md`

---

## Statut

**OPEN — chantier parent consumer posé ; sous-chantier de contract alignment ouvert ; aucune implémentation encore engagée**
