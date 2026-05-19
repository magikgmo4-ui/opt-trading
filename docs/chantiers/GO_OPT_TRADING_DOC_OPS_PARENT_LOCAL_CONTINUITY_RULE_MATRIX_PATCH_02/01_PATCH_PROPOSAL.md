---
doc_id: GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02_PATCH_PROPOSAL
doc_type: patch_proposal
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02
status: draft
lifecycle_stage: patch_proposal
topic_keys:
  - opt-trading
  - matrix_patch
  - local_continuity
  - index_inbox
surface: chantier
source_kind: canonical_candidate
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Apply proposed blocks into master matrix after local rebase"
updated_at: 2026-04-30
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01.md
---

# PATCH PROPOSAL — intégrer la règle dans la matrice

## Objectif

Ajouter dans `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` la règle de continuité locale des parents.

## Bloc cible recommandé — Partie 8

Insérer après `### 8.2 Frontieres minimales` ou après `### 8.3 Surfaces proches pertinentes mais non souveraines` :

```md
### 8.4 Continuité locale des parents et indexation différée

Pour tout nouveau chantier parent, la continuité courante doit être conservée prioritairement dans :

`docs/chantiers/<GO_PARENT>/`

Le dossier parent porte le cadrage, le plan ou état courant, les décisions locales, les gaps, les TODO et le point de reprise.

Une entrée courte atomique doit être créée dans :

`docs/index/inbox/<GO_PARENT>.md`

Cette entrée sert de tampon d'agrégation future.

Les index globaux ne doivent pas être modifiés à chaque micro-avancement. Ils sont modifiés seulement si :
- le parent devient officiellement actif dans la liste globale ;
- le parent est fermé ;
- le statut global change ;
- le next GO global change ;
- un batch explicite d'agrégation d'index est ouvert ;
- un arbitrage branche significatif l'exige.

Effet :
- chaque parent reste autonome pour la reprise ;
- les gros index globaux restent lisibles ;
- l'agrégation globale devient un acte séparé et contrôlé ;
- `docs/index/inbox/` évite de remplacer les index globaux par un journal de session.
```

## Bloc cible recommandé — Partie 10

Ajuster `### 10.1 Ouverture parent` :

```md
Propagation minimale d'ouverture :
- dossier chantier parent ;
- entrée atomique `docs/index/inbox/<GO_PARENT>.md` ;
- `GO_INDEX.md` seulement si le parent doit entrer immédiatement dans la liste globale ;
- `NEXT_GO_CANDIDATES.md` seulement si le parent devient priorite active globale ;
- `ACTIVE_STREAMS.md` seulement si le flux devient reellement actif globalement ;
- `REPRISE.md` seulement si un point de pilotage global est necessaire ;
- `BRANCH_STATE.md` seulement si une branche dediee significative est ouverte ou arbitree.
```

## Bloc cible recommandé — Partie 10.5

Compléter `### 10.5 Regle de propagation` :

```md
La propagation globale n'est pas obligatoire pour chaque micro-avancement local.

Par défaut, les évolutions locales restent dans le dossier parent `docs/chantiers/<GO_PARENT>/`.

L'entrée `docs/index/inbox/<GO_PARENT>.md` sert de trace courte en attente d'un batch d'agrégation.

Les index globaux sont réservés aux changements structurels, aux fermetures, aux ouvertures significatives, aux changements de statut global, aux changements de next GO global et aux batchs d'agrégation.
```

## Critère PASS

- La matrice contient explicitement la règle `parent local continuity + inbox + index global batch`.
- Les index globaux ne sont plus décrits comme obligatoires à chaque ouverture locale.
- La règle reste compatible avec les obligations de propagation lors d'une fermeture ou d'un changement global réel.

## Critère FAIL

- La matrice continue d'obliger `GO_INDEX.md` / `ACTIVE_STREAMS.md` / `REPRISE.md` pour chaque micro-avancement.
- L'inbox est absente.
- Le dossier parent n'est pas reconnu comme surface de continuité locale.
