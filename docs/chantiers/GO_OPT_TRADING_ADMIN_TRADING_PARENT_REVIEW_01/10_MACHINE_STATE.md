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

## Identite connue

| Champ | Valeur |
| --- | --- |
| Hostname | admin-trading |
| IP LAN | 192.168.0.111 |
| IP VPN (WireGuard) | 10.66.66.1 |
| Port SSH | 22 |
| User | ghost |
| Role | Runtime trading reel / orchestration / webhook / Desk Pro |
| OS | Debian (Linux) |

## Connectivite (2026-05-04)

### Depuis cursor-ai (Windows)

| Chemin | Resultat |
| --- | --- |
| 192.168.0.111:22 TCP | handshake TCP OK, banner SSH timeout |
| 10.66.66.1:22 (WireGuard) | timeout |
| 10.8.0.1:22 (WG tunnel) | timeout |

### Depuis db-layer (192.168.0.100)

| Chemin | Resultat |
| --- | --- |
| ping 192.168.0.111 | "Destination Host Unreachable" |
| ssh 192.168.0.111:22 | "No route to host" |
| WireGuard (wg-mgmt) | last handshake: 2 days 21 hours ago |

### Autres machines

| Machine | Statut SSH |
| --- | --- |
| db-layer (192.168.0.100) | OK |
| student (192.168.0.142) | OK |
| fantome (192.168.0.191) | OK |
| admin-trading (192.168.0.111) | UNREACHABLE |

## Diagnostic

- TCP handshake reussit depuis cursor-ai = machine allumee, firewall autorise port 22
- Banner SSH timeout = daemon SSH probablement bloque / surcharge / inactif
- Depuis db-layer = pas de route IP = segmentation reseau ou admin-trading sur un autre segment
- Handshake WireGuard stale (2+ jours) = tunnel WG probablement tombe
- Machine vraisemblablement en etat degrade — SSH daemon ne repond pas

## Impact

- Aucun controle runtime possible
- Aucune verification services / ports / processus
- Cartographie basee uniquement sur le repo et les registres
- /shared non monte sur db-layer (car admin-trading = serveur SFTP)

## Recommandation immediate

Avant tout GO runtime trading, retablir la connectivite admin-trading :
- Redemarrer physiquement la machine ou recuperer SSH via console
- Retablir le tunnel WireGuard
- Verifier l'etat du daemon SSH
