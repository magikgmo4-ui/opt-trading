# OT-WINSHARED-01 — REPORT (CURSOR-AI / WINDOWS ACCÈS SHARED CANONIQUE)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Objectif : formaliser comment `cursor-ai` (Windows) accède à la surface canonique inter-machines “/shared”, sans créer de chemin concurrent.
- Source canonique (serveur) : `admin-trading:/srv/sftp/shared_files/shared` (SFTP chroot `/srv/sftp/shared_files`).
- Mode Windows retenu (réaliste) : WinSCP/SFTP vers le serveur `admin-trading`, dossier distant `/shared` (et sous-dossiers type `/shared/inbox`, `/shared/outbox`).
- Chemin local Windows recommandé (à confirmer sur poste) : `C:\\Users\\ghost\\Downloads\\SHARED\\`.

## 2. RÔLE DE cursor-ai
- Client Windows/GUI : dépôt/retrait de fichiers projet (zips, screenshots, bundles) via SFTP.
- Ne monte pas SSHFS ; converge vers la **même surface serveur** que les clients Linux montent sous `/shared`.

## 3. SOURCE CANONIQUE SERVEUR
- Machine : `admin-trading`
- Répertoire réel : `/srv/sftp/shared_files/shared`
- Chroot SFTP : `/srv/sftp/shared_files` (donc le répertoire partagé apparaît comme `/shared` dans la session SFTP).
- Preuves repo/journal :
  - Step “shared_files_sftp installed” : chroot `/srv/sftp/shared_files` + `shared`/`upload` (journal step 2026-03-01 10:12).
  - Step overwrite fix : WinSCP upload/overwrite validé depuis `cursor-ai` + bookmark `/upload` `/shared` (journal step 2026-03-01 17:56).

## 4. CHEMIN LOCAL WINDOWS RECOMMANDÉ
- **Recommandé (à confirmer sur poste cursor-ai)** : `C:\\Users\\ghost\\Downloads\\SHARED\\`
- Raison : cohérence avec le workflow journalisé “Unified SHARED folder” (journal step 2026-03-01 20:13).

## 5. PROCÉDURE WinSCP / KeepUpToDate (CANONIQUE)

### 5.1 Pré-requis
- Host : `admin-trading` (LAN/VPN selon config locale)
- User : compte SFTP Windows (ex: `sftp_cursor_ai`) avec clé publique installée côté serveur.
- Remote root (chroot) : `/`

### 5.2 Bookmarks distants (recommandés)
- `/shared` : surface canonique (équivalent serveur de “/shared” Linux)
- `/shared/inbox` : dépôt upload
- `/shared/outbox` : récupération (download)
- `/upload` : zone éventuelle dédiée upload (si utilisée)

### 5.3 Mode KeepUpToDate (recommandé)
- Synchroniser **Local** `C:\\Users\\ghost\\Downloads\\SHARED\\` ↔ **Remote** `/shared`
- Objectif : un seul dossier utilisateur Windows qui reflète la surface canonique serveur.

## 6. ÉLÉMENTS LEGACY/DOC À ÉVITER
- Éviter d’introduire un “deuxième shared” Windows distinct (autre répertoire distant/serveur).
- Éviter de documenter `/shared` Windows comme un mount SSHFS ; la voie canonique Windows reste SFTP/WinSCP.

## 7. FICHIERS MODIFIÉS
- Repo : ce report + closing ; mises à jour doc ciblées (voir mission).

## 8. COMMANDES EXÉCUTÉES
- Aucune commande exécutée sur le poste `cursor-ai` (pas de replay direct Windows dans cette mission).
- Sources utilisées : docs repo + journal/steps.

## 9. VERDICT FINAL
- Standard Windows défini : WinSCP/SFTP vers `admin-trading` `/shared` avec chemin local recommandé.
- Réserve : à confirmer directement sur `cursor-ai` (chemin local réellement utilisé + config KeepUpToDate et hostkey).

## 10. IMPACT SUR OT-SVC-01 ET LIGNE CANONIQUE PROJET
- Réserve “Windows” : réduite (procédure formalisée), mais pas levée sans preuve directe sur poste.

