# OT-SOAK-SSHFS-01 — REPORT (STABILITÉ shared_sshfs_permanent)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Objectif : vérifier la stabilité opérationnelle de `shared_sshfs_permanent` sur `db-layer` après reboot/reconnexion réseau et usage normal.
- Contraintes : prudence runtime (pas de “stress test” destructif, pas de mount manuel).

## 2. MATRICE DE SOAK (CIBLES)

### A. Post-boot (après reboot)
- Service `shared-sshfs.service` : enabled + active (running)
- `/shared` : monté (`findmnt`) + lisible (listing non destructif)
- Sanity module : PASS

### B. Reconnexion réseau (après coupure / retour réseau)
- Service : reste actif ou se rétablit (restart policy)
- Logs : pas de boucle d’échec, pas de dérive perms/known_hosts
- `/shared` : redevient monté et lisible

### C. Usage normal
- Lecture directory + lecture d’échantillons (sans écriture)
- Pas d’erreurs “Transport endpoint is not connected”

## 3. MACHINE
- `db-layer` (Ubuntu 24.04.4, VPN 10.66.66.2)

## 4. TESTS REJOUÉS (LIVE)
### 4.1 Post-boot (boot courant)
Statut : **PASS**
```bash
uptime -s
systemctl is-enabled shared-sshfs.service
systemctl is-active shared-sshfs.service
systemctl status shared-sshfs.service --no-pager -n 20
findmnt /shared
sanity-shared_sshfs_permanent
```
Preuves clés (extraits) :
- Boot : `2026-03-13 17:22:33`
- Service : `enabled` + `active`
- Mount : `/shared` ← `ghost@admin-trading:/srv/sftp/shared_files/shared` (fuse.sshfs)
- Sanity : `Summary: PASS=6 FAIL=0`

### 4.2 Usage normal (lecture non destructive)
Statut : **PASS**
```bash
ls -lah /shared | head -n 40
sed -n '1,5p' /shared/boot_test.txt
```
Résultat : listing OK ; lecture OK (`boot-test`).

### 4.3 Erreurs service sur le boot courant
Statut : **PASS**
```bash
journalctl -u shared-sshfs.service -b --no-pager | egrep -i 'timeout|disconnect|error|fail|Transport endpoint' || echo 'no matching errors'
```
Résultat : `no matching errors`.

### 4.4 Reconnexion réseau (coupure/retour)
Statut : **NON TESTÉ**
- Aucune coupure réseau volontaire n’a été effectuée dans cette mission.
- Le service est configuré avec des options de reconnexion (`-o reconnect`, `ServerAliveInterval/CountMax`) et une policy systemd `Restart=on-failure`, ce qui est favorable, mais ne remplace pas une preuve par évènement réel.

## 5. RÉSERVE STABILITÉ / EXTENSION (CANONIQUE)
- Stabilité long-terme : à confirmer par observation sur plusieurs sessions/boots et incidents réseau.
- Généralisation multi-machines : à décider machine par machine (au-delà de `db-layer`).

## 5. CONCLUSION (PROVISOIRE)
Post-boot et usage normal sont prouvés OK sur `db-layer`. La seule réserve restante concerne une preuve explicite de comportement après reconnexion réseau (incident réel ou test contrôlé).
