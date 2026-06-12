# OT-OPS-RUNBOOK-01 — RAPPORT DE CRÉATION

## 1. FLUX RETENU
Le flux "Hub Centric" a été choisi car il masque la complexité des appels CLI individuels et guide l'opérateur.
Cependant, les commandes directes (`scripts/admin_trading/...`) sont maintenues pour les étapes de clôture/archivage qui ne sont pas encore dans le Hub.

## 2. POINTS D'ENTRÉE ÉCARTÉS
- **`scripts/desk_pro_cmd.sh`** : Écarté car ambigu et limité (simple wrapper legacy).
- **Appels Python directs** : Écartés pour éviter les erreurs de PYTHONPATH.
- **Wrappers individuels** : Mentionnés mais subordonnés au Hub pour simplifier la doc.

## 3. STATUT DU RUNBOOK
Ce runbook est **OPÉRATIONNEL IMMÉDIAT**.
Il reflète l'état réel du système au 2026-03-12.

## 4. PROCHAINE AMÉLIORATION POSSIBLE
Intégrer les fonctions `add-session-note` et `copy-latest-to-shared` directement dans le `menu-ops_menu_hub` pour éliminer le besoin de revenir au shell en fin de session.

## RISKS

- À qualifier.
