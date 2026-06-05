---
doc_id: GO_STRATEGY_KERNEL_SHARED_LAYER_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: trading
module: strategy_kernel
go_id: GO_STRATEGY_KERNEL_SHARED_LAYER_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - trading
  - strategy_kernel
  - audit
  - extensibility
surface: trading
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/ot/trading/23_STRATEGY_KERNEL_EXTENSIBILITY_AUDIT_01.md
  - docs/ot/trading/22_RANGE_STRATEGY_V1_STRUCT_01.md
  - docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md
---

# 00_cadrage — GO_STRATEGY_KERNEL_SHARED_LAYER_01

## Identité
- GO : GO_STRATEGY_KERNEL_SHARED_LAYER_01
- Repo : opt-trading
- Branche : sot/mainline
- Statut : active
- Type de travail : module durable documentaire / cadrage noyau stratégie partagé

## État de départ retenu
- l'intention produit et l'objectif final liés à `Range Strategy V1` sont déjà fixés dans la documentation précédente
- l'audit d'extensibilité du noyau stratégie montre que l'architecture est factorisable, mais que le code réel reste encore largement câblé XAU
- les modules source retenus pour ce constat sont `trading_lab_v1` et `trading_realtime_v1`

## Objectif du lot
- ouvrir le chantier canonique qui prépare une couche stratégie réellement partagée entre LAB et REALTIME
- transformer le constat d'audit en cadrage opératoire pour une migration future
- conserver le lien explicite entre intention produit, état réel du noyau, gap restant et next GO

## Non-objectifs
- implémenter immédiatement la couche stratégie partagée
- modifier le runtime ou ouvrir l'auto-trading
- ajouter une nouvelle stratégie opérationnelle complète dans ce lot

## Contexte utile
- l'architecture dual stack du repo impose déjà un noyau partagé de règles
- l'intention `range / fvg / breakout` a désormais besoin d'un support noyau plus générique que le câblage XAU actuel
- la méthode de session impose de documenter selon besoin initial, objectif final, plan validé, état établi, gap restant et next GO

## Critères PASS / FAIL
- PASS si : le chantier cadre clairement la future couche stratégie partagée et sépare les changements patchables des changements structurants
- FAIL si : le lot reste abstrait, ou mélange audit, implémentation et promesse produit

## Point de vigilance
- risque principal : basculer trop vite vers une refonte générale sans garder le lien avec l'état réel du code
- point d'arrêt acceptable : dossier chantier complet + ancre trading canonique + next GO unique

## RISKS

- À qualifier.
