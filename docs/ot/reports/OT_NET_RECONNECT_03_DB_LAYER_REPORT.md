# OT-NET-RECONNECT-03 — DB-LAYER REPORT

Date (America/Montreal) : 2026-03-14

## Résumé exécutif
- IP cible prouvée côté db-layer pour `admin-trading` : `192.168.16.155`.
- Coupure “réseau pur” vers `admin-trading:22` : **PASS / PROVED** (règle OUTPUT posée, observée, retirée).
- Pendant coupure : nouveaux SSH vers `admin-trading` bloqués (échec attendu) ; `/shared` reste monté ; lectures simples (`ls/stat`) restent OK dans la fenêtre observée.
- Après retrait : règle absente ; SSH vers `admin-trading` OK ; `/shared` reste monté ; lectures simples OK.

## Environnement réel
- Machine cible : `db-layer`
- `/shared` : monté via SSHFS (preuve ci-dessous)

## IP cible réellement retenue
### ÉTABLI
- IP cible : `192.168.16.155` (preuve opérateur fournie).

## Commandes exécutées
### A) Coupure opérateur (db-layer, sudo interactif)
- Insertion :
  - `sudo iptables -I OUTPUT -p tcp -d 192.168.16.155 --dport 22 -j REJECT -m comment --comment OT-NET-RECONNECT-03`
  - `INSERT_RC=0`
- Preuve présence :
  - `iptables -S OUTPUT` contient :
    - `-A OUTPUT -d 192.168.16.155/32 -p tcp -m tcp --dport 22 -m comment --comment OT-NET-RECONNECT-03 -j REJECT ...`
- Pendant coupure :
  - `findmnt -T /shared` (toujours monté en `fuse.sshfs`)
  - `timeout 3s ls -la /shared | head -n 8` ; `LS_DURING_RC=0`
  - `timeout 3s stat /shared/README.txt` ; `STAT_DURING_RC=0`
  - `timeout 3s ssh ... admin-trading` :
    - `ssh: connect to host 192.168.16.155 port 22: Connection refused`
    - `SSH_DURING_RC=255`
  - `shared-sshfs.service` reste active
- Retrait :
  - `sudo iptables -D OUTPUT -p tcp -d 192.168.16.155 --dport 22 -j REJECT -m comment --comment OT-NET-RECONNECT-03`
  - `DELETE_RC=0`
- Après restauration :
  - `iptables -S OUTPUT` ne contient plus la règle `OT-NET-RECONNECT-03`
  - `timeout 3s ssh ... admin-trading` : `SSH_OK` ; `SSH_AFTER_RC=0`
  - `/shared` toujours monté ; `LS_AFTER_RC=0` ; `STAT_AFTER_RC=0`
  - `shared-sshfs.service` active

## Résultats avant coupure
### ÉTABLI
- État initial fourni : `/shared` monté et lecture simple OK (prérequis de la fenêtre opérateur).

## Résultats pendant coupure
### OBSERVÉ PENDANT COUPURE (réseau pur)
### ÉTABLI
- Règle présente dans `iptables -S OUTPUT` (ciblée `192.168.16.155/32` port 22, comment `OT-NET-RECONNECT-03`).
- SSH vers `admin-trading` échoue pendant coupure :
  - `ssh: connect to host 192.168.16.155 port 22: Connection refused`
  - `SSH_DURING_RC=255`
- `/shared` reste monté en `fuse.sshfs` (findmnt).
- Lectures simples restent OK :
  - `LS_DURING_RC=0`
  - `STAT_DURING_RC=0`
- `shared-sshfs.service` reste active.

## Résultats après restauration
### OBSERVÉ APRÈS RESTAURATION
### ÉTABLI
- Règle absente dans `iptables -S OUTPUT`.
- SSH vers `admin-trading` OK : `SSH_OK` ; `SSH_AFTER_RC=0`.
- `/shared` toujours monté ; `LS_AFTER_RC=0` ; `STAT_AFTER_RC=0`.
- `shared-sshfs.service` active.

## Écarts prouvés
- Néant prouvé côté db-layer sur ce test.

## Corrections appliquées
- Néant (pas d’accès permettant correction ; pas de changement durable sans preuve).

## Verdict strict (db-layer)
**PASS / PROVED**.

## Point de reprise exact
> **OT-NET-RECONNECT-03 — STUDENT (détection méthode de coupure + preuve avant/pdt/après)**
