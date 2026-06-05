# OT-NET-RECONNECT-01 — REPORT (ROBUSTESSE RÉSEAU “PURE” /shared)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Objectif : prouver une vraie perturbation réseau contrôlée impactant le transport SSH vers `admin-trading` pour observer la récupération de `shared-sshfs.service` et `/shared`.
- Résultat : **NON TESTÉ (coupure réseau pure)** sur `db-layer` et `student` faute de mécanisme réversible exécutable sans `sudo` (et sans agent polkit interactif).
- Preuve live : baseline complète OK sur les deux machines ; tentative `nmcli networking off` échoue par manque d’autorisations.
- Preuve indirecte : logs historiques montrent des occurrences “Timeout … not responding” + “remote host has disconnected” sur les deux machines, indiquant un comportement de reconnexion déjà rencontré, mais non contrôlé.

## 2. MÉTHODE DE COUPURE RETENUE (ET LIMITES)

### 2.1 Méthodes envisagées
- `nmcli networking off/on` (NetworkManager)
- down/up interface (ip link)
- stop/start WireGuard (wg-quick@…)
- règle firewall temporaire (iptables/nft) ciblant `admin-trading:22`

### 2.2 Méthode réellement utilisable dans ce contexte
Sur `db-layer` et `student` :
- `sudo -n` indisponible (demande mot de passe).
- `nmcli` nécessite une autorisation polkit (refusée en non-interactif) :
  - `Not authorized to enable/disable networking`.

Conclusion : la coupure réseau “pure” n’est pas exécutable de manière contrôlée et réversible dans ce contexte non-interactif ; le test est classé **NON TESTÉ**.

### 2.3 Méthode recommandée (réaliste) pour lever la réserve
Exécuter localement sur chaque machine (avec `sudo` interactif) une coupure ciblée ne cassant pas la session SSH :
- Bloquer temporairement l’outbound TCP vers `admin-trading` port 22 (iptables OUTPUT).
- Observer `/shared` pendant blocage, puis après retrait des règles.

## 3. BASELINE (AVANT COUPURE)

### 3.1 db-layer — ÉTABLI LIVE
- `sudo -n` : NO
- `shared-sshfs.service` : enabled + active
- `findmnt /shared` : monté depuis `ghost@admin-trading:/srv/sftp/shared_files/shared`
- `sanity-shared_sshfs_permanent` : PASS
- lecture `/shared/boot_test.txt` : OK (`boot-test`)

### 3.2 student — ÉTABLI LIVE
- `sudo -n` : NO
- `shared-sshfs.service` : enabled + active
- `findmnt /shared` : monté depuis `ghost@admin-trading:/srv/sftp/shared_files/shared`
- `sanity-shared_sshfs_permanent` : PASS
- lecture `/shared/boot_test.txt` : OK (`boot-test`)

## 4. RÉSULTATS PENDANT COUPURE (NON TESTÉ)

### 4.1 db-layer
- Tentative `nmcli networking off` : refusée (“Not authorized”).
- Coupure réseau réelle : NON TESTÉE.

### 4.2 student
- Tentative `nmcli networking off` : refusée (“Not authorized”).
- Coupure réseau réelle : NON TESTÉE.

## 5. RÉSULTATS APRÈS RÉTABLISSEMENT (NON TESTÉ)
- Non applicable : coupure non effectuée.

## 6. COMPARATIF db-layer / student
- Symétrique : mêmes limites (pas de `sudo -n`, nmcli non autorisé) → mêmes conclusions NON TESTÉ.

## 7. JOURNAUX UTILES (INDIRECTS)

### 7.1 db-layer (extraits historiques)
- `Timeout, server 192.168.16.155 not responding.`
- `remote host has disconnected`

### 7.2 student (extraits historiques)
- `Timeout, server 192.168.16.155 not responding.`
- `remote host has disconnected`

## 8. FICHIERS MODIFIÉS
- `OT_NET_RECONNECT_01_REPORT.md`
- `OT_NET_RECONNECT_01_CLOSING.txt`

## 9. COMMANDES EXÉCUTÉES
- Baseline : `systemctl is-enabled/is-active`, `findmnt /shared`, `sanity-shared_sshfs_permanent`, `cat /shared/boot_test.txt`, `journalctl -u shared-sshfs.service -n 40`
- Qualification permissions : `sudo -n true`, `nmcli general permissions`
- Tentative coupure : `nmcli networking off` (refusée)

## 10. VERDICT FINAL
- `db-layer` : **NON TESTÉ** (coupure réseau “pure” non exécutable sans privilèges)
- `student` : **NON TESTÉ** (coupure réseau “pure” non exécutable sans privilèges)
- Réserve restante : test contrôlé au niveau firewall/interface.

## 11. IMPACT SUR OT-SVC-01
- Réserve “reconnexion” : **non levée** (preuve “pure” absente), mais déjà réduite par OT-SOAK-SSHFS-02 (transport reset via restart).

## ANNEXE — RUNBOOK MINIMAL (OPÉRATEUR, AVEC SUDO)

### A. db-layer (exécuter localement sur db-layer)
```bash
set -euo pipefail
start_epoch=$(date +%s)
echo "START_EPOCH=$start_epoch"

systemctl is-active shared-sshfs.service
findmnt /shared
timeout 4 cat /shared/boot_test.txt

ADMIN_V4_1=10.66.66.1
ADMIN_V4_2=192.168.16.155

sudo iptables -I OUTPUT 1 -p tcp -d "$ADMIN_V4_1" --dport 22 -j REJECT --reject-with tcp-reset
sudo iptables -I OUTPUT 1 -p tcp -d "$ADMIN_V4_2" --dport 22 -j REJECT --reject-with tcp-reset

sleep 30
systemctl is-active shared-sshfs.service || true
findmnt /shared || true
timeout 4 cat /shared/boot_test.txt || echo READ_FAIL
journalctl -u shared-sshfs.service --since "@$start_epoch" -n 120 --no-pager || true

sudo iptables -D OUTPUT -p tcp -d "$ADMIN_V4_1" --dport 22 -j REJECT --reject-with tcp-reset
sudo iptables -D OUTPUT -p tcp -d "$ADMIN_V4_2" --dport 22 -j REJECT --reject-with tcp-reset

sleep 30
systemctl is-active shared-sshfs.service || true
findmnt /shared || true
timeout 4 cat /shared/boot_test.txt || echo READ_FAIL
journalctl -u shared-sshfs.service --since "@$start_epoch" -n 200 --no-pager || true
```

### B. student (exécuter localement sur student)
Même runbook ; adapter si `admin-trading` est atteint via IP différente (consulter `getent ahostsv4 admin-trading`).


## RISKS

- À qualifier.
