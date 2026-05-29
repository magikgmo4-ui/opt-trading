---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_ARCHIVAL_CLEANUP_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Faire converger `mimo_open_observer` vers un etat archival/retired borne, sans suppression aveugle ni mutation registry prematuree.

## 3_INITIAL_NEED
Le GO precedent a clarifie que `mimo_open_observer` reste partiellement runnable mais strategiquement oriente fermeture/archive. Ce lot doit donc neutraliser les surfaces runtime encore actives par defaut, conserver les preuves utiles, et laisser un etat propre pour un futur retrait d'allowlist registry.

## 6_FINAL_TARGET
Les surfaces runtime/scheduler/wrappers `mimo_open_observer` ne se comportent plus comme une ligne active par defaut, et le module porte explicitement son statut archival.

## 12_INVARIANTS
- no registry mutation
- no global index mutation
- no placement_mode mutation
- no broad repo cleanup
- no unrelated scheduler/systemd mutation
- no `secrets/`

## 16_TODO
- [x] Auditer les surfaces runtime restantes
- [ ] Neutraliser les entrypoints actifs par defaut
- [ ] Documenter l'etat archival
- [ ] Verifier le lot

## 17_RESUME_POINT
Le cleanup doit conserver les preuves et assets, mais rendre explicite que `mimo_open_observer` n'est plus une ligne runtime active par defaut.
