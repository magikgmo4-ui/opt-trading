---
doc_id: OPT_TRADING_MULTI_AGENTS_TRANSITIONAL_GLOBAL_INDEXATION_METHOD_01
doc_type: method
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: method
topic_keys:
  - opt-trading
  - multi_agents
  - indexation
  - go_index
  - active_streams
  - next_go_candidates
  - reprise
  - git_friction
  - transition_method
search_tags:
  - surface:chantier
  - doc_role:method
  - governance:indexation
  - governance:transition_method
  - git:friction_reduction
  - index:go_index
  - index:active_streams
  - index:next_go_candidates
  - index:reprise
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Appliquer la méthode transitoire avant toute modification directe des index globaux volumineux"
updated_at: 2026-04-26
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/GAP_INDEXATION.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/05_OPERATIONAL_MATRIX_INTEGRATION_PLAN.md
---

# 07_TRANSITIONAL_GLOBAL_INDEXATION_METHOD — Méthode transitoire pour index globaux

## 1. Problème établi

Les fichiers suivants sont nécessaires à la continuité globale, mais ils créent de la friction Git :

- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/REPRISE.md`

Deux problèmes sont établis :

1. presque tous les chantiers doivent les toucher, peu importe leur nature ;
2. ces fichiers sont volumineux, donc difficiles à modifier proprement via connecteur ou interface distante sans risque de troncature, conflit ou remplacement excessif.

Conclusion : les index globaux restent canoniques, mais ne doivent pas être patchés à chaud par tous les chantiers.

## 2. Objectif de la méthode transitoire

Réduire les conflits Git et la friction opérationnelle sans abandonner la continuité globale.

La méthode transitoire doit permettre :

- d'ouvrir un chantier proprement ;
- de documenter son indexation attendue localement ;
- de différer la propagation globale ;
- de consolider les index globaux par lots dédiés ;
- d'éviter les modifications concurrentes sur les mêmes fichiers volumineux.

## 3. Principe retenu

Chaque chantier documente son indexation localement.

Les index globaux sont mis à jour uniquement par lot d'agrégation contrôlé.

Modèle :

```text
chantier local -> INDEX_PATCH / GAP_INDEXATION local -> lot agrégateur -> index globaux
```

## 4. Surfaces locales à utiliser

Pour chaque chantier parent ou GO significatif, ajouter dans `docs/chantiers/<GO_ID>/` :

```text
INDEX_PATCH.md
```

ou, si la propagation n'est pas encore prête :

```text
GAP_INDEXATION.md
```

### 4.1 INDEX_PATCH.md

À utiliser quand l'entrée globale est prête et structurée.

Contenu minimal :

- entrée proposée pour `GO_INDEX.md` ;
- entrée proposée pour `ACTIVE_STREAMS.md` si actif ;
- entrée proposée pour `NEXT_GO_CANDIDATES.md` si parent actif ;
- entrée proposée pour `REPRISE.md` si point de reprise utile ;
- statut de propagation : `TODO`, `APPLIED`, `SUPERSEDED`.

### 4.2 GAP_INDEXATION.md

À utiliser quand il y a un écart explicite ou un blocage de propagation.

Contenu minimal :

- ce qui devrait être propagé ;
- pourquoi ce n'est pas encore propagé ;
- risque Git ou risque de troncature ;
- prochaine action ;
- surface globale concernée.

## 5. Règle de non-friction

Un chantier ne doit pas modifier directement les quatre index globaux si :

- le fichier est volumineux ;
- le connecteur retourne du contenu tronqué ;
- plusieurs branches actives touchent déjà la même surface ;
- la modification peut être exprimée proprement dans un `INDEX_PATCH.md` local ;
- l'urgence opérationnelle ne justifie pas la propagation immédiate.

Dans ces cas, le chantier doit créer ou mettre à jour son `INDEX_PATCH.md` / `GAP_INDEXATION.md` local.

## 6. Rôle futur d'un lot agrégateur

Créer périodiquement un GO dédié, par exemple :

```text
GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01
```

Rôle :

- lire tous les `docs/chantiers/*/INDEX_PATCH.md` ;
- lire tous les `docs/chantiers/*/GAP_INDEXATION.md` ;
- appliquer les entrées dans les quatre index globaux ;
- résoudre les doublons ;
- fermer les gaps appliqués ;
- produire un closeout d'indexation.

## 7. Statuts proposés

Pour chaque entrée locale :

| Statut | Sens |
| --- | --- |
| `TODO` | à propager dans les index globaux |
| `READY` | entrée prête, validée localement |
| `APPLIED` | propagée dans les index globaux |
| `SUPERSEDED` | remplacée par une autre entrée |
| `BLOCKED` | propagation bloquée par conflit, troncature ou décision manquante |

## 8. Règle pour les quatre index globaux

### 8.1 `GO_INDEX.md`

Reste la vérité globale de liste.

Mais il ne doit être patché que :

- par lot agrégateur ;
- ou par chantier très court et non concurrent ;
- ou en local, avec fichier complet disponible et diff contrôlé.

### 8.2 `ACTIVE_STREAMS.md`

Reste la vue des flux actifs.

Mais l'ajout d'un nouveau flux peut d'abord être documenté dans `INDEX_PATCH.md` local.

### 8.3 `NEXT_GO_CANDIDATES.md`

Reste la matrice parent actif -> next GO primaire.

Mais un nouveau parent peut d'abord exposer son next dans son `INDEX_PATCH.md` local.

### 8.4 `REPRISE.md`

Reste support de reprise opératoire.

Mais la reprise locale d'un chantier doit d'abord vivre dans son propre dossier, puis être agrégée.

## 9. Avantages

- moins de conflits Git ;
- moins de remplacements massifs ;
- meilleure lisibilité par chantier ;
- possibilité de review locale ;
- propagation globale contrôlée ;
- compatible avec connecteurs limités ;
- compatible avec travail multi-agents.

## 10. Risques

- l'index global peut temporairement être en retard ;
- il faut un rituel d'agrégation ;
- les chantiers doivent être disciplinés sur `INDEX_PATCH.md` / `GAP_INDEXATION.md` ;
- les statuts locaux doivent être fermés après application.

## 11. Invariants

- les index globaux restent canoniques ;
- les patchs locaux ne remplacent pas les index globaux ;
- un `INDEX_PATCH.md` n'est pas une source souveraine permanente ;
- un `GAP_INDEXATION.md` doit être résolu ou maintenu explicitement ;
- la propagation globale doit être prouvée par diff et closeout.

## 12. Application au chantier courant

Pour `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` :

- `GAP_INDEXATION.md` existe déjà ;
- il documente les entrées attendues pour les quatre index ;
- la propagation globale directe est volontairement reportée ;
- la prochaine étape recommandée est de transformer `GAP_INDEXATION.md` en `INDEX_PATCH.md` prêt à appliquer, ou de créer un lot agrégateur.

## 13. Décision proposée

Adopter transitoirement cette règle :

```text
Aucun chantier ne modifie les quatre index globaux directement sauf nécessité forte.
Chaque chantier produit d'abord son INDEX_PATCH.md ou GAP_INDEXATION.md local.
Les index globaux sont mis à jour par lots d'agrégation dédiés.
```

## 14. Prochain GO recommandé

```text
GO_OPT_TRADING_INDEX_AGGREGATION_METHOD_01
```

Objectif : canoniser cette méthode au-delà du chantier multi-agents, puis créer le premier batch d'agrégation si nécessaire.

## 15. Point de reprise

Reprendre ici avant toute modification directe de :

- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/REPRISE.md`
