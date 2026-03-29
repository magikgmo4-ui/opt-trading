# Admin Trading Desk Pro - Incident Recovery Runbook

## 1. Objectif
Ce document guide l'opérateur pour restaurer le service Desk Pro sur `admin-trading` en cas de dysfonctionnement.
Il couvre les pannes courantes rencontrées en mode **PAPER** (simulation).

## 2. Périmètre
- **Machine** : `admin-trading` (Linux Headless)
- **Service** : Desk Pro (Orchestrator, Runner, Dashboard)
- **Interfaces** : CLI, Wrappers globaux, Partage `/shared`

## 3. Diagnostic Rapide
En cas de doute, exécutez ces commandes dans l'ordre :

1. **Vérifier l'intégrité globale**
   ```bash
   sanity-desk_pro
   ```
   *Doit retourner "Admin Sanity Check Passed".*

2. **Vérifier le dernier état connu**
   ```bash
   desk-pro-summary
   ```
   *Vérifier si le dernier run est SUCCESS ou FAILED.*

3. **Lire le dernier log d'erreur**
   ```bash
   desk-pro-tail-log
   ```

## 4. Scénarios de Reprise

### A. Run KO (Échec d'exécution)
**Symptôme** : `desk-pro-run-logged` affiche "Run FAILED".
**Diagnostic** :
1. Lire le log : `desk-pro-tail-log`
2. Identifier le module fautif (ex: `market_scanner`, `risk_engine`).
3. Vérifier si c'est une erreur de configuration (JSON invalide) ou de code.

**Reprise** :
1. Si erreur config : corriger le fichier JSON dans `modules/<module>/config/`.
2. Si erreur temporaire : relancer un run simple.
   ```bash
   desk-pro-run-logged
   ```
3. Valider avec `desk-pro-last-run`.

### B. Dashboard Vide ou Obsolète
**Symptôme** : `desk-pro dashboard-latest` ne montre rien ou des données anciennes.
**Diagnostic** :
1. Vérifier si un run récent a réussi : `desk-pro-last-run`
2. Si le run est vieux, le dashboard est logiquement obsolète.
3. Si le run est récent mais sans dashboard : le fichier `portfolio_engine.json` est peut-être corrompu.

**Reprise** :
1. Forcer un nouveau run complet.
   ```bash
   desk-pro-run-logged
   ```
2. Vérifier l'affichage immédiat.
   ```bash
   desk-pro dashboard-latest
   ```

### C. /shared Absent ou Non Mis à Jour
**Symptôme** : Les autres machines ne voient pas les nouveaux rapports.
**Diagnostic** :
1. Vérifier le montage sur admin-trading.
   ```bash
   ls -ld /shared
   ```
2. Tenter une copie manuelle et lire l'erreur.
   ```bash
   desk-pro-copy-latest
   ```

**Reprise** :
1. Si `/shared` est démonté : contacter l'admin système (hors périmètre Desk Pro).
2. Si `/shared` est là mais la copie échoue (permissions) : vérifier les droits.
3. Workaround temporaire : récupérer les rapports dans `data/dashboard/` via SCP.

### D. Wrappers Globaux Absents (Command not found)
**Symptôme** : `desk-pro` ou `sanity-desk_pro` introuvable.
**Diagnostic** :
1. Vérifier le PATH.
2. Vérifier `/usr/local/bin`.

**Reprise** :
1. Relancer l'installation des wrappers (nécessite sudo).
   ```bash
   cd /opt/trading
   sudo ./scripts/admin_trading/desk_pro_install_admin_trading.sh
   ```

### E. Log Absent / latest.log Incohérent
**Symptôme** : `desk-pro-tail-log` échoue.
**Diagnostic** :
1. Le lien symbolique `data/logs/desk_pro/latest.log` est peut-être cassé.

**Reprise** :
1. Lancer un nouveau run loggé pour régénérer le lien proprement.
   ```bash
   desk-pro-run-logged
   ```

### F. Reprise Après Patch Git (Pull)
**Contexte** : Après un `git pull`, le système semble instable.
**Reprise** :
1. Vérifier la structure des dossiers.
   ```bash
   sanity-desk_pro
   ```
2. Si des wrappers ont changé, réinstaller.
   ```bash
   sudo ./scripts/admin_trading/desk_pro_install_admin_trading.sh
   ```
3. Lancer un run de validation.
   ```bash
   desk-pro-run-logged
   ```

## 5. Journalisation de l'Incident
Toute reprise doit être notée dans le journal de session pour traçabilité.

```bash
desk-pro add-session-note "INCIDENT: Run échoué cause X. ACTION: Correctif Y appliqué. VALIDATION: Run Z OK."
```

## 6. Checklist de Clôture
Avant de rendre la main :
- [ ] `sanity-desk_pro` est PASS.
- [ ] Le dernier run est SUCCESS.
- [ ] Le dashboard s'affiche.
- [ ] La copie vers `/shared` fonctionne.
- [ ] L'incident est noté dans le journal de session.
