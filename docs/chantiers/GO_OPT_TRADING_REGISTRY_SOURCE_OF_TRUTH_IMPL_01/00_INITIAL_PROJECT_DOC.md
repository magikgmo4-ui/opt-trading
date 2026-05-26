---
go_id: GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_IMPL_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Appliquer le contrat source-of-truth registry dans les readers et checks minimaux, sans mutation runtime ni mutation des registries centrales.

## 3_INITIAL_NEED
Le contrat documentaire est merge, mais les readers n'exposent pas encore clairement leur nature canonique, et le fallback `ui_registry_seed.json` n'est pas signale explicitement comme mode degrade.

## 6_FINAL_TARGET
Les readers centraux indiquent clairement quand ils lisent une source canonique ou un fallback, et des tests verrouillent ce comportement.

## 12_INVARIANTS
- no registry mutation
- no runtime mutation
- no global index mutation
- no `secrets/`

## 16_TODO
- [x] Cadrer l'impl minimale depuis le contrat merge
- [ ] Impl reader/source metadata + fallback signaling
- [ ] Ajouter tests cibles
- [ ] Verifier le lot

## 17_RESUME_POINT
Impl minimale concentree sur les readers et le fallback UI seed, sans etendre encore le modele `legacy/transitional` ni `machine_target`.
