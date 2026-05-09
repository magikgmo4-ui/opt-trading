---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01_SAFETY
doc_type: safety_gates_and_rollback
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 50_SAFETY_GATES_AND_ROLLBACK - Safety Gates and Rollback

## Safety gates

1. **Dry-run obligatoire** pour toute premiere implementation
2. **No-trade semantics** explicites: aucune execution, aucun ordre, aucun ledger live
3. **No Telegram** tant qu'un GO separe ne l'autorise pas
4. **Aucun webhook reel** pendant la phase automation dry-run
5. **Aucun `systemctl enable/start`** avant validation du GO timer spec puis timer impl
6. **Logs sans secrets** et sans dump de payload sensible
7. **Controle Git propre** avant chaque patch runtime
8. **Tolerance stale** documentee, pas de faux positif de succes

## Rollback attendu pour phases futures

### Rollback code

- revert du GO d'implementation dry-run si comportement non conforme

### Rollback timer/service

- stop timer
- disable timer
- retirer unit files du GO timer impl
- verifier que les outputs stale ne sont plus regeneres

### Rollback fonctionnel

- revenir au mode manuel actuel
- conserver `desk_snapshot` et les tests existants comme preuves de reference

## Desactivation rapide cible

Le futur design doit permettre une coupure rapide par une seule action operateur: arret du timer ou execution manuelle retiree, sans impact sur webhook, desk_bridge ou capture.
