# Admin Trading Desk Pro - Runbook

## 1. Objectif
Ce runbook décrit les procédures opérationnelles standard pour l'exploitation du **Desk Pro** sur la machine `admin-trading`.
Le système fonctionne en mode **PAPER** (simulation) et est piloté via une interface ligne de commande (SSH).

## 2. Pré-requis
- Accès SSH à `admin-trading`
- Utilisateur avec droits d'exécution sur `/opt/trading`
- Environnement Python 3 configuré
- Accès au montage `/shared` (pour le partage de rapports)

## 3. Commandes Globales
Les wrappers suivants sont disponibles dans le PATH (`/usr/local/bin`) après installation :

| Commande | Description |
|---|---|
| `desk-pro` | Point d'entrée principal (wrapper runner) |
| `menu-desk-pro` | Menu interactif complet (Ops Menu) |
| `sanity-desk-pro` | Vérification de santé du système |
| `desk-pro-run-logged` | Lancer un run avec log complet |
| `desk-pro-tail-log` | Voir la fin du dernier log |
| `desk-pro-last-run` | Infos sur la dernière exécution |
| `desk-pro-session-journal` | Gérer le journal de session opérateur |
| `desk-pro-copy-latest` | Copier les résultats vers `/shared` |

## 4. Flux Opérateur : Début de Session

1. **Connexion SSH**
   ```bash
   ssh user@admin-trading
   ```

2. **Vérification de Santé**
   ```bash
   sanity-desk-pro
   ```
   *Attendu : "Admin Sanity Check Passed"*

3. **Vérification du Dernier État**
   ```bash
   desk-pro-last-run
   ```
   *Vérifier la date et le statut du dernier run.*

4. **Ouverture du Journal de Session**
   ```bash
   desk-pro add-session-note "Début de session opérateur."
   desk-pro show-session-journal
   ```

## 5. Flux Opérateur : Exécution (Run)

1. **Lancer un Run Loggé (Recommandé)**
   ```bash
   desk-pro-run-logged
   ```
   *Ceci lance l'orchestrateur, génère un log horodaté, et met à jour les liens `latest`.*

2. **Suivre l'Exécution (si besoin)**
   ```bash
   desk-pro-tail-log
   ```

3. **Vérifier le Résultat**
   ```bash
   desk-pro-last-run
   ```
   *Attendu : Status SUCCESS, run_summary.json Present*

4. **Visualiser le Dashboard**
   ```bash
   desk-pro dashboard-latest
   ```
   *Affiche le résumé du portefeuille dans le terminal.*

## 6. Flux Opérateur : Fin de Session

1. **Export et Partage**
   ```bash
   # Générer le rapport HTML
   desk-pro export-html-latest
   
   # Copier vers le partage réseau
   desk-pro-copy-latest
   ```

2. **Note de Fin**
   ```bash
   desk-pro add-session-note "Fin de session. Run OK, rapport partagé."
   ```

3. **Déconnexion**
   ```bash
   exit
   ```

## 7. Gestion des Incidents Courants

### Cas : Run FAILED
1. **Consulter les logs** : `desk-pro-tail-log`
2. **Identifier le module en erreur** (ex: market_scanner, risk_engine)
3. **Vérifier les configs** dans `modules/<module>/config/`
4. **Relancer un sanity check** : `sanity-desk-pro`

### Cas : /shared inaccessible
1. **Vérifier le montage** : `ls -ld /shared`
2. **Si absent**, les copies échoueront mais le run local reste valide.
3. **Action** : Signaler à l'admin système, ou récupérer les rapports manuellement dans `data/dashboard/`.

## 8. Emplacements Clés

- **Racine Repo** : `/opt/trading` (typique)
- **Logs Exécution** : `data/logs/desk_pro/`
  - `latest.log` : Lien vers le dernier log
- **Runs Orchestrator** : `data/desk_runs/`
- **Rapports Dashboard** : `data/dashboard/`
- **Journal Session** : `data/logs/desk_pro/session_journal.log`
- **Partage** : `/shared/desk_pro/latest/`

---
*Dernière mise à jour : 2026-03-06*
