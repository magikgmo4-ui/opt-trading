---
doc_id: GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01_JOURNAL_TECHNIQUE
doc_type: chantier_journal_technique
repo: opt-trading
project: opt-trading
module: repo_hygiene
go_id: GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01
status: active
lifecycle_stage: journal_technique
topic_keys:
  - opt-trading
  - obsolete
  - declass
  - archive
  - legacy
  - reclass
  - audit
surface: chantier
source_kind: canonical
updated_at: 2026-04-20
links:
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/03_decisions.md
---

# 02_journal_technique — GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01

## 2026-04-20
### Étape 1 — Ouverture du parent (PHASE A)
- création des artefacts minimaux :
  - `00_cadrage.md`
  - `02_journal_technique.md`
  - `03_decisions.md`
- principe : audit repo-first, doc-only, non destructif
- but : qualifier obsolete / déclassé / archive / legacy toléré / sous arbitrage ; produire matrice + plan de lots futurs

### Étape 1b — Ancrage dans la continuité (PHASE A)
- index mis à jour pour ouvrir ce parent comme actif :
  - `docs/index/GO_INDEX.md`
  - `docs/index/ACTIVE_STREAMS.md`
  - `docs/index/REPRISE.md`
  - `docs/index/NEXT_GO_CANDIDATES.md`
- compteur : 11 GO non clos

### Limites (rappel)
- pas de suppression massive
- pas de déplacement global
- pas de refactor transverse

### Étape 2 — Sous-lot A1 : recroisement continuité canonique
- index canoniques lus : `docs/index/*`
- politiques canoniques lues : `REPO_ROOT_POLICY`, `REPO_SURFACES_MAP`, `JOURNAL_HIERARCHY`
- constat : le périmètre opératoire est piloté par 11 GO non clos (incluant ce parent)

### Étape 3 — Sous-lot B1 : objets racine sous arbitrage (GROUPE 1)
Constat repo-first (présence physique confirmée) :
- `Readme`
- `TOOLBOX.txt`
- `UI_URLS.md`
- `journal_add.sh`
- `smartmoney.txt`
- `bitget_bridge.py`
- `_archive/`
- `trae_pack_texts/`
- `.gitignore.bak*`

### Étape 4 — Sous-lot B2 : reliquats workflow_post_change (GROUPE 2)
Constat repo-first :
- `modules/workflow_post_change_v2` est le candidat canonique actif
- des variantes `workflow_post_change_v2_fix*` existent encore physiquement
- un backup `workflow_post_change_v2_broken_backup` existe dans `_archive/`

### Étape 5 — Sous-lot B3 : docs historiques dispersées (GROUPE 3)
Constat repo-first :
- `docs/CLOSEOUT_FINAL_BOT_VISION.txt`
- `docs/ETABLI_BOT_VISION.txt`
- `docs/RESIDUEL_BOT_VISION.txt`

### Étape 6 — Sous-lot B4 : supports locaux non canoniques (GROUPE 4)
Constat repo-first :
- `trae_pack_texts/trae_pack/*` existe comme bibliothèque locale de textes

### Étape 7 — PHASE C : matrice d’objets (v0)

| chemin / famille | catégorie | justification | risque | action recommandée | dépendance avant action | validation requise |
| --- | --- | --- | --- | --- | --- | --- |
| `Readme` | sous arbitrage | listé explicitement dans `REPO_ROOT_POLICY.md` ; présent physiquement en racine | moyen | surveiller | inventaire callers + rôle réel | validation lot “racine” |
| `TOOLBOX.txt` | sous arbitrage | listé dans `REPO_ROOT_POLICY.md` ; présent physiquement en racine | faible | laisser en place | inventaire usages | validation lot “racine” |
| `UI_URLS.md` | sous arbitrage | listé dans `REPO_ROOT_POLICY.md` ; présent physiquement en racine | faible | laisser en place | inventaire usages | validation lot “racine” |
| `journal_add.sh` | sous arbitrage | listé dans `REPO_ROOT_POLICY.md` ; script racine | moyen | surveiller | vérifier callers (CI / usage humain) | validation lot “racine” |
| `smartmoney.txt` | sous arbitrage | listé dans `REPO_ROOT_POLICY.md` ; contenu non qualifié ici | moyen | surveiller | qualifier surface (doc/référence/runtime) | validation lot “racine” |
| `bitget_bridge.py` | sous arbitrage | listé dans `REPO_ROOT_POLICY.md` ; potentiel caller runtime | élevé | laisser en place | identifier appels runtime | validation lot “racine” + rollback |
| `.gitignore.bak*` | legacy toléré | backup ponctuel en racine (politique racine mentionne `.gitignore.bak*`) | faible | supprimer après validation | confirmer inutilité + pas de caller | validation lot “quick win” |
| `_archive/` | sous arbitrage | surface racine explicitement sous arbitrage | moyen | laisser en place | définir surface archive cible | validation lot “racine” |
| `_archive/workflow_post_change_v2_broken_backup/*` | archive existante | backup nommé ; utile rollback workflow | faible | archiver | définir emplacement archive technique cible | validation lot “workflow” |
| `modules/workflow_post_change_v2` | actif | candidat canonique actif (status `workflow_post_change_canonique`) | moyen | garder | confirmer callers | validation lot “workflow” |
| `modules/workflow_post_change_v2_fix1` | legacy toléré | reliquat marqué `DEPRECATED` ; présent physiquement | moyen | déplacer | prouver absence de caller | validation lot “workflow” + rollback |
| `modules/workflow_post_change_v2_fix2` | legacy toléré | reliquat marqué `DEPRECATED` ; présent physiquement | moyen | déplacer | prouver absence de caller | validation lot “workflow” + rollback |
| `modules/workflow_post_change_v2_fix3` | legacy toléré | reliquat marqué `DEPRECATED` ; présent physiquement | moyen | déplacer | prouver absence de caller | validation lot “workflow” + rollback |
| `docs/CLOSEOUT_FINAL_BOT_VISION.txt` | legacy toléré | doc historique en `docs/` ; doublonne potentiellement des traces `docs/status/*` | faible | archiver | choisir surface archive doc | validation lot “docs historiques” |
| `docs/ETABLI_BOT_VISION.txt` | legacy toléré | doc historique en `docs/` | faible | archiver | choisir surface archive doc | validation lot “docs historiques” |
| `docs/RESIDUEL_BOT_VISION.txt` | legacy toléré | doc historique en `docs/` | faible | archiver | choisir surface archive doc | validation lot “docs historiques” |
| `trae_pack_texts/trae_pack/*` | legacy toléré | bibliothèque locale de textes Trae ; utile mais hors canon Git | faible | laisser en place | expliciter politique d’archive locale | validation lot “supports locaux” |

### Étape 8 — PHASE D : plan de lots futurs (v0)
- lot quick wins sûrs :
  - `.gitignore.bak*` (après validation)
- lot reclassement legacy workflow :
  - `workflow_post_change_v2_fix*` + `_archive/workflow_post_change_v2_broken_backup`
- lot archivage docs historiques :
  - `docs/*BOT_VISION*.txt` (après validation, sans casser `docs/status/*`)
- lot arbitrage racine :
  - décider item par item de la liste `REPO_ROOT_POLICY` (sans sweep global)
- lot supports locaux / exception :
  - politique `trae_pack_texts` + `_archive` (surface cible, règles de conservation, rollback)

### Étape 9 — PHASE B : preuves repo-first callers/usages (v0)

#### `bitget_bridge.py`
- appelé réellement : aucun caller explicite trouvé dans le repo
- mention documentaire seulement :
  - `modules/simex_bitget_bridge/README.md` mentionne que le shim reste disponible
- preuve repo-first (structure) :
  - `bitget_bridge.py` n’est qu’un shim qui appelle `modules.simex_bitget_bridge.app.simex_bitget_bridge:main`
  - les scripts opérateur simex utilisent `modules/simex_bitget_bridge/app/simex_bitget_bridge.py` via `modules/simex_bitget_bridge/cmd.sh` (pas via `bitget_bridge.py`)
- statut proposé : sous arbitrage

#### `journal_add.sh`
- appelé réellement : aucun caller explicite trouvé dans le repo
- preuve repo-first (contenu) :
  - le script écrit dans `/opt/trading/journal/` puis exécute `git add/commit/push`
- statut proposé : sous arbitrage (risque opératoire)

#### `modules/workflow_post_change_v2`
- preuve repo-first (consommation outillage) :
  - déclaré `status: active` dans `registry/modules_registry.yaml`
  - consommé par l’outillage `modules_registry_reader` qui lit `registry/modules_registry.yaml`
- preuve repo-first (exposition opérateur) :
  - le module fournit `scripts/install_shortcuts.sh` pour installer des wrappers système `cmd-workflow_post_change_v2` / `menu-workflow_post_change_v2` / `sanity-workflow_post_change_v2`
- statut proposé : actif

#### `modules/workflow_post_change_v2_fix1`
- appelé réellement : aucun caller explicite trouvé dans le repo (hors docs et auto-références)
- preuve repo-first (contenu) :
  - `DEPRECATED.md` indique “obsolète” et impose `workflow_post_change_v2` comme canonique
- statut proposé : legacy toléré (historique / rollback ciblé)

#### `modules/workflow_post_change_v2_fix2`
- appelé réellement : aucun caller explicite trouvé dans le repo (hors docs et auto-références)
- preuve repo-first (contenu) :
  - `DEPRECATED.md` indique “obsolète” et impose `workflow_post_change_v2` comme canonique
- statut proposé : legacy toléré (historique / rollback ciblé)

#### `modules/workflow_post_change_v2_fix3`
- preuve repo-first (consommation outillage) :
  - déclaré `status: deprecated_merged` dans `registry/modules_registry.yaml`
- preuve repo-first (contenu) :
  - `DEPRECATED.md` indique “mergé dans v2” ; conservation temporaire pour rollback/référence
- statut proposé : legacy toléré / archive existante (selon arbitrage lot workflow)

#### `docs/CLOSEOUT_FINAL_BOT_VISION.txt`, `docs/ETABLI_BOT_VISION.txt`, `docs/RESIDUEL_BOT_VISION.txt`
- appelé réellement : aucun caller technique trouvé (pas de lecture par `.py/.sh` détectée)
- mention documentaire seulement :
  - référencés comme liens repo dans `docs/ot/project_cards/PROJECT_CARD_BOT_VISION_INGESTION_01.md`
- statut proposé : legacy toléré (doc historique)

### Matrice v1 (items à risque)

| chemin | caller / preuve | statut proposé | risque | action proposée | lot recommandé |
| --- | --- | --- | --- | --- | --- |
| `bitget_bridge.py` | pas d’appel explicite repo ; shim python vers `modules/simex_bitget_bridge/app/simex_bitget_bridge.py` ; scripts simex utilisent le module directement | sous arbitrage | élevé | laisser en place | lot “arbitrage racine” |
| `journal_add.sh` | pas d’appel explicite repo ; script effectue `git add/commit/push` sur `/opt/trading/journal/` | sous arbitrage | élevé | surveiller | lot “arbitrage racine” |
| `modules/workflow_post_change_v2` | `registry/modules_registry.yaml` = `status: active` ; consommé par `modules_registry_reader` ; module fournit `install_shortcuts.sh` | actif | moyen | garder | lot “workflow” |
| `modules/workflow_post_change_v2_fix1` | `DEPRECATED.md` = obsolète ; pas d’appel repo identifié | legacy toléré | moyen | laisser en place | lot “workflow” |
| `modules/workflow_post_change_v2_fix2` | `DEPRECATED.md` = obsolète ; pas d’appel repo identifié | legacy toléré | moyen | laisser en place | lot “workflow” |
| `modules/workflow_post_change_v2_fix3` | `registry/modules_registry.yaml` = `deprecated_merged` ; `DEPRECATED.md` = mergé ; pas d’appel repo identifié | legacy toléré | moyen | laisser en place | lot “workflow” |
| `docs/CLOSEOUT_FINAL_BOT_VISION.txt` | pas de caller technique (`.py/.sh`) ; lien dans `PROJECT_CARD_BOT_VISION_INGESTION_01` | legacy toléré | faible | archiver (après validation) | lot “docs historiques” |
| `docs/ETABLI_BOT_VISION.txt` | pas de caller technique (`.py/.sh`) ; lien dans `PROJECT_CARD_BOT_VISION_INGESTION_01` | legacy toléré | faible | archiver (après validation) | lot “docs historiques” |
| `docs/RESIDUEL_BOT_VISION.txt` | pas de caller technique (`.py/.sh`) ; doc historique | legacy toléré | faible | archiver (après validation) | lot “docs historiques” |

### Étape 10 — Sous-lot prêt : LOT_DOCS_HISTORIQUES_BOT_VISION (préparation, sans action physique)

#### Périmètre exact
- `docs/CLOSEOUT_FINAL_BOT_VISION.txt`
- `docs/ETABLI_BOT_VISION.txt`
- `docs/RESIDUEL_BOT_VISION.txt`

#### Vérification repo-first (doc-only / hors runtime)
- aucun caller technique trouvé dans le repo (`*.py`, `*.sh`, `*.ps1`, `*.json`, `*.yaml`, etc.)
- usages observés :
  - mentions documentaires et liens repo uniquement (ex : `docs/ot/project_cards/PROJECT_CARD_BOT_VISION_INGESTION_01.md`)
  - mention documentaire dans `modules/bot_vision_step2/SHAREX_WATCHDOG.md` (référence à `docs/RESIDUEL_BOT_VISION.txt`)
  - mention documentaire dans `docs/ot/closings/OT_BOT_VISION_WATCHDOG_01_CLOSING.txt`

#### Justification
- réduire la dispersion documentaire en `docs/` racine en déplaçant des documents historiques Bot Vision vers une surface d’archive OT.
- conserver l’historique (pas de suppression) et rendre la localisation plus canonique, sans rouvrir la chaîne Bot Vision runtime.

#### Risque
- faible côté runtime (doc-only)
- moyen côté continuité documentaire : nécessite mise à jour des liens/refs pointant vers l’ancien chemin

#### Cible d’archivage proposée (canonique)
- `docs/ot/closings/bot_vision/`

#### Exclusions (strict)
- ne traiter que les 3 fichiers du périmètre
- ne pas toucher `workflow_post_change_v2` (hors lot)
- ne pas toucher `bitget_bridge.py` (hors lot)
- ne pas toucher `journal_add.sh` (hors lot)
- ne pas déplacer d’autres fichiers “BOT_VISION” ou “watchdog” hors validation explicite

#### Rollback (si le lot est appliqué plus tard)
- rollback simple : revert du commit du lot (restaure les chemins + les liens)
- rollback local : annuler les `git mv` et restaurer les anciens chemins avant commit

#### Critères PASS / FAIL
- PASS si :
  - les 3 fichiers ont été déplacés uniquement vers la cible d’archive proposée
  - tous les liens/refs repo pointant vers l’ancien chemin ont été mis à jour (au minimum : project card + docs/ot/closings + doc module)
  - aucun impact runtime (aucune exécution, aucun script modifié)
  - diff borné au lot (3 moves + mises à jour de liens)
- FAIL si :
  - un fichier hors périmètre est déplacé
  - un caller runtime est découvert ou impacté
  - des liens critiques sont cassés (références restantes vers chemins inexistants)

### Étape 11 — Application physique validée : LOT_DOCS_HISTORIQUES_BOT_VISION
- dossier cible confirmé/créé : `docs/ot/closings/bot_vision/`
- moves appliqués (strictement 3) :
  - `docs/CLOSEOUT_FINAL_BOT_VISION.txt` -> `docs/ot/closings/bot_vision/CLOSEOUT_FINAL_BOT_VISION.txt`
  - `docs/ETABLI_BOT_VISION.txt` -> `docs/ot/closings/bot_vision/ETABLI_BOT_VISION.txt`
  - `docs/RESIDUEL_BOT_VISION.txt` -> `docs/ot/closings/bot_vision/RESIDUEL_BOT_VISION.txt`
- mises à jour minimales de références appliquées dans :
  - `docs/ot/project_cards/PROJECT_CARD_BOT_VISION_INGESTION_01.md`
  - `modules/bot_vision_step2/SHAREX_WATCHDOG.md`
  - `docs/ot/closings/OT_BOT_VISION_WATCHDOG_01_CLOSING.txt`
- vérifications réalisées :
  - diff borné au lot (3 renames + 5 ajustements documentaires)
  - `git grep` des anciens chemins ciblés : vide
- exclusions respectées :
  - aucun move/delete hors périmètre
  - aucun changement sur `modules/workflow_post_change_v2`
  - aucun changement sur `bitget_bridge.py`
  - aucun changement sur `journal_add.sh`

### REPRISE
Point de reprise unique :
- revue finale du lot appliqué puis décision de clôture parent ou ouverture du lot suivant validé
