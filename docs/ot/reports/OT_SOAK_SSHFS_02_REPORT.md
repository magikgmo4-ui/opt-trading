# OT-SOAK-SSHFS-02 — REPORT (RECONNEXION CONTRÔLÉE shared_sshfs_permanent)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Objectif : prouver le comportement de récupération de `/shared` après “perte/reprise” contrôlée sur `db-layer` et `student`.
- Contrainte opérationnelle : aucun accès `sudo` non-interactif sur ces machines (pas de coupure réseau iptables/nmcli sans saisir un mot de passe).
- Méthode retenue (sûre, ciblée) : simuler la perte réseau **du point de vue du montage** en terminant le process `sshfs` (MainPID) du service `shared-sshfs.service`, afin d’observer le **restart systemd** et le rétablissement du mount.
- Résultat : sur `db-layer` et `student`, `shared-sshfs.service` redémarre automatiquement et `/shared` redevient lisible sans intervention manuelle.

## 2. MÉTHODE DE TEST

### 2.1 Pourquoi cette méthode
- Une coupure réseau “pure” (désactivation interface, iptables/nftables, nmcli) nécessite `sudo`.
- Les services `shared-sshfs.service` tournent en `User=<user>` : l’utilisateur peut terminer son propre process `sshfs` sans privilèges.
- Terminer le process `sshfs` reproduit l’effet “lien brisé” pour `/shared`, tout en évitant de casser la connectivité SSH globale de la machine.

### 2.2 Procédure
Pour chaque machine (une à la fois) :
1. Baseline : `systemctl is-enabled/is-active`, `findmnt /shared`, `sanity-shared_sshfs_permanent`, lecture non destructive.
2. Coupure contrôlée : `kill -TERM $(systemctl show -p MainPID --value shared-sshfs.service)`
3. Observation : `systemctl is-active`, `findmnt /shared`, lecture sous `timeout`.
4. Rétablissement : attendu automatiquement via `Restart=on-failure` (systemd), puis re-validation.

## 3. BASELINE AVANT COUPURE

### 3.1 db-layer
- `shared-sshfs.service` : enabled + active
- `/shared` : monté (fuse.sshfs) depuis `ghost@admin-trading:/srv/sftp/shared_files/shared`
- Sanity : PASS (6/0)
- Lecture : `/shared/boot_test.txt` lisible

### 3.2 student
- `shared-sshfs.service` : enabled + active
- `/shared` : monté (fuse.sshfs) depuis `ghost@admin-trading:/srv/sftp/shared_files/shared`
- Sanity : PASS (6/0)
- Lecture : `/shared/boot_test.txt` lisible

## 4. RÉSULTAT PENDANT COUPURE

### 4.1 db-layer
- Pendant la fenêtre de redémarrage : `systemctl is-active` → `activating`
- Lecture non destructive : échec temporaire (`READ_FAIL`) pendant l’intervalle de redémarrage

### 4.2 student
- Pendant la fenêtre de redémarrage : `systemctl is-active` → `activating`
- Lecture non destructive : échec temporaire (`READ_FAIL`) pendant l’intervalle de redémarrage

## 5. RÉSULTAT APRÈS RÉTABLISSEMENT

### 5.1 db-layer
- Auto-récupération : **OK**
- Service : `active`
- Mount : `/shared` à nouveau monté et lisible
- Preuve logs (extrait) :
  - `Main process exited ... status=1/FAILURE`
  - `Scheduled restart job ...`
  - `Started shared-sshfs.service ...`

### 5.2 student
- Auto-récupération : **OK**
- Service : `active`
- Mount : `/shared` à nouveau monté et lisible
- Preuve : changement de `Main PID` observé via `systemctl status` (service relancé à `2026-03-13 20:11:27`)

## 6. COMPARATIF db-layer / student
- Comportement identique : arrêt contrôlé du process `sshfs` → redémarrage systemd → `/shared` de nouveau lisible.
- Différence mineure : lecture “depuis start timestamp” de `journalctl --since` n’est pas uniforme entre distributions ; preuve complémentaire faite via `systemctl status` (student).

## 7. JOURNAUX UTILES (EXTRAITS)
- `db-layer` : journalctl depuis le début du test montre la séquence failure→restart→mount.
- `student` : `systemctl status shared-sshfs.service` montre le nouveau PID et les lignes de mount.

## 8. FICHIERS MODIFIÉS
- Repo : ce report (et le closing associé).

## 9. COMMANDES EXÉCUTÉES
- Baseline :
  - `systemctl is-enabled shared-sshfs.service`
  - `systemctl is-active shared-sshfs.service`
  - `findmnt /shared`
  - `sanity-shared_sshfs_permanent`
  - `timeout 4 ls -lah /shared/boot_test.txt`
- Coupure :
  - `systemctl show -p MainPID --value shared-sshfs.service`
  - `kill -TERM <MainPID>`
- Vérification :
  - `systemctl is-active shared-sshfs.service`
  - `findmnt /shared`
  - `timeout 4 ls -lah /shared/boot_test.txt`
  - `journalctl -u shared-sshfs.service ...` / `systemctl status shared-sshfs.service`

## 10. VERDICT FINAL
- `db-layer` : **PASS**
- `student` : **PASS**
- Réserve restante : la coupure “réseau” n’a pas été réalisée au niveau interface/firewall (nécessite `sudo`). Le comportement de récupération du service et du mount est cependant prouvé via restart contrôlé du transport sshfs.

## 11. IMPACT SUR OT-SVC-01
- La réserve “reconnexion réseau” est **réduite** : récupération automatique prouvée sur `db-layer` et `student` sans intervention manuelle (dans le modèle “transport reset”).


## RISKS

- À qualifier.
