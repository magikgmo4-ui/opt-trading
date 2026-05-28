---
go_id: GO_OPT_TRADING_REGISTRY_MODEL_P3_CLOSEOUT_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Clore la phase P3 du modele registry apres contrat source-of-truth, implementation minimale, decisions DeepSeek, raffinement `machine_target`, et rollout `placement_mode`.

## 3_INITIAL_NEED
Les lots P3 ont deja pose et applique l'essentiel du modele registry, mais la lecture globale reste dispersee entre plusieurs GOs. Ce closeout doit fixer l'etat canonique courant, les mutations appliquees, et le residuel reel sans rouvrir les decisions tranchees.

## 6_FINAL_TARGET
Un closeout doc-only qui fige l'etat courant du modele registry P3 et borne les seuls next GOs encore utiles.

## 12_INVARIANTS
- doc-only
- no registry mutation
- no runtime mutation
- no global index mutation
- no `secrets/`

## 16_TODO
- [x] Relire les GOs registry/DeepSeek/machine-target P3 merges
- [x] Synthesiser le modele canonique courant
- [ ] Verifier le scope doc-only

## 17_RESUME_POINT
Closeout P3 attendu: registry centrale prioritaire, DeepSeek student hors registries, `machine_target` conserve, `placement_mode` applique en deux batches, residuel reduit a `mimo_open_observer`.
