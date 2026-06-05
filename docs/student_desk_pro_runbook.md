# Student Desk Pro - Runbook

## 1. Objectif
Ce document guide l'opérateur pour utiliser le pack **Desk Pro Student** sur la machine `student` (Linux Headless).
Le rôle principal est la **consultation** des analyses produites par `admin-trading` et la vérification de l'état local.

## 2. Pré-requis
- Accès SSH à `student`
- Montage `/shared` actif (pour lire les résultats d'`admin-trading`)
- Pack `desk-pro-student` installé

## 3. Commandes Globales
Les wrappers suivants sont disponibles après installation :

| Commande | Description |
|---|---|
| `desk-pro-student` | Wrapper principal (status, summary) |
| `menu-desk-pro-student` | Menu interactif simple |
| `sanity-desk-pro-student` | Vérification de l'environnement local |
| `desk-pro-student-shared-info` | Lire les derniers résultats partagés |

## 4. Flux Opérateur : Consultation Quotidienne

1. **Connexion SSH**
   ```bash
   ssh user@student
   ```

2. **Vérification de Santé**
   ```bash
   sanity-desk-pro-student
   ```
   *Attendu : "Student Sanity Check Passed"*

3. **Lire les Résultats du Hub (Admin)**
   ```bash
   desk-pro-student-shared-info
   ```
   *Affiche le résumé du dernier run, l'état du portefeuille et les risques, lus depuis `/shared/desk_pro/latest`.*

4. **Vérifier l'État Local**
   ```bash
   desk-pro-student status
   ```

## 5. Gestion des Incidents Courants

### Cas : Shared Info Vide / Missing
**Symptôme** : `desk-pro-student-shared-info` retourne "WARN: Shared directory not found".
**Diagnostic** :
1. Le montage NFS/SSHFS vers `admin-trading` est tombé.
2. `admin-trading` n'a pas encore exporté de run.

**Action** :
1. Vérifier le montage : `ls -ld /shared`
2. Si le montage est OK, attendre qu'`admin-trading` termine un run et fasse un `copy-latest`.

### Cas : Command not found
**Action** :
1. Réinstaller les wrappers :
   ```bash
   sudo ./scripts/student/desk_pro_student_install.sh
   ```

## 6. Emplacements Clés

- **Racine Repo** : `/opt/trading` (typique)
- **Partage Lecture** : `/shared/desk_pro/latest/`
- **Scripts Student** : `scripts/student/`

---
*Dernière mise à jour : 2026-03-06*

## RISKS

- À qualifier.
