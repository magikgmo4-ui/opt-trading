---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_IMPL_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Appliquer un premier lot compatible du modele `machine_target + placement_mode` sans casser les readers existants ni lancer de rewrite massif de registry.

## 3_INITIAL_NEED
Le modele parent est merge, mais les registries et readers n'exposent pas encore `placement_mode`. Un premier lot cible doit donc enrichir les entrees `machine_target: any` les moins ambigues et ajouter des garde-fous de gouvernance.

## 6_FINAL_TARGET
`placement_mode` existe comme champ optionnel sur un premier batch borne d'entrees modules, le reader modules l'affiche, et des tests de gouvernance verrouillent le contrat minimal.

## 12_INVARIANTS
- no secrets/
- no runtime mutation
- no global index mutation
- no full registry rewrite
- no machine_targets matrix
- no legacy/transitional rollout

## 16_TODO
- [x] Auditer les entrees `machine_target:any` candidates
- [ ] Appliquer le premier batch `placement_mode`
- [ ] Mettre a jour reader et tests
- [ ] Verifier le lot

## 17_RESUME_POINT
Premier batch cible: readers registry, `registry_router`, et facades/bridges OpenClaw les plus explicites.
