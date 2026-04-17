---
doc_id: OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONSUMER_PARENT_SCOPE
doc_type: chantier_addendum
repo: opt-trading
project: memory_bricks
module: memory_bricks
go_id: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONSUMER
chantier_parent: opt_trading_memory_bricks_localcms_consumer
sous_chantier: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01
intention_parent: aligner proprement le canon memory_bricks de opt-trading avec un consumer reel LocalCMS, sans melanger spec, implementation et adaptation UI, et sans sauter directement a un patch technique non cadre
cible_finale_parent: obtenir une chaine producer consumer claire, stable et documentee entre opt-trading et LocalCMS, avec contrat minimal valide, ordre d'implementation explicite, fallback assume si necessaire, et reprise propre par GO successifs
objectif_sous_chantier: ouvrir la trajectoire consumer par un premier cadrage de contrat entre le canon opt-trading et la surface reelle LocalCMS
objectif_local_go: figer le contrat minimal cible, les ecarts reels producer consumer, le mode de convergence retenu et le point de reprise avant toute implementation
cible_locale_go: matrice canon vs consumer + decisions de contrat + ordre des GO suivants + reprise
reference_canonique_principale: modules/memory_bricks/docs/SPEC_MEMORY_BRICKS_API_V2_READONLY.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONSUMER/00B_parent_scope_and_structure.md
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - memory_bricks
  - localcms
  - consumer
  - contract
  - parent_chantier
  - continuity
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
---

# GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONSUMER — Portée parent et structure

## Objet

Figer explicitement qu'un chantier parent consumer existe désormais pour la trajectoire :

- `opt-trading` comme source canonique `memory_bricks`
- `LocalCMS` comme consumer réel
- convergence progressive du contrat, sans sauter directement à l'implémentation

---

## Besoin initial

Éviter que les prochains GO sur `memory_bricks` ↔ `LocalCMS` soient lus comme des chantiers isolés ou techniques, sans lien avec une cible finale consumer documentée.

---

## Intention

- garder un chantier parent clair côté consumer
- séparer canon producer / consumer réel / adaptation locale
- faire suivre cette logique dans les sous-chantiers
- éviter de confondre cadrage de contrat, implémentation API et patch UI

---

## Produits finaux voulus / objectifs du chantier parent

Le chantier parent vise une trajectoire complète de convergence producer/consumer avec :

- un contrat minimal lisible et stable
- une séparation explicite entre V1 fichier local et V2 HTTP read-only
- une décision claire sur le mode principal et le fallback
- un ordre d'implémentation sûr
- une continuité documentaire propre entre `opt-trading` et `LocalCMS`

L'horizon final visé est :

- un producer `memory_bricks` canonique côté `opt-trading`
- un consumer `LocalCMS` aligné sur un contrat validé
- une reprise plus simple
- moins d'ambiguïté entre spec, export, endpoint et rendu UI
- une trajectoire découpée en GO propres

---

## Cible finale du chantier parent

Obtenir une chaîne producer/consumer claire, stable et documentée entre `opt-trading` et `LocalCMS`, sans rouvrir un audit global à chaque étape et sans patch technique prématuré.

---

## Next GO

Chaque GO suivant doit être documenté comme :

- une étape
- ou un sous-chantier

à l'intérieur du chantier parent consumer.

Chaque GO doit donc faire suivre explicitement :

- le besoin initial parent
- l'intention parent
- la cible finale du chantier parent
- la cible locale du GO
- la référence canonique principale
- le point de reprise

---

## Plan validé

1. Le chantier parent consumer devient le cadre de référence.
2. Le premier sous-chantier cadre le contrat minimal cible.
3. Les GO suivants pourront ensuite séparer :
   - implémentation producer côté `opt-trading`
   - adaptation consumer côté `LocalCMS`
   - fallback et transition
4. La continuité documentaire doit conserver :
   - le parent
   - le sous-chantier
   - la cible finale commune
   - le point de reprise

---

## ETABLI

- `opt-trading` porte déjà la spec canonique `memory_bricks`
- `LocalCMS` existe déjà comme consumer réel
- la spec V2 read-only n'est pas encore verrouillée par un consumer réel
- un chantier parent consumer manquait encore pour porter cette trajectoire
- le prochain pas logique est un cadrage de contrat, pas un patch technique immédiat

---

## Gap restant

- ouvrir le premier sous-chantier de contract alignment
- figer la matrice canon vs consumer
- décider le mode cible : V1 fichier, V2 HTTP, ou hybride avec fallback
- ordonner les GO techniques ultérieurs

---

## REPRISE

Lire ce document comme addendum de portée du chantier parent consumer.

Les sous-chantiers `memory_bricks` ↔ `LocalCMS` doivent désormais s'y rattacher explicitement.

---

## Structure minimale à reprendre (front matter)

```yaml
chantier_parent:
sous_chantier:
intention_parent:
cible_finale_parent:
objectif_sous_chantier:
go_id:
objectif_local_go:
cible_locale_go:
reference_canonique_principale:
point_de_reprise:
```
