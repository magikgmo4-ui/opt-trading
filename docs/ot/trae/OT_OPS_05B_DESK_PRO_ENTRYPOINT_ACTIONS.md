# OT-OPS-05B — ACTIONS DE SÉCURISATION (DESK PRO)

## 1. MISE À JOUR DOCUMENTAIRE (MASTER PACK)
Mettre à jour `docs/master_pack/00_current_state_and_standards.md` pour clarifier la hiérarchie des entrypoints Desk Pro :
- Officialiser `menu-ops_menu_hub` comme entrypoint opérateur.
- Officialiser `scripts/admin_trading/` comme couche d'administration.
- Marquer `scripts/desk_pro_*.sh` comme Legacy/Compatibilité.

## 2. SIGNALISATION LOCALE (ADMIN TRADING)
Ajouter un `README_ENTRYPOINTS.md` dans `scripts/admin_trading/` pour expliquer que ce dossier est le véritable pilote de l'orchestrateur sur cette machine.

## 3. SIGNALISATION LOCALE (ROOT SCRIPTS)
(Optionnel) Ajouter un commentaire en tête de `scripts/desk_pro_cmd.sh` rappelant qu'il est legacy, mais sans modifier le code fonctionnel pour éviter tout risque.

## 4. PRINCIPE DE STABILITÉ
L'objectif est de figer l'usage, pas de changer le code.
On ne touche pas aux fichiers, on change la façon dont on les documente.
