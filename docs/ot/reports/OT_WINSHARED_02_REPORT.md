# OT-WINSHARED-02 — REPORT (VALIDATION DIRECTE CURSOR-AI)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Poste `cursor-ai` (Windows) validé directement : un dossier local unique `C:\Users\ghost\Downloads\SHARED\` existe et sert de surface utilisateur.
- Accès distant canonique validé : SFTP vers `admin-trading` en user `sftp_cursor_ai`, root chroot `/` contenant `/shared`.
- Lecture/transfer non destructif validé : listing `/shared` + download de `/shared/boot_test.txt` (contenu conforme à la copie locale).
- KeepUpToDate WinSCP : **NON ÉTABLI SUR POSTE** (WinSCP non présent, aucune config/sessions détectées).

## 2. POSTE INSPECTÉ
- Host Windows : `DESKTOP-1KDQTBH`
- User : `ghost`

## 3. CHEMIN LOCAL VALIDÉ
### A. ÉTABLI SUR POSTE
- Chemin canonique : `C:\Users\ghost\Downloads\SHARED\`
- Statut : présent (dossier), contient des artefacts alignés sur `/shared` (ex: `boot_test.txt`, bundles zip).

### C. À CONFIRMER
- Aucun autre dossier `SHARED` concurrent n’a été observé dans le profil (scan limité profondeur 4).

## 4. SOURCE DISTANTE VALIDÉE
### A. ÉTABLI SUR POSTE
- Serveur : `admin-trading`
- User SFTP : `sftp_cursor_ai`
- Root SFTP : `/` (chroot) exposant `/shared`, `/inbox`, `/outbox`, `/upload`
- Chemin distant canonique : `/shared`

## 5. TEST(S) OPÉRATOIRES RÉALISÉS
### A. ÉTABLI SUR POSTE
- Connexion SSH (shell) vers `admin-trading` en user `ghost` : OK (preuve connectivité).
- Connexion SFTP vers `admin-trading` en user `sftp_cursor_ai` : OK.
- Listing `/shared` : OK.
- Download non destructif : `get /shared/boot_test.txt` vers un fichier temporaire local : OK.
- Cohérence : contenu `boot-test` identique entre copie locale `Downloads\SHARED\boot_test.txt` et fichier téléchargé.

### B. ÉTABLI INDIRECTEMENT
- Le flux Windows vers la surface canonique est cohérent avec la doctrine : la session SFTP expose `/shared` (même surface que montages Linux).

## 6. KeepUpToDate : ÉTAT
### C. À CONFIRMER / NON ÉTABLI
- WinSCP n’est pas trouvé sur le poste (pas de `WinSCP.exe` dans PATH, ni en Program Files, ni binaire portable dans le profil).
- Aucune clé registre “WinSCP Sessions” et aucun `WinSCP.ini` trouvé aux emplacements usuels.
- Conclusion : KeepUpToDate WinSCP ne peut pas être validé ici (probablement non installé / non utilisé actuellement).

## 7. ÉLÉMENTS LEGACY / AMBIGUÏTÉS
- À éviter : introduire un second dossier local “shared” concurrent.
- Note : l’absence de WinSCP ne bloque pas l’accès (SFTP OpenSSH fonctionne), mais empêche de valider un workflow GUI KeepUpToDate.

## 8. FICHIERS MODIFIÉS (REPO)
- `OT_WINSHARED_02_REPORT.md`
- `OT_WINSHARED_02_CLOSING.txt`
- Ajustements doc ciblés (standards + arch + README) pour refléter “ÉTABLI SUR POSTE”.

## 9. COMMANDES EXÉCUTÉES (SUR POSTE)
- Inspection local :
  - `Test-Path/Get-Item/Get-ChildItem` sur `C:\Users\ghost\Downloads\SHARED\`
  - scan limité de répertoires `SHARED` (profondeur 4)
- Validation distante :
  - `ssh -o BatchMode=yes admin-trading 'hostname; whoami'`
  - `sftp -b <batch> sftp_cursor_ai@admin-trading` (pwd + ls / + ls /shared)
  - `sftp get /shared/boot_test.txt <tmp>`

## 10. VERDICT FINAL
- **PASS** : chemin local canonique validé et accès SFTP canonique confirmé.
- **PASS AVEC NOTE** : KeepUpToDate WinSCP non validable car WinSCP non présent/config non détectée.

## 11. IMPACT SUR OT-SVC-01 ET LIGNE CANONIQUE PROJET
- Réserve “poste Windows” : **levée** (accès direct prouvé, chemin local validé).
- Réserve restante : reconnexion réseau “pure” côté Linux (interface/firewall) et/ou décision d’outillage WinSCP (si GUI KeepUpToDate requis).


## RISKS

- À qualifier.
