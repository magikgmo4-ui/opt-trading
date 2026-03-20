# STUDENT — RAPPORT CLEANUP DOUBLONS

```
Date     : 2026-03-20
Branche  : audit/opt-trading-20260320a
Mission  : GO_STUDENT_CLEANUP_DUPLICATES_01
Pivot    : opt-trading / sot/mainline
Statut   : LIVRÉ — classification complète, aucune suppression appliquée,
           documentation mise à jour, validation live requise avant tout retrait
```

---

## 1. État réel observé

### 1.1 Façades canoniques — SAINES, non touchées

| Script | Rôle | État |
|---|---|---|
| `student/scripts/student_cmd.sh` | Top-level façade canonique | CANONIQUE — non modifié |
| `student/scripts/student_menu.sh` | Top-level façade canonique | CANONIQUE — non modifié |
| `student/scripts/student_sanity_check.sh` | Top-level façade canonique | CANONIQUE — non modifié |
| `student/scripts/wrappers/deepseek_student_cmd.sh` | Module-level operator wrapper (survivant CMD) | CANONIQUE — non modifié |
| `student/bin/install_shortcuts.sh` | Installer canonique complet | CANONIQUE — non modifié |

### 1.2 Chaîne d'appel critique identifiée

`modules/deepseek_hub/scripts/deepseek_hub_cmd.sh` appelle `cmd-deepseek_student roadmap` via l'**alias global** `/usr/local/bin/cmd-deepseek_student`.

Ce shortcut peut pointer vers :
- **canonique** : `student/scripts/wrappers/deepseek_student_cmd.sh` (si installé par `student/bin/install_shortcuts.sh`)
- **legacy** : `modules/deepseek_student/scripts/cmd.sh` (si installé par le legacy installer `modules/deepseek_student/scripts/install_shortcuts.sh`)

**C'est le seul risque réel de cette passe.** Non vérifiable sans SSH live.

---

## 2. Inventaire complet des doublons — classification par niveau de risque

### 2.1 Couche CMD

| Script | Callers dans `student/` | Callers hors `student/` | Risque retrait | Décision |
|---|---|---|---|---|
| `student_cmd.sh` | shortcut `cmd-student` (canonical) | — | — | CANONIQUE — ne pas toucher |
| `wrappers/deepseek_student_cmd.sh` | `wrappers/deepseek_student_menu.sh`, `wrappers/deepseek_student_daily_ai_report.sh`, `wrappers/deepseek_student_sanity_check.sh`, shortcut `cmd-deepseek_student` (canonical) | — | — | CANONIQUE SURVIVANT — ne pas toucher |
| `deepseek_student/cmd.sh` | aucun caller externe depuis `student/` | `modules/deepseek_student/scripts/cmd.sh` (copie legacy source) | MOYEN | CONSERVER — dispatcher interne, pas d'exposition globale depuis `bin/` |
| `deepseek_student/deepseek_student_cmd.sh` | `deepseek_student/cmd.sh` (dispatch `roadmap\|pull\|test\|sanity`) | Via alias global `cmd-deepseek_student` si shortcut mal configuré | ÉLEVÉ — dépend de l'état live du shortcut | CONSERVER — supprimer uniquement après `readlink /usr/local/bin/cmd-deepseek_student` confirmé canonical |

### 2.2 Couche Installer

| Script | Callers | Risque retrait | Décision |
|---|---|---|---|
| `bin/install_shortcuts.sh` | — | — | CANONIQUE — ne pas toucher |
| `scripts/deepseek_hub/install_shortcuts.sh` | aucun caller programmatique | FAIBLE — usage manuel uniquement | CONSERVER — marquer `legacy/internal` dans doc |
| `scripts/deepseek_student/install_shortcuts.sh` | aucun caller programmatique | FAIBLE — usage manuel uniquement | CONSERVER — marquer `legacy/internal` dans doc |

### 2.3 Couche Sanity

| Script | Scope réel | Callers actifs | Risque retrait | Décision |
|---|---|---|---|---|
| `student_sanity_check.sh` | top-level | shortcut `sanity-student` | — | CANONIQUE — ne pas toucher |
| `deepseek_hub/sanity_check_deepseek_hub.sh` | hub runtime | shortcut `sanity-deepseek_hub`, `student_sanity_check.sh` via exec | ÉLEVÉ — appelé par la façade top-level | CONSERVER — interne indispensable |
| `wrappers/deepseek_student_sanity_check.sh` | module facade | shortcut `sanity-deepseek_student`, `wrappers/deepseek_student_cmd.sh sanity` | MOYEN | CONSERVER — module-level facade, scope clair |
| `deepseek_student/sanity_check_deepseek_student.sh` | backend narrow | `deepseek_student/deepseek_student_cmd.sh sanity` | FAIBLE — backend interne uniquement | CONSERVER — backend scope, clairement scopé |
| `deepseek_student/sanity_check.sh` | structure check générique | aucun caller actif trouvé | FAIBLE | CONSERVER — module wrapper pattern générique, inoffensif |

### 2.4 Couche Menu

| Script | Scope réel | Callers actifs | Risque retrait | Décision |
|---|---|---|---|---|
| `student_menu.sh` | top-level | shortcut `menu-student` | — | CANONIQUE — ne pas toucher |
| `deepseek_hub/deepseek_hub_menu.sh` | hub runtime | shortcut `menu-deepseek_hub`, `student_menu.sh` via exec | ÉLEVÉ — appelé par la façade top-level | CONSERVER — interne indispensable |
| `wrappers/deepseek_student_menu.sh` | module facade | shortcut `menu-deepseek_student`, `wrappers/deepseek_student_cmd.sh menu` | MOYEN | CONSERVER — module-level facade, scope clair |
| `wrappers/desk_pro_student_menu.sh` | Desk Pro student | `wrappers/desk_pro_student_cmd.sh menu` | MOYEN | CONSERVER — périmètre Desk Pro student distinct |
| `deepseek_student/menu.sh` | module wrapper menu générique | aucun caller actif depuis `student/` | FAIBLE | CONSERVER — module wrapper pattern, pas d'exposition globale |

---

## 3. Changements appliqués

### 3.1 `student/docs/DUPLICATES_AUDIT.md`

Ajout d'une section **"Caller Audit — État 2026-03-20"** contenant :
- tableau de classification par niveau de risque pour tous les doublons
- résultat principal : aucun retrait physique justifié
- identification du risque principal (`cmd-deepseek_student` alias live)
- décision : pas de suppression avant validation live

---

## 4. Changements préparés mais non appliqués

### 4.1 Notices de dépréciation dans les scripts

Prêt à ajouter dans `scripts/deepseek_hub/install_shortcuts.sh` et `scripts/deepseek_student/install_shortcuts.sh` un commentaire d'en-tête marquant leur statut `legacy/internal`. **Non appliqué** : modification de scripts sans validation live = risque de confusion opérateur.

### 4.2 Retrait de `deepseek_student/deepseek_student_cmd.sh` comme entrypoint

Non appliqué. Conditionné à la confirmation live que :
```bash
readlink -f /usr/local/bin/cmd-deepseek_student
# doit retourner : .../student/scripts/wrappers/deepseek_student_cmd.sh
```

### 4.3 Cleanup de `deepseek_student/cmd.sh`

Non appliqué. Ce dispatcher thin reste utile tant que la couche legacy module est en place.

---

## 5. Commandes de validation manuelle requises avant tout retrait

À exécuter sur la machine `student` :

```bash
# Vérifier l'alias critique
readlink -f /usr/local/bin/cmd-deepseek_student
# Attendu : /opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh

# Vérifier tous les shortcuts student
readlink -f /usr/local/bin/menu-student
readlink -f /usr/local/bin/cmd-student
readlink -f /usr/local/bin/sanity-student
readlink -f /usr/local/bin/menu-deepseek_student
readlink -f /usr/local/bin/sanity-deepseek_student

# Vérifier la chaîne complète
sanity-student
cmd-student status
cmd-deepseek_student show-paths   # ligne "Hub Cmd" doit pointer vers student/scripts/deepseek_hub/
```

Si `cmd-deepseek_student` pointe encore vers `modules/deepseek_student/scripts/cmd.sh` :
```bash
# Réinstaller les shortcuts depuis le canonical installer
bash /opt/trading/student/bin/install_shortcuts.sh
```

---

## 6. Limites réelles observées

Audit purement structurel et documentaire — aucun accès SSH live à la machine `student`. L'état du shortcut global `cmd-deepseek_student` sur la machine est le seul point non vérifiable depuis ce contexte. Les modules `opt-trading/modules/deepseek_hub/` et `opt-trading/modules/deepseek_student/` contiennent des copies des scripts similaires à `student/` : ces copies legacy sont hors périmètre de cette passe.

---

## 7. Point de reprise suivant

```
GO_STUDENT_CLEANUP_DUPLICATES_01 → LIVRÉ

Ce qui est fait :
  ✓ audit terrain complet des callers de tous les doublons identifiés
  ✓ classification par niveau de risque (CMD / Installer / Sanity / Menu)
  ✓ DUPLICATES_AUDIT.md mis à jour avec section Caller Audit 2026-03-20
  ✓ identification du risque principal : alias cmd-deepseek_student live

Ce qui reste conditionné à la validation live :
  → vérifier readlink /usr/local/bin/cmd-deepseek_student sur machine student
  → si legacy : réexécuter student/bin/install_shortcuts.sh
  → après confirmation : supprimer deepseek_student/deepseek_student_cmd.sh
    comme entrypoint opérateur (garder comme backend narrow scope)

Prochain chantier portefeuille recommandé :
  GO_API_COLLECTOR_CANONICAL_MODULE_01
  → qualifier le module api collector (état fonctionnel réel, nom canonique,
    runbook minimal, décision module opt-trading ou projet séparé)
```
