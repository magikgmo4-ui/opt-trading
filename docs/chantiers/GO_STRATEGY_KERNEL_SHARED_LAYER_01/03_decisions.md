---
doc_id: GO_STRATEGY_KERNEL_SHARED_LAYER_01_DECISIONS
doc_type: decision
repo: opt-trading
project: trading
module: strategy_kernel
go_id: GO_STRATEGY_KERNEL_SHARED_LAYER_01
status: active
lifecycle_stage: validation
topic_keys:
  - opt-trading
  - trading
  - strategy_kernel
  - decisions
surface: trading
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/ot/trading/23_STRATEGY_KERNEL_EXTENSIBILITY_AUDIT_01.md
  - docs/chantiers/GO_STRATEGY_KERNEL_SHARED_LAYER_01/00_cadrage.md
---

# 03_decisions — GO_STRATEGY_KERNEL_SHARED_LAYER_01

## Décision 1
- sujet : statut du noyau stratégie actuel
- option retenue : noyau factorisable en architecture, mais non encore générique dans le code réel
- raison du choix : le canon dual stack pousse vers le partage, alors que le code reste encore fortement câblé XAU
- impact : un lot structurant est justifié ; un simple patch cosmétique ne suffira pas

## Décision 2
- sujet : points d'extension réellement retenus
- option retenue : `Trader Frame`, `Feature Extractor`, `Variant Resolver`, `Event / Trade Projection`
- raison du choix : ce sont les couches effectivement identifiables dans le code repo-source actuel
- impact : elles servent désormais de grille canonique pour la future couche stratégie partagée

## Décision 3
- sujet : qualification des familles de stratégies
- option retenue :
  - proches du noyau actuel : `fvg`, `sweep`, `session_open`, `breakout` simple, `reclaim` simple
  - nécessitant une vraie extension : `range`, `mean_reversion`, `range + false breakout`, `range + reclaim`
- raison du choix : ces familles reflètent le différentiel réel entre ce que le code sait déjà faire et ce qu'il faudra ajouter
- impact : `range` n'est pas refusé, mais traité comme extension noyau explicite

## Décision 4
- sujet : passage multi-actifs
- option retenue : rendre injectables profils, symboles, strategy_id, variant space et sources de données
- raison du choix : les constantes et IDs XAU actuels bloquent la généricité réelle
- impact : première marche concrète vers un noyau multi-actifs

## Décision 5
- sujet : passage multi-stratégies
- option retenue : introduire une interface stratégie partagée et un registre minimal de stratégies
- raison du choix : la logique actuelle fusionne encore trop extraction, variante, signal, entrée et risque
- impact : prépare un noyau partagé LAB / REALTIME sans casser l'architecture dual stack existante

## Décision 6
- sujet : rôle des couches transverses globales
- option retenue : ne pas étendre `governance`, `index`, `master_pack`, `next`, `opportunities`, `product_targets` dans ce lot
- raison du choix : aucun nouveau fait transverse global n'a été établi au-delà du périmètre trading / noyau stratégie
- impact : le canon reste localisé dans `docs/ot/trading/` et `docs/chantiers/`

## RISKS

- À qualifier.
