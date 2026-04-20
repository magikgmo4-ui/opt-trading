# Fiches machines — référence consolidée

> Document de référence lisible pour les 4 machines du stack trading.
> Source : fiches + rôles + snapshots (sans données sensibles).
> Note 2026-04-20 : LAN actif observé depuis `cursor-ai` = `192.168.0.0/24`.
> Les valeurs `192.168.16.x` issues des snapshots du 2026-02-26 sont historiques (ancien routeur).

---

## 1. admin-trading

| Champ | Valeur |
|-------|--------|
| **Hostname** | admin-trading |
| **Matériel** | HP EliteBook 840 G1 (laptop) |
| **OS** | Debian 12 (bookworm) |
| **Kernel** | 6.1.0-42-amd64 |
| **CPU** | Intel Core i5-4300U @ 1.90 GHz (4 threads) |
| **RAM** | 7,7 Go |
| **Disque** | 219 Go (ext4 sur /) |

**Réseau (LAN)**
- Subnet : 192.168.0.0/24
- Interface : wlo1 (Wi-Fi)
- IP : 192.168.0.111
- Gateway : 192.168.0.1
- DNS : 192.168.0.1

**Ports en écoute** : 22, 631, 4040, 5353, 8000, 8010, 42029, 51385, 51820

**Rôle**
- OPS / hôte principal des services
- Bastion SSH + orchestration
- APIs / UI exposées uniquement en LAN

**Services clés**
- sshd, tv-webhook, tv-bitget-runner
- <REDACTED_TUNNEL>-tv (tunnel webhook TradingView)

**Chemins utiles**
- Code : `/opt/trading/`, `/opt/trading/modules/`
- Scripts : `/opt/trading/scripts/`, `/usr/local/bin/` (menu-desk_pro, cmd-desk_pro)
- Logs : `/var/log/`, `/opt/trading/tmp/`

---

## 2. cursor-ai (poste de dev Windows)

| Champ | Valeur |
|-------|--------|
| **Hostname** | DESKTOP-1KDTQBH |
| **Matériel** | Dell (poste de dev) |
| **OS** | Windows 10 Pro (build 22621) |
| **CPU** | Intel Core i5-1145G7 @ 2.60 GHz (8 threads) |
| **RAM** | 16 Go |
| **Disques** | C: ~589 Go, D: ~1 To, E: ~1.5 To (NTFS) |

**Réseau (LAN)**
- Subnet : 192.168.0.0/24
- Interface LAN : Ethernet
- IP : 192.168.0.177
- Gateway : 192.168.0.1
- DNS : 192.168.0.1

**Rôle**
- Poste de dev principal (Cursor, UI, navigateur)
- Push/pull et déploiement vers les hôtes Debian via SSH

**Chemins utiles**
- Code : `C:\Users\ghost\Desktop\cursor_ai_workflow\`
- Transferts : `C:\Users\ghost\Downloads\`

---

## 3. db-layer

| Champ | Valeur |
|-------|--------|
| **Hostname** | ghost |
| **Matériel** | MSI GE62 2QD (laptop) |
| **OS** | Ubuntu 24.04.4 LTS |
| **Kernel** | 6.17.0-14-generic |
| **CPU** | Intel Core i7-5700HQ @ 2.70 GHz (8 threads) |
| **RAM** | 11 Go |
| **Disque** | 915 Go (ext4 sur /) |

**Réseau (LAN)**
- Subnet : 192.168.0.0/24
- Interface : enp4s0 (Ethernet)
- IP : 192.168.0.100
- Gateway : 192.168.0.1
- DNS :

**Ports en écoute** : 22, 53, 631, 1901, 5353, 9100, 32400, 32401, 32410–32414, 32600, 34211, 36397, 36708, 40225, 43128, 44539, 50803, 51821, 56112, 60399

**Rôle**
- Couche DB / services backend persistants
- Hébergement bases de données (LAN-only)
- APIs / services backend selon besoin

**Services clés**
- sshd, algo-hf-api (FastAPI webhook)
- plexmediaserver, gnome-remote-desktop

**Chemins utiles**
- Données : `/var/lib/postgresql/`, `/var/lib/docker/` (si utilisé)
- Logs : `/var/log/`

---

## 4. student

| Champ | Valeur |
|-------|--------|
| **Hostname** | student |
| **Matériel** | HP ProDesk 600 G3 SFF (desktop) |
| **OS** | Debian 12 (bookworm) |
| **Kernel** | 6.1.0-43-amd64 |
| **CPU** | Intel Core i5-6500 @ 3.20 GHz (4 cœurs) |
| **RAM** | 7,6 Go |
| **Disques** | 28 Go /, 200 Go /home (LVM sur nvme, LUKS) |

**Réseau (LAN)**
- Subnet : 192.168.0.0/24
- Interface : eno1 (Ethernet)
- IP : 192.168.0.142
- Gateway : 192.168.0.1
- DNS : 1.1.1.1, 8.8.8.8

**Ports en écoute** : 22, 631, 5353, 8020, 45095, 59623

**Rôle**
- Sandbox / expérimentations / POC
- Environnement pour agents et tests
- Réception de jeux de données / logs sanitisés

**Services clés**
- sshd, fail2ban
- student-ingest, student-watchdrop (API FastAPI + watcher)

**Chemins utiles**
- Code : `/opt/trading/` (clone trading, user student)
- Scripts : `/opt/trading/scripts/`, `/usr/local/bin/` (menu-student, cmd-student)

---

## Vue d’ensemble réseau active (LAN 192.168.0.0/24)

| Machine        | IP             | Interface |
|----------------|----------------|-----------|
| admin-trading  | 192.168.0.111  | wlo1      |
| cursor-ai      | 192.168.0.177  | Ethernet  |
| db-layer       | 192.168.0.100  | enp4s0    |
| student        | 192.168.0.142  | eno1      |

---

*Généré le 2026-02-26 à partir des snapshots et fiches machines.*
