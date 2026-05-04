---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01_NEXT_GO
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 50_NEXT_GO_DECISION — Desk Pro Runtime Review

## Verdict

**PASS** — Desk Pro est operationnel. Runner OK, mode PAPER, dernier run SUCCESS. desk_bridge et macro-xau sont des problemes peripheriques non bloquants.

## Resume

- **Desk Pro runner**: OK (PAPER mode, orchestrator + dashboard disponibles)
- **38 runs historiques**: tous SUCCESS
- **Dernier run**: 2026-04-05 (OK: 11, Failed: 0)
- **/shared/desk_pro/latest/**: 5 fichiers, ~1 mois (stale mais valides)
- **desk_bridge**: FAIL (inputs corrompus, pas un bug pipeline)
- **macro-xau**: OBSOLETE (timer actif, module absent)

## Prochain GO recommande (P1)

### GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01

**Objectif**: Nettoyer les inputs corrompus et deverrouiller le pipeline Vision -> Desk.

Priorite: Desk Pro core est stable. Le blocage principal est le pipeline vision/desk_bridge qui empeche l'analyse de screenshots. Ce GO nettoie les inputs, ajoute une garde, et relance.

**Actions**:
1. Supprimer les 9 fichiers 0-byte de /shared/vision_inbox/
2. Supprimer ou renommer les 5 .uploading partiels
3. Ajouter une garde `[ -s "$file" ]` dans bridge_vision_to_desk_inbox.sh
4. Relancer desk_bridge (sudo systemctl start desk_bridge.service)
5. Verifier que le pipeline Vision -> Desk est deverrouille
6. Desactiver macro-xau.timer (sudo systemctl disable --now macro-xau.timer)

**Ne pas faire**:
- Ne pas modifier Desk Pro core
- Ne pas modifier webhook/perf
- Ne pas supprimer le service macro-xau (disable seulement)

## Prochains GO (dans l'ordre)

### P1: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01
Nettoyer vision_inbox, deverrouiller desk_bridge, cleanup macro-xau timer

### P2: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01
Lancer un run Desk Pro frais (smoke test), verifier pipeline complet
- cmd-desk_pro_runner run (mode PAPER)
- Verifier sorties dans /shared/desk_pro/latest/
- Valider dashboard_latest.html genere

### P3: GO_OPT_TRADING_ADMIN_TRADING_FAILED_SERVICES_TRIAGE_01
Triage complet des services (macro-xau, desk_bridge, timers desactives)
- Cleanup final macro-xau (disable service + timer)
- Verifier trading-heartbeat, bot_vision_step2_send

### P4: GO_OPT_TRADING_ADMIN_TRADING_OPENCLAW_INTEGRATION_01 (FUTUR)
Integration OpenClaw sur admin-trading. DIFFERE.

## Decision

- Desk Pro est sain, le probleme principal est le pipeline Vision bloque par des inputs corrompus
- Priorite: deverrouiller Vision avant de relancer Desk Pro
- macro-xau doit etre desactive (pas supprime)
