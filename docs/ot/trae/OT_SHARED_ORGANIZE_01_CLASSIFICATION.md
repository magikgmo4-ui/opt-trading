# OT-SHARED-ORGANIZE-01 — CLASSIFICATION (ÉTAT ACTUEL /shared)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- Inventaire racine `/shared` (source admin-trading) : **11 dossiers** + **91 fichiers** à plat.
- Les dossiers critiques pipeline sont identifiés et doivent rester à la racine.
- La majorité des fichiers à plat est reclassable vers `_bundles/` (zips) et `_ops/` (scripts), sans casser de flux.
- Deux artefacts à risque existent à la racine : `.ssh.zip` (potentiellement sensible) et `.venv.zip` (volumineux, probablement accidentel) → **AMBIGU / À CONFIRMER**.

## 2. LÉGENDE (CATÉGORIES)
- A. RÉSERVÉ / SYSTÈME / PIPELINE (ne pas bouger)
- B. STABLE / CANONIQUE (peut rester, déplacement seulement si preuve)
- C. RECLASSABLE (déplaçable plus tard sans risque apparent)
- D. ARCHIVABLE (ancien/doublon, déplacer plus tard vers `_archives/`)
- E. AMBIGU / À CONFIRMER (ne pas bouger, nécessite preuve)
- F. HORS PÉRIMÈTRE (ne pas traiter dans le rangement /shared sans décision)

## 3. INVENTAIRE RACINE ACTUEL (SOURCE)

### 3.1 Dossiers (maxdepth 1)
- `desk_pro/`
- `documents/`
- `_git_archives/`
- `inbox/`
- `_logs/`
- `modules/`
- `outbox/`
- `vision_inbox/`
- `vision_outbox/`
- `vision_processed/`
- `windows/`

### 3.2 Fichiers (maxdepth 1)
Fichiers présents à plat (extraits représentatifs + patterns) :
- Docs/sentinelles : `README.txt`, `boot_test.txt`, `audit_opt_trading_branches.md`
- Scripts `.sh` : `bridge_vision_to_desk_inbox.sh`, `install_desk_bridge_timer.sh`, `prep_commit_admin_trading.sh`, `bv2_*.sh`, `check_*.sh`
- Zips “bundles/packs/patches” : `*_bundle*.zip`, `*_pack*.zip`, `*_patch*.zip`, `install_module_*.zip`, `desk_*step*.zip`, `ops_*.zip`, `registry_*.zip`, `ui_*.zip`, `vision_*patch*.zip`, etc.
- Artefacts à risque : `.ssh.zip`, `.venv.zip`

## 4. DOSSIERS RÉSERVÉS / STABLES (CLASSIFICATION)

| Dossier | Catégorie | Rôle actuel | Preuve (repo/runtime) | Recommandation |
| :--- | :---: | :--- | :--- | :--- |
| `inbox/` | A | Entrée transfert + inbox ingestion snapshots | `desk_snapshot_ingest` utilise `.../shared/inbox` + `_processed` | Ne pas bouger |
| `outbox/` | A | Sortie transfert (fetch) | `winscp_transfer` utilise `.../shared/outbox` | Ne pas bouger |
| `modules/` | A | Dépôt zips modules | `winscp_transfer` utilise `.../shared/modules` | Ne pas bouger |
| `_logs/` | A | Logs opératoires transfert | `winscp_transfer` utilise `.../shared/_logs` | Ne pas bouger |
| `vision_inbox/` | A | Flux vision (entrée) | `vision_bot.service` pointe `.../vision_inbox` | Ne pas bouger |
| `vision_outbox/` | A | Flux vision (sortie) | `vision_bot.service` pointe `.../vision_outbox` | Ne pas bouger |
| `vision_processed/` | A | Flux vision (processed) | `vision_bot.service` pointe `.../vision_processed` | Ne pas bouger |
| `desk_pro/` | A | Export canonical `/shared/desk_pro/latest` | scripts db_layer/student lisent `/shared/desk_pro/latest` | Ne pas bouger |
| `documents/` | B | Documents opératoires | usage humain (pas de preuve pipeline) | Garder en place ; déplacer seulement si volonté claire |
| `windows/` | E | Contenu Windows (17M) | aucune preuve d’usage code | Ne pas bouger ; qualifier contenu avant tout rangement |
| `_git_archives/` | E | Archives git (128K) | aucune preuve d’usage code | Ne pas bouger ; peut migrer plus tard vers `_archives/` |

## 5. CLASSIFICATION DU CONTENU À PLAT (PROPOSITION SANS DÉPLACEMENT)

### 5.1 À CONSERVER À LA RACINE (B)
- `boot_test.txt` : sentinelle utilisée pour sanity/validation multi-machines.
- `README.txt` : doc d’entrée minimale (peut être remplacée plus tard par un README plus structuré).

### 5.2 À RECLASSER PLUS TARD VERS `_refs/` (C)
- `audit_opt_trading_branches.md`
- Tout futur `*.md` / `*.txt` “référence” non consommé par pipeline.

### 5.3 À RECLASSER PLUS TARD VERS `_ops/` (C)
Scripts à plat (exemples) :
- `bridge_vision_to_desk_inbox.sh`
- `install_desk_bridge_timer.sh`
- `prep_commit_admin_trading.sh`
- `check_menus_all.sh`
- `check_shortcuts_targets.sh`
- `bv2_*` (scripts de maintenance/patch/inspection)

### 5.4 À RECLASSER PLUS TARD VERS `_bundles/` (C)
Zips à plat (principe) :
- `*_bundle*.zip`, `*_PACK*.zip`, `*_step*.zip`, `*_patch*.zip`
- `install_module_*.zip`
- `desk_*step*.zip`
- `ops_*zip`, `registry_*zip`, `ui_*zip`, `vision_*zip`

Note : la racine contient aussi des fichiers `.zip` sans suffixe standard ; ils restent reclassables si non consommés par un chemin hardcodé.

### 5.5 À ARCHIVER PLUS TARD VERS `_archives/` (D)
Indices typiques d’archivage :
- doublons `(...).zip` ex: `desk_analyze_vision_stepC_patch (1).zip`
- versions supplantées (`*_v1`, `_v2`, `_v3` quand un pack “current” existe) après preuve d’obsolescence

### 5.6 AMBIGU / À CONFIRMER (E)
Ne pas déplacer avant qualification :
- `.ssh.zip` : risque secrets/clé ; à considérer comme **quarantaine** (à ouvrir/qualifier dans une fenêtre contrôlée).
- `.venv.zip` : artefact volumineux (4,5M) ; probable export local non canonique ; confirmer qu’aucun flux ne le requiert.

## 6. STRATÉGIE DE MIGRATION DOUCE (SANS EXÉCUTION ICI)
1. Créer les dossiers cibles `_bundles/`, `_ops/`, `_refs/`, `_archives/` (sans déplacer).
2. Déplacer uniquement les scripts `.sh` “manifestement opératoires” vers `_ops/` (en gardant une liste des mouvements).
3. Déplacer ensuite les zips “manifestement bundles” vers `_bundles/` par lots (ex: `*_bundle*.zip`).
4. Traiter les doublons `(1)` vers `_archives/` après validation.
5. Traiter les cas sensibles/volumineux (`.ssh.zip`, `.venv.zip`) séparément, avec décision explicite.

## 7. FICHIERS MODIFIÉS
- `OT_SHARED_ORGANIZE_01_ARCHITECTURE.md`
- `OT_SHARED_ORGANIZE_01_CLASSIFICATION.md`
- `OT_SHARED_ORGANIZE_01_CLOSING.txt`

## 8. COMMANDES EXÉCUTÉES
- Inventaire (admin-trading source) : `ls`, `find -maxdepth 1`, `du -sh <dirs>`
- Inventaire (db-layer) : `ls -lah /shared | head` pour cohérence visuelle
- Lecture repo : scripts/services référencés pour qualifier les dossiers réservés

## 9. VERDICT FINAL
- Arbo cible proposée : **simple, durable, migration douce**.
- Classification : dossiers pipeline identifiés ; la racine est majoritairement reclassable ; deux éléments restent ambigus (sécurité/volume).

