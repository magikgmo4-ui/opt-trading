# OT-OPS-RUNBOOK-03 — FRICTIONS CIBLE

## 1. ACCÈS DISTANT
L'opérateur (Agent) n'a pas de route réseau ou SSH vers `admin-trading`.
Le test "in situ" est donc impossible sans changer de contexte.

## 2. DÉPENDANCES SYSTÈME
Les scripts `scripts/admin_trading/*.sh` supposent un environnement Linux standard (`/bin/bash`, `cp`, `mkdir`).
Ils échouent immédiatement sur Windows sans WSL.

## 3. RISQUE RÉSIDUEL
Il reste un risque mineur sur les **Permissions Fichiers** et les **Symlinks** (`/usr/local/bin`) qui ne peuvent être vérifiés que sur la cible.
Le runbook assume que l'installation (`install_desk_pro_wrappers.sh`) a été faite correctement.
