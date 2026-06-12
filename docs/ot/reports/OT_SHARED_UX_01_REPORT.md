# OT-SHARED-UX-01 — REPORT (DOCTRINE + UX MINIMALE shared)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Doctrine `shared` (V1) formalisée et documentée : `shared` est la surface canonique inter-machines du projet.
- UX minimale livrée (Linux) : `cmd-shared` fournit `ls/get/put` (et `cat/status/path`) avec un comportement par défaut robuste.
- Aucun changement d’architecture `/shared` : compatibilité conservée avec `shared_sshfs_permanent`, `shared_files_sftp` et le flux Windows (SFTP).

## 2. MODULE CHOISI POUR PORTER L’UX
### Choix
- Module : `modules/shared`

### Justification
- Aucun `cmd-shared`/`menu-shared` n’existait ; les modules existants sont spécialisés :
  - `shared_sshfs_permanent` : montage client Linux (systemd) de `/shared`, pas une UX dépôt/récupération.
  - `shared_files_sftp` : serveur SFTP et comptes, pas une UX usage quotidien.
  - `winscp_transfer` : outillage transfert orienté workflow WinSCP/ops, pas une UX générique “je mets / je récupère”.
- Ajouter un module minimal dédié évite de mélanger “montage” et “usage” et ne casse aucun flux existant.

## 3. DOCTRINE OFFICIELLE shared (V1)
`shared` est la surface canonique inter-machines du projet.

Il sert par défaut au dépôt, à la récupération, à la livraison et au transfert des artefacts utiles entre `cursor-ai/Windows`, `admin-trading`, `db-layer`, `student`, et selon le cas les sorties générées par Trae.

`shared` est également le dossier par défaut pour les ajouts manuels liés au projet : téléchargements utiles, patchs, bundles, scripts, documents, fichiers externes reçus et livraisons intermédiaires.

Principe : tout fichier utile au projet, susceptible d’être relu, déplacé, exécuté, validé ou récupéré depuis une autre machine, doit aller par défaut dans `shared`.

Règles :
1. fichier utile au projet => `shared` par défaut
2. transfert inter-machines => `shared` comme canal normal
3. livraisons d’outils/docs/bundles/patchs => `shared`
4. racine `shared` légère ; utiliser les sous-dossiers canoniques
5. ne pas déplacer automatiquement les cas ambigus/sensibles
6. Linux client => `/shared`
7. admin-trading (source réelle) => `/srv/sftp/shared_files/shared` (alias `/shared`)
8. Windows local canonique => `C:\Users\ghost\Downloads\SHARED\`

## 4. CHEMINS CANONIQUES PAR MACHINE
### A. ÉTABLI (runtime + preuves)
- `admin-trading`
  - `/srv/sftp/shared_files/shared` (source réelle)
  - `/shared` (alias local)
- `db-layer`
  - `/shared` via `shared_sshfs_permanent`
- `student`
  - `/shared` via `shared_sshfs_permanent`
- `cursor-ai` (Windows)
  - local : `C:\Users\ghost\Downloads\SHARED\`
  - distant : SFTP vers `admin-trading`, surface `/shared`

### C. À CONFIRMER
- Aucun : les chemins ci-dessus sont alignés avec les OT précédents (Linux + Windows déjà validés).

## 5. COMMANDES AJOUTÉES / CONFIRMÉES
Wrappers déclarés :
- `cmd-shared`
- `menu-shared`
- `sanity-shared`

## 6. SYNTAXE EXACTE (ls/get/put)

### 6.1 ls
```bash
cmd-shared ls
cmd-shared ls _bundles
cmd-shared ls _ops
```

### 6.2 get
```bash
cmd-shared get README.txt .
cmd-shared get _bundles/mon_bundle.zip .
cmd-shared get --dry-run boot_test.txt /tmp/boot_test.txt
cmd-shared get --force _bundles/x.zip ./x.zip
```

### 6.3 put
```bash
cmd-shared put ./mon_patch.zip _bundles/
cmd-shared put ./note.txt _refs/
cmd-shared put --dry-run ./note.txt _refs/
cmd-shared put --force ./note.txt _refs/note.txt
```

## 7. FICHIERS MODIFIÉS
- Nouveau module :
  - `modules/shared/README.md`
  - `modules/shared/scripts/cmd.sh`
  - `modules/shared/scripts/menu.sh`
  - `modules/shared/scripts/sanity_check.sh`
- Registries :
  - `registry/modules_registry.yaml`
  - `registry/wrappers_registry.yaml`
- Standards :
  - `docs/master_pack/00_current_state_and_standards.md`

## 8. VALIDATION EFFECTUÉE
- Syntaxe bash : `bash -n` sur `cmd.sh` (sur `admin-trading` via copie temporaire).
- `ls` : listing de `/shared/_bundles` (head) OK.
- `cat` : `boot_test.txt` OK.
- `get --dry-run` : OK.
- `put --dry-run` : OK (aucune écriture réelle).

## 9. LIMITES / RÉSERVES
- L’UX `cmd-shared` est livrée pour Linux (bash). Sur Windows, l’usage quotidien reste :
  - dépôt local dans `C:\Users\ghost\Downloads\SHARED\`
  - transferts via SFTP/WinSCP vers la même surface distante `/shared`
- Les cas ambigus/sensibles ne sont pas automatisés (doctrine V1).

## 10. VERDICT FINAL
**PASS** : doctrine figée + UX minimale opérationnelle sans casser l’existant.

## 11. POINT DE REPRISE SUIVANT
- Optionnel : ajouter des garde-fous UX (ex: refuser `put` sans cible explicite vers `_bundles/_ops/_refs`), sans complexifier.


## RISKS

- À qualifier.
