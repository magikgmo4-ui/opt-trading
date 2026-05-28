---
go_id: GO_OPT_TRADING_PLACEMENT_MODE_ROLLOUT_BATCH_02
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Traiter le second batch des entrees `machine_target:any` explictement differees, sans rewrite massif du registry et sans casser le modele `machine_target + placement_mode` deja en place.

## 3_INITIAL_NEED
Le batch 01 a introduit `placement_mode` et reduit une partie des `any` ambigus. Il reste quatre entrees differees qui demandent une lecture plus fine: `mimo_open_observer`, `shared_sshfs_permanent`, `shared`, `reseau_ssh`.

## 6_FINAL_TARGET
Qualifier les cas suffisamment prouvables et resserrer l'allowlist residuelle au minimum strictement justifie.

## 12_INVARIANTS
- no secrets/
- no runtime mutation
- no global index mutation
- no full registry rewrite
- no machine_targets matrix
- no legacy/transitional rollout
- no mutation hors `registry/modules_registry.yaml`, `tests/governance/test_machine_target_model_impl.py`, et docs chantier

## 16_TODO
- [x] Auditer les quatre entrees differees
- [ ] Appliquer les choix batch 02
- [ ] Resserrer tests/allowlist
- [ ] Verifier le lot

## 17_RESUME_POINT
Batch 02 vise un resserrement utile, pas l'elimination forcee de toute incertitude residuelle.
