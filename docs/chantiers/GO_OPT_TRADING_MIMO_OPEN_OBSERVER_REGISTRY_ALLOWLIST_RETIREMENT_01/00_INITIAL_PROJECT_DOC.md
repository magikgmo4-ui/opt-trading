---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_REGISTRY_ALLOWLIST_RETIREMENT_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-29
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Retirer `mimo_open_observer` de l'allowlist residuelle P3 maintenant que son etat archival/runtime est clarifie et borne.

## 3_INITIAL_NEED
Le module n'est plus une ligne active par defaut, mais son etat n'est plus ambigu: c'est un residu runnable borne cote `student`. Le registry peut donc cesser de le laisser en `machine_target:any` non qualifie.

## 6_FINAL_TARGET
`mimo_open_observer` ne depend plus de l'allowlist `machine_target:any` et dispose d'une lecture registry minimale compatible avec l'etat archival actuel.

## 12_INVARIANTS
- no secrets/
- no runtime mutation
- no global index mutation
- no wrapper/ui registry mutation
- no legacy/transitional rollout

## 16_TODO
- [x] Confirm allowlist retirement preconditions from archival cleanup
- [ ] Apply minimal registry + governance change
- [ ] Verify targeted governance tests

## 17_RESUME_POINT
Retire the last residual allowlist case by anchoring `mimo_open_observer` on `student` with an explicit placement read, without reopening broader registry design work.
