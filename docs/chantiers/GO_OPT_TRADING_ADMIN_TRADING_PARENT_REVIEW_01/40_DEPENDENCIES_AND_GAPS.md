---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01_DEPS_GAPS
doc_type: dependencies_gaps
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_DEPENDENCIES_AND_GAPS — admin-trading

## Dependances inter-machines

### admin-trading est fournisseur pour

| Machine | Service | Protocole | Etat |
| --- | --- | --- | --- |
| db-layer | /shared via SSHFS | SSHFS | OK (admin-trading accessible) |
| student | /shared via SSHFS | SSHFS | OK |
| cursor-ai | SFTP vision_inbox | SFTP | OK |
| cursor-ai | SSH | SSH | OK |
| db-layer | WireGuard | WG | OK (handshake < 2 min) |
| student | WireGuard | WG | OK (handshake < 2 min) |
| cursor-ai | WireGuard | WG | OK (handshake < 2 min) |

### admin-trading depend de

| Service | Fournisseur | Etat |
| --- | --- | --- |
| TradingView | Internet (ngrok) | OK (ngrok actif) |
| Telegram Bot API | Internet | OK (webhook/perf utilisent Telegram) |

## Gaps identifies

### GAP-01: desk_bridge.service — FAILED (FAIBLE)

- **Symptome**: Service failed sur image corrompue screen_2026-03-06
- **Impact**: Bridge vision -> desk inbox bloque sur cette entree
- **Action**: Supprimer les images 0-byte dans vision_inbox, relancer ou ignorer

### GAP-02: macro-xau.service — FAILED (FAIBLE)

- **Symptome**: /opt/trading/jobs/macro_xau/run.sh absent
- **Impact**: Module macro XAU non deploye, service ne peut pas demarrer
- **Action**: Creer le module ou desactiver le service

### GAP-03: vision_inbox — fichiers 0-byte (FAIBLE)

- **Symptome**: 6 fichiers screen_*.png a 0 octet (mars 2026)
- **Impact**: Peut bloquer desk_bridge ou vision_bot
- **Action**: Nettoyer les fichiers 0-byte

### GAP-04: Desk Pro — dernier run 2026-04-05 (MEDIUM)

- **Symptome**: Derniere execution Desk Pro il y a ~1 mois
- **Impact**: Donnees trading non fraiches
- **Action**: Relancer desk_pro_runner ou verifier si automatise

### GAP-05: trading-heartbeat — disabled (MEDIUM)

- **Symptome**: Service et timer desactives
- **Impact**: Pas de heartbeat monitoring
- **Action**: Reactiver si necessaire, sinon documenter comme obsoleted

### GAP-06: bot_vision_step2_send.timer — disabled (MEDIUM)

- **Symptome**: Timer envoi Telegram desactive
- **Impact**: Pas d'envoi automatique des analyses vision
- **Action**: Reactiver si necessaire

### GAP-07: perf.service — masked (FAIBLE)

- **Symptome**: Service perf.service masque, remplace par tv-perf.service
- **Impact**: Aucun (tv-perf assure le meme role)
- **Action**: Documenter, laisser en l'etat

### GAP-08: OpenClaw absent (ATTENDU)

- **Symptome**: Aucun binaire openclaw, pas de gateway 18789/18790
- **Impact**: Aucun (conformement au plan)
- **Note**: OpenCode 1.4.2 est installe (127.0.0.1:4096) mais n'est pas OpenClaw

### GAP-09: Pas de tmux sessions (OBSERVATION)

- **Symptome**: Aucune session tmux active
- **Impact**: Pas de monitoring temps reel visible, services tournent en systemd direct

### GAP-10: Repo local — modifications unstaged (FAIBLE)

- **Symptome**: GO_INDEX, ACTIVE_STREAMS, REPRISE modifies + fichiers supprimes
- **Impact**: Divergence potentielle avec origin/sot/mainline
- **Action**: Verifier l'etat, commit ou discard selon la politique
