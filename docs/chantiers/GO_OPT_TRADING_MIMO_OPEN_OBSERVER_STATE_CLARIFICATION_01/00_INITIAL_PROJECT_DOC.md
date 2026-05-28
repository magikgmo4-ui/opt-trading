---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_STATE_CLARIFICATION_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Clarifier l'etat reel de `mimo_open_observer` avant toute mutation registry ou suppression de l'allowlist residuelle P3.

## 3_INITIAL_NEED
`mimo_open_observer` reste le seul cas `machine_target:any` non qualifie. Le repo expose encore des signaux techniques de runtime/scheduler, mais certaines docs de consolidation le classent `CLOSED (student)` et recommandent l'archivage. Il faut donc trancher l'etat le plus fidele.

## 6_FINAL_TARGET
Une decision doc-only sur:
- le statut reel du module
- la nature du runtime restant
- le maintien ou non de l'allowlist
- le prochain GO utile

## 12_INVARIANTS
- doc-only
- no registry mutation
- no runtime mutation
- no scheduler/systemd mutation
- no global index mutation
- no `secrets/`

## 16_TODO
- [x] Auditer preuves registry/runtime/docs historiques
- [x] Clarifier l'etat le plus fidele
- [ ] Verifier le scope doc-only

## 17_RESUME_POINT
Trancher si `mimo_open_observer` est encore un module actif qualifiable, ou un cas suffisamment ambigu/heritage pour rester temporairement en allowlist jusqu'a cleanup ou archival explicite.
