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

**FAIL CONTROLE** — admin-trading est unreachable. L'audit read-only a atteint sa limite observable.

## Raison

- TCP handshake OK mais banner SSH timeout = machine allumee mais SSH bloque
- Depuis db-layer = "No route to host"
- WireGuard handshake stale 2+ jours
- Aucun controle runtime possible
- Cartographie realisee uniquement sur base repo/registres

## Ce qui a ete accompli

- Index canoniques lus et recroises
- Chantier parent ADMIN_TRADING_PARENT_01 lu (3 fichiers)
- Repo scanne integralement (git grep) -> cartographie complete des references
- Registres lus (machines_registry, modules_registry, ui_surfaces_registry, wrappers_registry)
- Tentative SSH multi-chemins (LAN, VPN, WG tunnel, jump host)
- Diagnostic connectivite croisee (db-layer, student, fantome)
- Cartographie des 18 surfaces trading referencees
- 10 gaps documentes

## Prochain GO recommande (P0)

### GO_OPT_TRADING_ADMIN_TRADING_MACHINE_RECOVERY_01

**Objectif**: Retablir la connectivite admin-trading avant tout audit runtime.

**Actions**:
1. Acces physique ou console a la machine admin-trading
2. Diagnostiquer etat daemon SSH (bloque? surcharge?)
3. Redemarrer si necessaire
4. Verifier connectivite reseau LAN (192.168.0.111)
5. Relancer WireGuard (wg-quick up wg0, wg-quick up wg-mgmt)
6. Verifier SSH operationnel
7. Verifier connectivite depuis db-layer et cursor-ai

**Conditions de succes**:
- SSH admin-trading fonctionnel
- WireGuard handshake < 1 minute
- Ping admin-trading depuis db-layer OK

## Prochains GO apres recovery (dans l'ordre)

### P1: GO_OPT_TRADING_ADMIN_TRADING_RUNTIME_AUDIT_01

Auditer l'etat runtime reel une fois la machine accessible :
- Services systemd (status, enabled/disabled)
- Processus actifs
- Ports en ecoute
- Tmux sessions
- Verifier tv-webhook, perf, Desk Pro, vision_bot
- Distinguer actif / arrete / obsoleted

### P2: GO_OPT_TRADING_ADMIN_TRADING_SERVICE_RESTORE_01

Si des services sont arretes :
- Relancer tv-webhook.service
- Relancer vision_bot
- Verifier ngrok
- Retablir /shared (SFTP + SSHFS mounts)

### P3: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01

Review ciblee Desk Pro :
- Verifier pipeline probability -> decision -> risk -> position
- Verifier /shared/desk_pro/latest/
- Tester desk_pro_cmd.sh status

### P4: GO_OPT_TRADING_ADMIN_TRADING_OPENCLAW_INTEGRATION_01 (FUTUR)

Integration OpenClaw sur admin-trading pour le runtime trading.
NE PAS OUVRIR avant stabilisation complete de la machine.

## Decision

- admin-trading doit etre retabli avant toute autre action
- Aucun GO runtime trading ne peut etre ouvert sans SSH fonctionnel
- Les 18 surfaces referencees dans les registres sont documentees et pretes pour l'audit
- La cartographie repo-side est complete
