# STUDENT VALIDATION PACK — HANDOFF

```
Date     : 2026-03-20
Mission  : GO_STUDENT_LIVE_VALIDATION_PACK_01
Statut   : LIVRÉ
Pivot    : opt-trading / sot/mainline
```

---

## 1. CE QUI A ÉTÉ CONSTRUIT

### Fichiers produits (ce pack)

| Fichier | Rôle |
|---|---|
| `validate_student_live.sh` | Runner principal — 5 sections de validation live |
| `student_validation_cmd.sh` | Dispatcher CMD — interface programmatique |
| `student_validation_menu.sh` | Menu interactif opérateur |
| `student_validation_sanity_check.sh` | Sanity check structurel statique |
| `RUNBOOK.md` | Runbook opérateur complet |
| `HANDOFF.md` | Ce document — état de livraison |

### Emplacement

```
/opt/trading/student/validation/
```

Ce répertoire n'existait pas avant cette mission. Il a été créé dans cette passe.

---

## 2. CE QUE LE PACK VALIDE

### Validation couverte

| Périmètre | Script |
|---|---|
| 9 raccourcis globaux (readlink -f) | `validate_student_live.sh` §1 |
| Raccourci critique `cmd-deepseek_student` (RISQUE ÉLEVÉ) | `validate_student_live.sh` §2 |
| Callers legacy item 5 (alias-based fallback) | `validate_student_live.sh` §3 |
| Entrypoints canoniques live (sanity-student, cmd-student, cmd-deepseek_student) | `validate_student_live.sh` §4 |
| Structure répertoire student/ (fichiers sources) | `validate_student_live.sh` §5 |
| Pack validation lui-même (autocontrôle) | `student_validation_sanity_check.sh` §1 |

### Contexte du raccourci critique

Issue identifiée lors de la passe d'audit 2026-03-20 (document `94_student_cleanup_duplicates.md`) :
`readlink -f /usr/local/bin/cmd-deepseek_student` doit pointer vers les **wrappers** et non
vers les modules. Ce pack permet de confirmer ou d'infirmer cet état sur la machine live.

---

## 3. CE QUE LE PACK NE VALIDE PAS

| Périmètre | Raison du report |
|---|---|
| Exécution réelle des modèles DeepSeek | Dépendance réseau/API externe — hors périmètre validation structurelle |
| Modules `deepseek_thinking` / `deepseek_response` | Dépendances Python externes — hors périmètre |
| État des sessions tmux/screen actives | Non observable depuis le pack statique |
| Environnement Python/virtualenv | Hors périmètre passe documentaire |
| Item 5 LEGACY_CALLERS_INVENTORY — exécution | Vérifiable par grep (§3 de `validate_student_live.sh`) mais non exécuté live |

Chantier différé pour validation approfondie : `GO_STUDENT_DEEP_RUNTIME_AUDIT_01`

---

## 4. COMMENT LANCER CE PACK

### Sur la machine Linux cible (où /opt/trading/student est effectivement déployé)

```bash
# S'assurer que le repo est à jour
cd /opt/trading && git pull origin sot/mainline

# Lancer la validation live complète
bash /opt/trading/student/validation/validate_student_live.sh

# Si erreurs détectées — réparer et re-valider
bash /opt/trading/student/validation/validate_student_live.sh --repair
bash /opt/trading/student/validation/validate_student_live.sh

# Menu interactif
bash /opt/trading/student/validation/student_validation_menu.sh
```

---

## 5. RÉSULTATS ATTENDUS (machine saine)

```
[OK] menu-deepseek_hub → /opt/trading/student/scripts/deepseek_hub/deepseek_hub_menu.sh
[OK] cmd-deepseek_hub  → /opt/trading/student/scripts/deepseek_hub/deepseek_hub_cmd.sh
[OK] sanity-deepseek_hub → ...
[OK] menu-deepseek_student → ...
[OK] cmd-deepseek_student → /opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh  [CRITIQUE — OK]
[OK] sanity-deepseek_student → ...
[OK] menu-student → ...
[OK] cmd-student → ...
[OK] sanity-student → ...

✓ VALIDATION RÉUSSIE — 0 erreur, 0 avertissement
```

---

## 6. RÉSULTATS EN CAS DE RÉGRESSION

Si `cmd-deepseek_student` pointe vers les modules (régression type) :

```
[FAIL] cmd-deepseek_student
       attendu : /opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh
       obtenu  : /opt/trading/student/modules/deepseek_student/...  [CRITIQUE — MAUVAISE CIBLE]

✗ VALIDATION ÉCHOUÉE — 1 erreur(s), 0 avertissement(s)
Réparation : bash /opt/trading/student/bin/install_shortcuts.sh
```

---

## 7. POINTS DE REPRISE

| Point | État |
|---|---|
| `GO_STUDENT_LIVE_VALIDATION_PACK_01` | **LIVRÉ** — 2026-03-20 |
| `GO_STUDENT_PHASE2_MIGRATION_01` | PARTIEL — validation live différée à ce pack |
| Items 1–4 LEGACY_CALLERS_INVENTORY | CORRIGÉ (passe précédente) |
| Item 5 LEGACY_CALLERS_INVENTORY | EN ATTENTE — à confirmer par §3 de `validate_student_live.sh` |
| `GO_STUDENT_DEEP_RUNTIME_AUDIT_01` | DIFFÉRÉ — chantier suivant si PM décide d'approfondir |

---

## 8. SOURCES DE RÉFÉRENCE

| Document | Rôle |
|---|---|
| `audit/2026-03-20/92_student_canonical_surface.md` | Surface canonique student |
| `audit/2026-03-20/93_student_phase2_migration.md` | Migration Phase 2 — état réel |
| `audit/2026-03-20/94_student_cleanup_duplicates.md` | Doublons + raccourci critique identifié |
| `student/bin/install_shortcuts.sh` | Source des 9 raccourcis canoniques |
| `student/docs/LEGACY_CALLERS_INVENTORY.md` | Inventaire callers legacy — item 5 EN ATTENTE |
| `student/config/shortcut_map.env` | Carte des cibles (3 entrées student/cmd/sanity) |
