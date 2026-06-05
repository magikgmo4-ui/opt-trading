# Admin Trading Desk Pro - Runbook

## 1. Objectif
Ce runbook décrit les procédures opérationnelles standard pour l'exploitation du **Desk Pro** sur la machine `admin-trading`.
Le système fonctionne en mode **PAPER** (simulation) et est piloté via une interface ligne de commande (SSH).

## 2. Pré-requis
- Accès SSH à `admin-trading`
- Utilisateur avec droits d'exécution sur `/opt/trading`
- Environnement Python 3 configuré
- Accès au montage `/shared` (pour le partage de rapports)

## 3. EntryPoints Canoniques
Hiérarchie canonique établie :

| Surface | Commande / Chemin | Rôle |
|---|---|---|
| Opérateur | `menu-ops_menu_hub` | Point d'entrée unique de session |
| Admin / debug | `scripts/admin_trading/desk_pro_cmd.sh` | Wrapper d'orchestration et utilitaires admin |
| Backend direct | `cmd-desk_pro_runner` | CLI directe vers le runner |
| Legacy compat | `scripts/desk_pro_*.sh` | Compatibilité uniquement, ne pas promouvoir |

## 4. Commandes Admin Réelles
Les commandes suivantes sont celles à utiliser sur `admin-trading` :

| Commande | Description |
|---|---|
| `menu-ops_menu_hub` | Menu opérateur canonique |
| `scripts/admin_trading/desk_pro_cmd.sh status` | Vérifier l'état du runner |
| `scripts/admin_trading/desk_pro_cmd.sh run-logged` | Lancer un run avec log complet |
| `scripts/admin_trading/desk_pro_cmd.sh tail-latest-log` | Voir la fin du dernier log |
| `scripts/admin_trading/desk_pro_cmd.sh last-run-info` | Infos sur la dernière exécution |
| `scripts/admin_trading/desk_pro_cmd.sh show-session-journal` | Lire le journal de session |
| `scripts/admin_trading/desk_pro_cmd.sh add-session-note "..."` | Ajouter une note de session |
| `scripts/admin_trading/desk_pro_cmd.sh copy-latest-to-shared` | Copier les résultats vers `/shared` |

## 5. Flux Opérateur : Début de Session

1. **Connexion SSH**
   ```bash
   ssh user@admin-trading
   ```

2. **Ouverture opérateur canonique**
   ```bash
   menu-ops_menu_hub
   ```

3. **Vérification de Santé / Statut**
   ```bash
   scripts/admin_trading/desk_pro_cmd.sh status
   ```
   *Attendu : état runner exploitable.*

4. **Vérification du Dernier État**
   ```bash
   scripts/admin_trading/desk_pro_cmd.sh last-run-info
   ```
   *Vérifier la date et le statut du dernier run.*

5. **Ouverture du Journal de Session**
   ```bash
   scripts/admin_trading/desk_pro_cmd.sh add-session-note "Début de session opérateur."
   scripts/admin_trading/desk_pro_cmd.sh show-session-journal
   ```

## 6. Flux Opérateur : Exécution (Run)

1. **Lancer un Run Loggé (Recommandé)**
   ```bash
   scripts/admin_trading/desk_pro_cmd.sh run-logged
   ```
   *Ceci lance l'orchestrateur, génère un log horodaté, et met à jour les liens `latest`.*

2. **Suivre l'Exécution (si besoin)**
   ```bash
   scripts/admin_trading/desk_pro_cmd.sh tail-latest-log
   ```

3. **Vérifier le Résultat**
   ```bash
   scripts/admin_trading/desk_pro_cmd.sh last-run-info
   ```
   *Attendu : Status SUCCESS, run_summary.json Present*

4. **Visualiser le Dashboard**
   ```bash
   cmd-desk_pro_runner dashboard-latest
   ```
   *Affiche le résumé du portefeuille dans le terminal.*

## 7. Flux Opérateur : Fin de Session

1. **Export et Partage**
    ```bash
    # Générer le rapport HTML
    scripts/admin_trading/desk_pro_cmd.sh export-html-latest
    
    # Copier vers le partage réseau
    scripts/admin_trading/desk_pro_cmd.sh copy-latest-to-shared
    ```

2. **Note de Fin**
    ```bash
    scripts/admin_trading/desk_pro_cmd.sh add-session-note "Fin de session. Run OK, rapport partagé."
    ```

3. **Déconnexion**
   ```bash
   exit
   ```

## 8. Gestion des Incidents Courants

### Cas : Run FAILED
1. **Consulter les logs** : `scripts/admin_trading/desk_pro_cmd.sh tail-latest-log`
2. **Identifier le module en erreur** (ex: market_scanner, risk_engine)
3. **Vérifier les configs** dans `modules/<module>/config/`
4. **Revalider l'entrée admin** : `scripts/admin_trading/desk_pro_cmd.sh status`

### Cas : /shared inaccessible
1. **Vérifier le montage** : `ls -ld /shared`
2. **Si absent**, les copies échoueront mais le run local reste valide.
3. **Action** : Signaler à l'admin système, ou récupérer les rapports manuellement dans `data/dashboard/`.

## 9. Emplacements Clés

- **Racine Repo** : `/opt/trading` (typique)
- **Logs Exécution** : `data/logs/desk_pro/`
  - `latest.log` : Lien vers le dernier log
- **Runs Orchestrator** : `data/desk_runs/`
- **Rapports Dashboard** : `data/dashboard/`
- **Journal Session** : `data/logs/desk_pro/session_journal.log`
- **Partage** : `/shared/desk_pro/latest/`

---
*Dernière mise à jour : 2026-03-06*

## RISKS

- À qualifier.
