# OT-OPS-RUNBOOK-01 — ADMIN TRADING DESK PRO

Ce document définit la procédure standard pour l'opérateur Desk Pro sur la machine `admin-trading`.

## 1. OBJECTIF
Assurer une session de trading quotidienne fiable, répétable et tracée, en utilisant les entrypoints canoniques validés.

## 2. PRÉREQUIS
- **Machine** : `admin-trading` (Linux)
- **Utilisateur** : `ghost` (ou user standard)
- **Accès** : Terminal local ou SSH

## 3. POINT D'ENTRÉE RECOMMANDÉ
Pour 90% des usages, utiliser le **Hub Opérateur** :
```bash
menu-ops_menu_hub
```
Ce menu centralise les outils, dashboards et maintenances.

## 4. ROUTINE QUOTIDIENNE (FLUX CANONIQUE)

### Étape 1 : Ouverture de Session (Santé)
Avant de lancer quoi que ce soit, vérifier que la machine est saine.
1. Lancer `menu-ops_menu_hub`.
2. Aller dans **4. Maintenance & Sanity**.
3. Exécuter **2. Sanity: Runner** (`sanity-desk_pro_runner`).
   - Si `PASS` : Continuer.
   - Si `FAIL` : Ne pas trader. Consulter les logs.

### Étape 2 : Lancement du Run (Orchestration)
1. Dans le Hub, aller dans **1. Operator Tools**.
2. Sélectionner **1. Run Desk Pro** (`cmd-desk_pro_runner`).
   - Cela lance l'analyse complète (Probabilités, Décisions, Risque).
   - Attendre la fin du processus (quelques secondes/minutes).

### Étape 3 : Contrôle Visuel (Dashboard)
1. Toujours dans **1. Operator Tools**.
2. Sélectionner **4. Show Dashboard**.
   - Vérifier les indicateurs clés (Risque, Positions, Alertes).
   - Valider que le `run_id` correspond bien à l'exécution de l'étape 2.

### Étape 4 : Journalisation (Optionnel mais Recommandé)
Pour noter un événement ou une observation manuelle :
1. Quitter le Hub (`0. Exit`).
2. Utiliser la commande admin directe pour voir les infos du dernier run :
   ```bash
   bash scripts/admin_trading/desk_pro_cmd.sh last-run-info
   ```
3. Ajouter une note :
   ```bash
   bash scripts/admin_trading/desk_pro_cmd.sh add-session-note "Observation ici"
   ```

### Étape 5 : Clôture / Archivage
En fin de session, pour assurer que les données sont sauvegardées :
1. Utiliser la commande admin directe :
   ```bash
   bash scripts/admin_trading/desk_pro_cmd.sh copy-latest-to-shared
   ```
   - Cela pousse les résultats vers le dossier partagé (accessible par `msi_db_layer` ou `student`).

## 5. INCIDENTS FRÉQUENTS & RÉSOLUTIONS

| Symptôme | Cause Probable | Action |
| :--- | :--- | :--- |
| **Erreur "Module not found"** | Mauvais entrypoint | Utiliser `menu-ops_menu_hub` ou les scripts dans `scripts/admin_trading/`. |
| **Dashboard vide** | Run non effectué | Relancer **Run Desk Pro** (Étape 2). |
| **Permission denied** | Mauvais user | Vérifier `whoami`. Ne jamais utiliser `sudo` sauf install. |

## 6. À NE PAS FAIRE (PIÈGES)
- **NE PAS LANCER** `scripts/desk_pro_cmd.sh` (Script racine legacy). Il est incomplet.
- **NE PAS LANCER** `python -m modules.desk_pro` directement. Ce module est une librairie.
- **NE PAS MODIFIER** les fichiers dans `modules/` pendant une session active.

## 7. RECAP ENTRYPOINTS
- **Quotidien** : `menu-ops_menu_hub`
- **Admin Avancé** : `scripts/admin_trading/desk_pro_cmd.sh`
- **Debug Rapide** : `cmd-desk_pro_runner status`

## RISKS

- À qualifier.
