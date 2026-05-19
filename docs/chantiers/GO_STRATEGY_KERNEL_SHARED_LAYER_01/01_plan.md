---
doc_id: GO_STRATEGY_KERNEL_SHARED_LAYER_01_PLAN
doc_type: chantier_plan
repo: opt-trading
project: trading
module: strategy_kernel
go_id: GO_STRATEGY_KERNEL_SHARED_LAYER_01
status: active
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - trading
  - strategy_kernel
  - plan
surface: trading
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/chantiers/GO_STRATEGY_KERNEL_SHARED_LAYER_01/00_cadrage.md
  - docs/ot/trading/23_STRATEGY_KERNEL_EXTENSIBILITY_AUDIT_01.md
---

# 01_plan — GO_STRATEGY_KERNEL_SHARED_LAYER_01

## But du plan
- but : transformer l'audit d'extensibilité en plan de cadrage opératoire pour un noyau stratégie partagé
- ordre d'exécution retenu : cadrage -> plan -> journal technique -> décisions -> closeout

## Étapes
1. figer l'état réel du noyau actuel LAB / REALTIME
2. séparer les points d'extension réellement présents
3. distinguer ce qui est patchable de ce qui est structurant
4. expliciter ce qu'un noyau partagé devra porter pour `range`, `fvg`, `breakout`
5. fermer le lot avec un next GO unique vers la couche stratégie partagée

## Zones de travail retenues
- `modules/trading_lab_v1/app/trading_lab_v1.py`
- `modules/trading_realtime_v1/app/runtime_loop_v1.py`
- `modules/trading_realtime_v1/app/guardrails_v1.py`
- `docs/ot/trading/23_STRATEGY_KERNEL_EXTENSIBILITY_AUDIT_01.md`

## Validations prévues
- cohérence entre l'audit, le dossier chantier et l'intention produit déjà figée
- séparation explicite entre état établi et migration future
- présence d'un next GO unique

## Risques
- risque : dériver vers une refonte générale sans hiérarchie des changements
- mitigation : distinguer patch local, extension noyau et lot structurant

## Point d'arrêt acceptable
- arrêt acceptable si : le chantier qualifie clairement le noyau actuel, ses limites et la prochaine couche partagée à ouvrir
