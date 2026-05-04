---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01_MACHINE_STATE
doc_type: machine_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_MACHINE_STATE — admin-trading

## Identite reelle

| Champ | Valeur |
| --- | --- |
| Hostname | admin-trading |
| IP LAN | 192.168.0.111 |
| IP VPN (WireGuard wg0) | 10.8.0.1 |
| IP VPN (WireGuard wg-mgmt) | 10.66.66.1 |
| Port SSH | 22 |
| User | ghost |
| OS | Linux 6.1.0-44-amd64 Debian |
| Uptime (2026-05-04) | 14 days 21 hours |
| Load | 2.62 / 1.08 / 0.59 |
| Home | /home/ghost |
| Repo | /opt/trading (git: sot/mainline) |

## Connectivite (2026-05-04, apres reprise SSH)

| Chemin | Resultat |
| --- | --- |
| 192.168.0.111:22 | OK |
| 10.66.66.1:22 (WG) | OK |
| Ping depuis cursor-ai | OK |
| Ping depuis db-layer | OK |

## WireGuard

### wg0 (VPN principal)
| Champ | Valeur |
| --- | --- |
| Port | 51820 |
| Peer | 10.8.0.2 |

### wg-mgmt (VPN management)
| Champ | Valeur |
| --- | --- |
| Port | 51821 |
| Peers | cursor-ai (10.66.66.4), db-layer (10.66.66.2), student (10.66.66.3) |
| Handshakes | Tous < 2 min |

## Tmux

Aucune session tmux active.

## Repo Git

- Branche: sot/mainline
- Modifications locales: GO_INDEX.md, ACTIVE_STREAMS.md, REPRISE.md modifies
- Fichiers supprimes localement: reseau_ssh_step1, reseau_ssh_step1b, reseau_ssh_step2 (anciens modules)
- Untracked: _archive/legacy_modules/, docs/chantiers/* (runtime/OpenClaw), modules/reseau_ssh/*

## OpenCode

| Champ | Valeur |
| --- | --- |
| Binaire | /usr/local/bin/opencode |
| Version | 1.4.2 |
| Port | 127.0.0.1:4096 |
| Statut | Actif (process opencode) |

## OpenClaw

NON INSTALLE sur admin-trading. Modules documentaires seulement (configure_openclaw, doctor_openclaw, evidence_openclaw). Conformement au plan, OpenClaw principal est sur db-layer (127.0.0.1:18789).
