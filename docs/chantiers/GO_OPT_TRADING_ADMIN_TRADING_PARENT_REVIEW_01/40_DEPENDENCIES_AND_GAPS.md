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
| db-layer | /shared via SSHFS | SSHFS | DOWN (admin-trading unreachable) |
| student | /shared via SSHFS | SSHFS | DOWN |
| cursor-ai | SFTP vision_inbox | SFTP | DOWN |
| cursor-ai | SSH | SSH | DOWN (banner timeout) |
| db-layer | WireGuard | WG | STALE (2+ jours) |
| student | WireGuard | WG | Probablement stale |
| cursor-ai | WireGuard | WG | Probablement stale |

### admin-trading depend de

| Service | Fournisseur | Etat |
| --- | --- | --- |
| TradingView | Internet (ngrok) | Inconnu |
| Telegram Bot API | Internet | Inconnu |
| reseau_ssh | modules/reseau_ssh | OK (repo-side) |

## Gaps identifies

### GAP-01: Connectivite physique (CRITIQUE)

- **Symptome**: admin-trading unreachable sur toutes les routes
- **Impact**: Aucun controle runtime possible, /shared down, WG down
- **Cause probable**: Daemon SSH bloque, machine en etat degrade
- **Action**: Retablir acces physique/console, redemarrer si necessaire

### GAP-02: Tunnel WireGuard (CRITIQUE)

- **Symptome**: Handshake stale 2+ jours depuis db-layer
- **Impact**: Pas de connectivite VPN entre machines
- **Cause probable**: admin-trading down ou service WG arrete
- **Action**: Verifier et relancer wg-quick apres retablissement admin-trading

### GAP-03: /shared non disponible (HAUT)

- **Symptome**: /shared vide sur db-layer
- **Impact**: Pas de donnees Desk Pro visibles sur db-layer/student
- **Cause**: admin-trading unreachable = serveur SFTP down
- **Action**: Retablir admin-trading, verifier shared_files_sftp, remonter SSHFS

### GAP-04: Etat runtime inconnu (HAUT)

- **Symptome**: Aucun controle service/processus/port possible
- **Impact**: Impossible de savoir ce qui tourne ou non
- **Action**: Apres retablissement SSH, auditer systemd, processus, ports

### GAP-05: tv-webhook etat inconnu (HAUT)

- **Symptome**: Service webhook non verifiable
- **Impact**: Impossible de savoir si le flux TradingView est operationnel
- **Action**: Verifier systemctl status tv-webhook, ports, logs

### GAP-06: Vision/ShareX pipeline (MEDIUM)

- **Symptome**: SFTP probablement down
- **Impact**: Captures ShareX non traitees
- **Action**: Verifier vision_bot et bot_vision_step2 apres retablissement

### GAP-07: Telegram alerts (MEDIUM)

- **Symptome**: Pas de visibilite sur les alertes Telegram
- **Impact**: Pas de monitoring trading actif
- **Action**: Verifier logs webhook/perf pour alertes ratees

### GAP-08: Tokens / .env (DOCUMENTATION SEULEMENT)

- **Symptome**: Fichiers .env et tokens existent mais ne doivent pas etre affiches
- **Impact**: Aucun (bonne pratique)
- **Action**: Lister les fichiers sans contenu, verifier leur presence

### GAP-09: OpenClaw absent sur admin-trading (ATTENDU)

- **Symptome**: Aucune reference OpenClaw sur admin-trading
- **Impact**: Aucun (conformement au plan)
- **Note**: OpenClaw principal est sur db-layer (127.0.0.1:18789), lab sur student (127.0.0.1:18790)

### GAP-10: Etat cron / timers systemd (FAIBLE)

- **Symptome**: Non verifiable
- **Impact**: Peut affecter les taches planifiees (Desk Pro, retention, etc.)
- **Action**: Verifier systemctl list-timers apres retablissement
