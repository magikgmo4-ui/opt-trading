# OT-OPS-05 — ACTIONS DE SÉCURISATION (RUNTIME)

## 1. MISE À JOUR DOCUMENTAIRE (MASTER PACK)
Mettre à jour `docs/master_pack/00_current_state_and_standards.md` pour inclure les nouvelles catégories d'exceptions identifiées :
- **Reseau SSH** : Classé comme exception (Runtime dans `scripts/`).
- **Runtime Layers** : Reconnaissance officielle des dossiers `scripts/admin_trading/`, `scripts/db_layer/` comme couches d'intégration légitimes.

## 2. SIGNALISATION LOCALE (RESEAU SSH)
Ajouter un fichier `README_RUNTIME.md` (ou mise à jour du README existant) dans `scripts/reseau_ssh/` pour confirmer qu'il est la source de vérité active, afin d'éviter qu'un développeur ne tente de redéployer le module imbriqué par erreur.

## 3. GESTION DE L'AMBIGUÏTÉ (DESK PRO ROOT)
Ne pas supprimer `scripts/desk_pro_*.sh` (risque de casser des cronjobs ou habitudes), mais documenter dans le Master Pack que les **Wrappers Globaux** (`/usr/local/bin/...`) sont la seule méthode d'invocation supportée officiellement.

## 4. PRINCIPE DE NON-INTERVENTION
- **Pas de migration** de `scripts/reseau_ssh/` vers `modules/`.
- **Pas de fusion** de `scripts/admin_trading/` avec `modules/desk_pro/`.
- **Pas de suppression** de `scripts/desk_pro_*.sh`.

L'objectif est de figer la connaissance, pas de refactorer le code.
