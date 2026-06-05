# OT-NET-RECONNECT-03 — STUDENT REPORT

Date (America/Montreal) : 2026-03-14

## Résumé exécutif
- Cible prouvée : `192.168.16.155:22`.
- Coupure “réseau pur” vers `admin-trading:22` : **PASS / PROVED** (règle OUTPUT posée, prouvée présente, puis retirée).
- Pendant coupure : nouveaux SSH vers `admin-trading` bloqués comme attendu ; `/shared` reste monté ; lectures simples (`ls/stat`) restent OK dans la fenêtre observée ; `shared-sshfs.service` reste active.
- Après retrait : règle absente ; SSH vers `admin-trading` OK ; `/shared` reste monté ; lectures simples OK ; service actif.

## Environnement réel
- Hostname : `student`
- User : `student`
- Shell : `/bin/bash`
- `/shared` : présent (montage SSHFS via systemd)

## IP cible réellement retenue
### ÉTABLI
- `192.168.16.155:22`

## Commandes exécutées
### A) Coupure opérateur (student, sudo interactif)
- Insertion règle (ciblée `192.168.16.155:22`) :
  - `sudo /usr/sbin/iptables -I OUTPUT -p tcp -d 192.168.16.155 --dport 22 -j REJECT -m comment --comment OT-NET-RECONNECT-03`
  - `INSERT_RC=0`
- Preuve règle présente :
  - `iptables -S OUTPUT`
  - `iptables -L OUTPUT`
- Observation pendant coupure :
  - `findmnt -T /shared`
  - `timeout 3s ls -la /shared | head -n 8` ; `LS_DURING_RC=0`
  - `timeout 3s stat /shared/README.txt` ; `STAT_DURING_RC=0`
  - `timeout 3s ssh -o BatchMode=yes -o ConnectTimeout=3 admin-trading "echo SHOULD_FAIL"` :
    - `ssh: connect to host 192.168.16.155 port 22: Connection refused`
    - `SSH_DURING_RC=255`
  - `shared-sshfs.service` active
- Retrait règle :
  - `sudo /usr/sbin/iptables -D OUTPUT -p tcp -d 192.168.16.155 --dport 22 -j REJECT -m comment --comment OT-NET-RECONNECT-03`
  - `DELETE_RC=0`
- Après restauration :
  - `iptables -S OUTPUT` ne contient plus `OT-NET-RECONNECT-03`
  - `timeout 3s ssh -o BatchMode=yes -o ConnectTimeout=3 admin-trading "echo SSH_OK"` ; `SSH_AFTER_RC=0`
  - `/shared` toujours monté ; `LS_AFTER_RC=0` ; `STAT_AFTER_RC=0`
  - `shared-sshfs.service` active

## Résultats avant coupure
### ÉTABLI
- Cible retenue : `192.168.16.155:22`.

## Résultats pendant coupure
### OBSERVÉ PENDANT COUPURE (réseau pur)
### ÉTABLI
- Règle présente (prouvée via `iptables -S OUTPUT` et `iptables -L OUTPUT`).
- SSH vers admin-trading échoue comme attendu :
  - `ssh: connect to host 192.168.16.155 port 22: Connection refused`
  - `SSH_DURING_RC=255`
- `/shared` reste monté en `fuse.sshfs` (`findmnt -T /shared`).
- Lectures simples OK :
  - `LS_DURING_RC=0`
  - `STAT_DURING_RC=0`
- `shared-sshfs.service` reste active.

## Résultats après restauration
### OBSERVÉ APRÈS RESTAURATION
### ÉTABLI
- Règle absente (`iptables -S OUTPUT` ne contient plus `OT-NET-RECONNECT-03`).
- SSH vers admin-trading OK :
  - `SSH_OK`
  - `SSH_AFTER_RC=0`
- `/shared` toujours monté ; lectures simples OK :
  - `LS_AFTER_RC=0`
  - `STAT_AFTER_RC=0`
- `shared-sshfs.service` active.

## Écarts prouvés
- Néant prouvé sur ce test.

## Corrections appliquées
- Néant (périmètre : pas d’installation “par confort” sans décision opérateur explicite).

## Verdict strict (student)
**PASS / PROVED**.

## Point de reprise exact
> **Néant (student prouvé ; OT-NET-RECONNECT-03 clôturée)**

## RISKS

- À qualifier.
