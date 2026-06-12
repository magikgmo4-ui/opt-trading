# OT-PATCH-SSHFS-01 — REPORT (WRAPPERS SYMLINK-SAFE)

Date (America/Montreal) : 2026-03-12

## 1. RÉSUMÉ EXÉCUTIF
- Patch minimal appliqué sur `shared_sshfs_permanent` : les wrappers ne dérivent plus vers `/usr/local` quand invoqués via symlink `/usr/local/bin/*`.
- Alignement avec le modèle d’installation : si les scripts installés `/opt/trading/scripts/shared_sshfs_permanent_*.sh` existent, les wrappers module délèguent vers eux.
- Aucun changement systemd / aucun mount / aucune action live effectuée.

## 2. CAUSE RETENUE
- Cause prouvée par OT-LIVE-01 : les wrappers globaux sur `admin-trading` pointaient vers `modules/shared_sshfs_permanent/scripts/*`.
- Les scripts `cmd.sh` / `menu.sh` / `sanity_check.sh` utilisaient `$0` pour retrouver le module, donc via symlink (`/usr/local/bin/...`) ils prenaient `/usr/local` comme racine.
- Symptômes live associés : `name=local path=/usr/local` et `FAIL: scripts missing`.

## 3. FICHIERS INSPECTÉS
- [OT_FIX_SSHFS_01_DIAGNOSTIC.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_FIX_SSHFS_01_DIAGNOSTIC.md)
- [README.md](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/README.md)
- [INSTALL.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/INSTALL.sh)
- [cmd.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/cmd.sh)
- [menu.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/menu.sh)
- [sanity_check.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/sanity_check.sh)

## 4. PATCH APPLIQUÉ

### 4.1 Résolution symlink-safe (patch nécessaire)
- Remplacement de la déduction `MOD="${0%/*}/.."` par une résolution basée sur `${BASH_SOURCE[0]}` + `readlink -f` quand disponible, puis `MOD="$(cd "$(dirname "$SCRIPT")/.." && pwd -P)"`.
- Fichiers : [cmd.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/cmd.sh), [menu.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/menu.sh), [sanity_check.sh](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/scripts/sanity_check.sh).

### 4.2 Délégation vers le modèle d’installation (patch nécessaire)
- Si invocation via wrapper global attendu et scripts installés présents :
  - `cmd-shared_sshfs_permanent` → `/opt/trading/scripts/shared_sshfs_permanent_cmd.sh`
  - `menu-shared_sshfs_permanent` → `/opt/trading/scripts/shared_sshfs_permanent_menu.sh`
  - `sanity-shared_sshfs_permanent` → `/opt/trading/scripts/shared_sshfs_permanent_sanity.sh`
- Objectif : rester cohérent avec `INSTALL.sh` sans refactor ni changement live.

### 4.3 Doc minimale (patch nécessaire)
- Ajout d’une note de clarification dans le README sur la cible attendue des wrappers globaux (scripts installés) et le comportement en cas de wrapper pointant vers `modules/.../scripts/*`.
- Fichier : [README.md](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/README.md).

## 5. VALIDATION LOCALE/REPO

### 5.1 Contrôles statiques (PASS)
- Ancien pattern `$0%/*` supprimé dans ces wrappers.
- Présence de `readlink -f` ajoutée aux 3 scripts.

### 5.2 Exécution locale (NON TESTÉ)
- Sur ce poste Windows, `bash` passe via WSL mais aucune distro n’est installée, donc pas de test d’exécution direct.

### 5.3 Mini revalidation live (conseillée, non destructive)
Après `git pull` sur `admin-trading` :
```bash
/usr/local/bin/cmd-shared_sshfs_permanent info
/usr/local/bin/sanity-shared_sshfs_permanent || true
```
Test symlink sans toucher `/usr/local` (réversible, dans `/tmp`) :
```bash
ln -sf /opt/trading/modules/shared_sshfs_permanent/scripts/cmd.sh /tmp/cmd-shared_sshfs_permanent-test
bash /tmp/cmd-shared_sshfs_permanent-test info
ln -sf /opt/trading/modules/shared_sshfs_permanent/scripts/sanity_check.sh /tmp/sanity-shared_sshfs_permanent-test
bash /tmp/sanity-shared_sshfs_permanent-test || true
```

## 6. LIMITES RESTANTES
- Ce patch ne déploie pas `shared-sshfs.service` et ne monte pas `/shared` (hors périmètre).
- Si l’état live `admin-trading` n’a pas les scripts installés `/opt/trading/scripts/shared_sshfs_permanent_*.sh`, la délégation ne s’active pas (comportement volontaire).

## 7. FICHIERS MODIFIÉS
- `modules/shared_sshfs_permanent/scripts/cmd.sh`
- `modules/shared_sshfs_permanent/scripts/menu.sh`
- `modules/shared_sshfs_permanent/scripts/sanity_check.sh`
- `modules/shared_sshfs_permanent/README.md`

## 8. COMMANDES EXÉCUTÉES
- Tentative locale : `bash --version` (échoue car WSL sans distribution).
- Contrôles statiques : recherche de l’ancien pattern et de `readlink -f` dans les scripts.

## 9. VERDICT FINAL
Patch minimal et cohérent : les wrappers `shared_sshfs_permanent` deviennent symlink-safe et s’alignent sur le modèle d’installation, sans toucher au déploiement systemd live.

## 10. POINT DE REPRISE SUIVANT
- Mini revalidation live sur `admin-trading` (commandes ci-dessus), puis requalification OT-SVC-01 si les symptômes `name=local/path=/usr/local` et `FAIL: scripts missing` disparaissent.


## RISKS

- À qualifier.
