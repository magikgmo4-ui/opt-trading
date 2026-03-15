# OT-OPS-RUNBOOK-02 — FRICTIONS ET LIMITES

## 1. ENVIRONNEMENT D'EXÉCUTION
Le runbook est conçu pour `admin-trading` (Linux).
Les tests effectués depuis un environnement Windows sans couche de compatibilité (WSL/Git Bash complet) échouent sur les commandes `bash` et les wrappers `/usr/local/bin`.

## 2. POINTS D'ATTENTION
- **Wrappers** : Les commandes `menu-ops_menu_hub`, `cmd-*` dépendent de l'installation dans `/usr/local/bin`.
- **Scripts Admin** : Les scripts `scripts/admin_trading/*.sh` nécessitent un interpréteur Bash.

## 3. RECOMMANDATION
Ne pas tenter d'exécuter ce runbook depuis un PowerShell Windows standard.
Toujours se connecter en SSH à `admin-trading` avant de commencer.
