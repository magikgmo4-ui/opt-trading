---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_REFINEMENT_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Raffiner le modele `machine_target` apres les closeouts P2 et le contrat registry source-of-truth, sans casser la compatibilite du schema actuel.

## 3_INITIAL_NEED
Le champ `machine_target` reste utile mais trop grossier pour distinguer correctement surface operateur, runtime reel, facade, shim de compatibilite, et diffusion cross-machine. Plusieurs lots ont utilise `any` comme approximation de secours, ce qui masque des topologies reelles.

## 6_FINAL_TARGET
Un modele doc-only qui conserve `machine_target` comme axe primaire compatible, mais precise quand il faut l'enrichir via une deuxieme dimension plutot que de surcharger `any`.

## 12_INVARIANTS
- doc-only
- no registry mutation
- no runtime mutation
- no global index mutation
- no `secrets/`

## 16_TODO
- [x] Auditer l'usage actuel de `machine_target`
- [x] Definir le modele raffine compatible
- [ ] Verifier le scope doc-only

## 17_RESUME_POINT
Conserver `machine_target` comme cible primaire simple, mais deplacer les besoins cross-machine et de placement dans une dimension complementaire explicite.
