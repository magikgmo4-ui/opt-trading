# OT-RECHECK-SSHFS-01 — REPORT (MINI REVALIDATION LIVE ADMIN-TRADING)

Date (America/Montreal) : 2026-03-12

## 1. RÉSUMÉ EXÉCUTIF
- **Bug symlink-safe** : corrigé et confirmé live sur `admin-trading` (`cmd-shared_sshfs_permanent info` et `sanity-shared_sshfs_permanent` ne dérivent plus vers `/usr/local`).
- **Déploiement SSHFS** : inchangé, toujours **absent/non déployé** sur `admin-trading` (`/opt/trading/scripts/shared_sshfs_permanent_*` absent et aucune unit `shared-sshfs.service` prouvée par OT-LIVE-01).
- **Réserve OT-SVC-01 (SSHFS)** : peut être **réduite/reformulée** (wrapper bug levé), mais reste **maintenue** côté déploiement service/mount.

## 2. MACHINE INSPECTÉE
- `admin-trading` (Debian 12, user `ghost`)

## 3. VERSION / TESTS REJOUÉS

### 3.1 Mise à jour repo
```bash
git -C /opt/trading pull --ff-only
```
Résultat : “Déjà à jour.”

### 3.2 Note de rigueur (patch réellement testé)
- Les wrappers installés sur `admin-trading` pointent vers `modules/shared_sshfs_permanent/scripts/*`.
- La version des scripts testée live est celle présente sur disque dans `/opt/trading/modules/shared_sshfs_permanent/scripts/`.

## 4. RÉSULTATS PAR COMMANDE (LIVE)

### 4.1 Preuve wrappers (symlinks installés)
```bash
ls -l /usr/local/bin/cmd-shared_sshfs_permanent /usr/local/bin/sanity-shared_sshfs_permanent /usr/local/bin/menu-shared_sshfs_permanent
```
Extrait :
```text
/usr/local/bin/cmd-shared_sshfs_permanent -> /opt/trading/modules/shared_sshfs_permanent/scripts/cmd.sh
/usr/local/bin/sanity-shared_sshfs_permanent -> /opt/trading/modules/shared_sshfs_permanent/scripts/sanity_check.sh
```

### 4.2 cmd-shared_sshfs_permanent info (post-patch)
```bash
cmd-shared_sshfs_permanent info
```
Résultat :
```text
name=shared_sshfs_permanent
path=/opt/trading/modules/shared_sshfs_permanent
```
Statut : **PASS**

### 4.3 sanity-shared_sshfs_permanent (post-patch)
```bash
sanity-shared_sshfs_permanent || true
```
Résultat :
```text
PASS: wrapper sanity OK
```
Statut : **PASS**

### 4.4 cmd-shared_sshfs_permanent readme (post-patch)
```bash
cmd-shared_sshfs_permanent readme || true
```
Résultat : README trouvée (extrait visible), dont note sur wrappers install vs module.
Statut : **PASS**

### 4.5 Test symlink temporaire (/tmp)
```bash
ln -sf /opt/trading/modules/shared_sshfs_permanent/scripts/cmd.sh /tmp/cmd-shared_sshfs_permanent-test
bash /tmp/cmd-shared_sshfs_permanent-test info
ln -sf /opt/trading/modules/shared_sshfs_permanent/scripts/sanity_check.sh /tmp/sanity-shared_sshfs_permanent-test
bash /tmp/sanity-shared_sshfs_permanent-test || true
```
Résultat : `name=shared_sshfs_permanent` + `PASS: wrapper sanity OK`.
Statut : **PASS**

### 4.6 Délégation vers /opt/trading/scripts (modèle d’installation)
```bash
ls -l /opt/trading/scripts/shared_sshfs_permanent_* 2>/dev/null || echo "NO /opt/trading/scripts/shared_sshfs_permanent_*"
```
Résultat : `NO /opt/trading/scripts/shared_sshfs_permanent_*`
Statut : **PASS AVEC NOTE** (délégation non activable car install non fait)

## 5. BUG SYMLINK CORRIGÉ OU NON ?
- **Oui (ÉTABLI LIVE)** : la dérive `/usr/local` a disparu ; les wrappers retrouvent le module.

## 6. LIMITES RESTANTES
- **Service/mount** : toujours non prouvé/déployé sur `admin-trading` (hors périmètre de cette revalidation).
- **Délégation install** : non validée (scripts `/opt/trading/scripts/shared_sshfs_permanent_*` absents).
- **Note opérationnelle** : lors de la copie de fichiers depuis un poste Windows, une correction CRLF→LF a été nécessaire côté `admin-trading` (symptôme `bash\\r`). Ce point n’affecte pas l’analyse du bug symlink, mais doit être évité via discipline d’EOL.

## 7. FICHIERS MODIFIÉS
- Repo Windows : aucun fichier supplémentaire au-delà du patch déjà livré (OT-PATCH-SSHFS-01).
- Live `admin-trading` (strict minimum pour test) :
  - mise à jour /opt/trading : `git pull` (no-op),
  - normalisation LF des scripts wrappers après transfert (sinon `bash\\r`).

## 8. COMMANDES EXÉCUTÉES
- Voir sections 3 et 4.

## 9. VERDICT FINAL
La correction symlink-safe est **confirmée live** sur `admin-trading`. Le déploiement SSHFS reste **absent/non prouvé** et la réserve OT-SVC-01 doit rester maintenue côté service/mount, mais peut être reformulée car l’erreur “wrappers incohérents” est levée.

## 10. IMPACT SUR OT-SVC-01
- Réserve SSHFS : **réduire** (bug wrappers levé) / **maintenir** (service/mount non déployé).

