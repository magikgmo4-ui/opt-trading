# OT-ROLL-SSHFS-02 — CLEANUP REPORT (RÉDUCTION CHEMINS CONCURRENTS)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Aucun mécanisme “shared” n’a été supprimé sans preuve.
- Côté Linux clients : la normalisation converge vers un **seul point** `/shared` monté via `shared_sshfs_permanent`.
- Côté Windows/GUI : WinSCP/SFTP reste la voie réaliste, mais doit pointer vers la **même surface serveur**.
- Cleanup technique supplémentaire dans cette mission : **packaging/registry** (clarification, pas de suppression runtime).

## 2. MÉCANISMES LEGACY INVENTORIÉS
- `winscp_transfer` : encore utile (Windows → inbox, push/pull modules). À conserver.
- Mounts legacy alternatifs (ex: `~/Téléchargements/SHARED`) : à éviter si `/shared` est disponible ; un cas redondant a déjà été retiré réversiblement sur `db-layer` (OT-DEPLOY-SSHFS-01).

## 3. ÉLÉMENTS RETIRÉS (OT-ROLL-SSHFS-02)
- Aucun retrait destructif dans cette mission.

## 4. ÉLÉMENTS CONSERVÉS
- `shared_files_sftp` : source d’exposition serveur, nécessaire.
- `winscp_transfer` : nécessaire pour Windows/GUI et opérations de push/pull.
- `shared_sshfs_permanent` : standard client Linux.

## 5. FICHIERS MODIFIÉS (REPO)
- `registry/modules_registry.yaml` : cible machine corrigée et description alignée “clients Linux”.
- `registry/wrappers_registry.yaml` : ajout des wrappers `cmd/menu/sanity-shared_sshfs_permanent`.
- `docs/master_pack/00_current_state_and_standards.md` : ajout section standard transfert `/shared`.
- `OT_SVC_01_CANONICAL_RUNTIME_MAP.md` : “clients Linux” + preuve `student`.

## 6. COMMANDES EXÉCUTÉES
- Audits non destructifs via SSH : `findmnt`, `systemctl status/is-active`, `sanity-shared_sshfs_permanent`, listing `/shared`.

## 7. VERDICT FINAL
Cleanup conforme : réduction des chemins concurrents par clarification et packaging, sans supprimer de mécanismes encore utiles ou ambigus.


## RISKS

- À qualifier.
