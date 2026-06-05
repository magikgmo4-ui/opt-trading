# OT-ROLL-SSHFS-02 — ARCHITECTURE (/shared STANDARD INTER-MACHINES)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- `/shared` est retenu comme **surface canonique** de transfert inter-machines.
- `admin-trading` est la **source canonique** (répertoire serveur réel), et les clients Linux montent `/shared` via `shared_sshfs_permanent`.
- `db-layer` et `student` sont **alignés et prouvés live** (service systemd + mount `/shared`).
- `cursor-ai` (Windows/GUI) reste aligné via **WinSCP/SFTP** vers la même source serveur (pas de création d’un autre “shared”).

## 2. DOCTRINE CANONIQUE RETENUE
- **Source unique** : `/srv/sftp/shared_files/shared` (sur `admin-trading`)
- **Alias local toléré** : `/shared` sur `admin-trading` peut rester un alias (symlink) vers la source.
- **Clients Linux** : montent la source sur **`/shared`** via `shared_sshfs_permanent` (systemd `shared-sshfs.service`).
- **Windows/GUI** : accède à la même source via WinSCP/SFTP et travaille dans un dossier local “SHARED” synchronisé, sans introduire d’autre surface concurrente.

## 3. MATRICE MACHINES → RÔLE → ACCÈS SHARED

| Machine | Rôle | Chemin canonique exposé | Mode d’accès recommandé | Preuve |
| :--- | :--- | :--- | :--- | :--- |
| `admin-trading` | Source/Export | `/srv/sftp/shared_files/shared` (alias `/shared`) | SFTP (serveur) + filesystem local | Live (`/shared` symlink, perms serveur) |
| `db-layer` | Client Linux | `/shared` | `shared_sshfs_permanent` (`shared-sshfs.service`) | Live (`findmnt /shared`, service actif) |
| `student` | Client Linux | `/shared` | `shared_sshfs_permanent` (`shared-sshfs.service`) | Live (`findmnt /shared`, service actif) |
| `cursor-ai` | Client Windows/GUI | même source serveur | WinSCP keepuptodate / SFTP vers `.../shared` | Partiel (preuves indirectes + docs) |

## 4. ÉTAT LIVE PAR MACHINE (SYNTHÈSE)

### 4.1 admin-trading (source)
- `/shared` : symlink vers `/srv/sftp/shared_files/shared`
- Répertoire source : `/srv/sftp/shared_files/shared` (group/perms SFTP)

### 4.2 db-layer (client Linux)
- `shared-sshfs.service` : enabled + active
- `/shared` : monté (sshfs) depuis `ghost@admin-trading:/srv/sftp/shared_files/shared`

### 4.3 student (client Linux)
- `shared-sshfs.service` : enabled + active
- `/shared` : monté (sshfs) depuis `ghost@admin-trading:/srv/sftp/shared_files/shared`

### 4.4 cursor-ai (Windows/GUI)
- Mode recommandé : WinSCP/SFTP vers `admin-trading` (distant SFTP `/shared`).
- Preuve partielle : fichiers présents sur la source serveur avec propriétaire `sftp_cursor_ai` (indique un flux Windows effectif vers la même surface).
- Chemin local Windows canonique (établi sur poste) : `C:\\Users\\ghost\\Downloads\\SHARED\\`.
- Note : WinSCP/KeepUpToDate n’est pas établi sur poste (WinSCP non présent/config non détectée) ; SFTP OpenSSH validé.

## 5. MÉCANISMES COEXISTANTS (CLASSIFICATION)
- **STANDARD CANONIQUE** :
  - `shared_files_sftp` (serveur) : maintenu comme source d’exposition.
  - `shared_sshfs_permanent` (clients Linux) : montages `/shared` via systemd.
- **LEGACY ENCORE UTILISÉ** :
  - `winscp_transfer` : utile côté Windows et pour push/pull modules (inbox/outbox) sans casser l’unification de surface.
- **LEGACY REMPLAÇABLE / À ÉVITER** :
  - mounts “par utilisateur” vers d’autres chemins (ex: `~/Téléchargements/SHARED`) si `/shared` est déjà monté et prouvé stable.

## 6. LIGNE CANONIQUE PROJET
`/shared` est le standard inter-machines : `admin-trading` expose `/srv/sftp/shared_files/shared`, les clients Linux montent cette source sur `/shared` via `shared_sshfs_permanent`, et Windows accède à la même surface via WinSCP/SFTP.

## RISKS

- À qualifier.
