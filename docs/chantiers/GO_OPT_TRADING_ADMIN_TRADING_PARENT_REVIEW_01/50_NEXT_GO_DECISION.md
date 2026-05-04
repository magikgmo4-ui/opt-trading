---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01_NEXT_GO
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 50_NEXT_GO_DECISION — admin-trading

## Verdict

**PASS** — admin-trading est accessible et operationnel. Audit read-only complet termine.

## Resume de l'etat reel

- **5 services actifs**: tv-webhook (8000), tv-perf (8010), vision_bot, bot_vision_step2, ngrok
- **2 services failed non bloquants**: desk_bridge (image corrompue), macro-xau (module manquant)
- **WireGuard**: operationnel, tous les peers connectes (< 2 min handshake)
- **/shared**: operationnel, SFTP + SSHFS fonctionnels
- **Desk Pro**: dernier run 2026-04-05 (SUCCESS), donnees presentes dans /shared/desk_pro/latest/
- **OpenCode 1.4.2**: installe (127.0.0.1:4096), pas OpenClaw
- **40+ wrappers**: installes dans /usr/local/bin

## Prochain GO recommande (P1)

### GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01

Recommandation: auditer le pipeline Desk Pro comme premier chantier runtime.

Justification:
- Desk Pro est le coeur metier trading
- Dernier run il y a ~1 mois, a verifier
- Services webhook/perf sont actifs et stables
- Les services failed sont non bloquants

**Objectif**:
- Verifier l'etat du pipeline Desk Pro (probability -> decision -> risk -> position)
- Lancer un dry-run ou status check
- Verifier les sorties dans /shared/desk_pro/latest/
- Tester cmd-desk_pro_runner status
- Cartographier les modules manquants ou obsoletes
- Ne pas modifier le runtime sans GO dedie

## Prochains GO (dans l'ordre)

### P1: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01
Pipeline Desk Pro runtime review

### P2: GO_OPT_TRADING_ADMIN_TRADING_FAILED_SERVICES_TRIAGE_01
Trier les 2 services failed :
- desk_bridge: nettoyer images 0-byte, relancer
- macro-xau: creer module ou desactiver service

### P2: GO_OPT_TRADING_ADMIN_TRADING_TIMERS_RESTORE_01
Reviser les timers desactives :
- trading-heartbeat (disabled)
- bot_vision_step2_send (disabled)

### P3: GO_OPT_TRADING_ADMIN_TRADING_OPENCLAW_INTEGRATION_01 (FUTUR)
Integration OpenClaw sur admin-trading pour runtime trading.
NE PAS OUVRIR avant stabilisation Desk Pro.

## Decisions

- admin-trading est operationnel et stable
- Le coeur runtime (webhook + perf) tourne normalement
- Aucun service critique n'est down
- Les failed sont non bloquants
- Prochaine etape logique: audit Desk Pro
