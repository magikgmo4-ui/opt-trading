# OT-NET-RECONNECT-03 — SYNTHESIS

Date (America/Montreal) : 2026-03-14

## Objectif
Tester une coupure “réseau pur” vers `admin-trading:22` pour observer la robustesse de reconnexion de `/shared` (SSHFS), sur :
- db-layer
- student

## ÉTABLI
- `/shared` est monté et lisible avant coupure sur db-layer et student (SSHFS via `shared-sshfs.service`).
- Le montage SSHFS est configuré avec `-o reconnect` + keepalives (vu dans `systemctl status shared-sshfs.service`).

## DB-LAYER — PASS / PROVED
### ÉTABLI
- IP cible retenue : `192.168.16.155:22`.
- La règle OUTPUT ciblée vers `admin-trading:22` a été réellement posée puis retirée (fenêtre opérateur).
### OBSERVÉ PENDANT COUPURE
- Nouveaux SSH vers `admin-trading` bloqués comme attendu.
- `/shared` reste monté ; lectures simples (`ls/stat`) restent OK dans la fenêtre observée.
### OBSERVÉ APRÈS RESTAURATION
- SSH vers `admin-trading` redevient possible.
- `/shared` reste observable.

## STUDENT — PASS / PROVED
### ÉTABLI
- IP cible : `192.168.16.155:22`.
- Règle OUTPUT posée puis retirée via `sudo /usr/sbin/iptables ...`.
### OBSERVÉ PENDANT COUPURE
- Nouveaux SSH vers `admin-trading` bloqués (attendu) ; `SSH_DURING_RC=255`.
- `/shared` reste monté en `fuse.sshfs` ; `LS_DURING_RC=0` ; `STAT_DURING_RC=0`.
- `shared-sshfs.service` reste active.
### OBSERVÉ APRÈS RESTAURATION
- Règle absente ; SSH redevient OK ; `SSH_AFTER_RC=0`.
- `/shared` reste monté ; `LS_AFTER_RC=0` ; `STAT_AFTER_RC=0`.
- `shared-sshfs.service` active.

## Verdict global OT-NET-RECONNECT-03
**CLOSE / PROVED** :
- db-layer : PASS / PROVED
- student : PASS / PROVED

## Point de reprise exact
> **Néant (OT-NET-RECONNECT-03 clôturée)**
