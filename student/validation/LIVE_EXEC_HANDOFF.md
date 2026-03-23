# STUDENT — LIVE EXECUTION HANDOFF

```
Mission : GO_STUDENT_LIVE_EXECUTION_HANDOFF_01
Date    : 2026-03-23
Pivot   : opt-trading / sot/mainline
Machine : student (Debian 12, 192.168.16.103)
```

---

## 1. PRÉREQUIS

| Condition | Détail |
|---|---|
| Accès | SSH ou terminal local avec droits `sudo` |
| Repo déployé | `/opt/trading/` présent sur la machine |
| Branche | `sot/mainline` à jour |

```bash
# Obligatoire avant toute validation
cd /opt/trading && git pull origin sot/mainline
```

---

## 2. COMMANDES

```bash
# Validation complète (lancer en premier)
bash /opt/trading/student/validation/validate_student_live.sh

# Si erreurs de raccourcis détectées : réparer puis re-valider
bash /opt/trading/student/bin/install_shortcuts.sh
bash /opt/trading/student/validation/validate_student_live.sh

# Si droits insuffisants sur install_shortcuts :
sudo bash /opt/trading/student/bin/install_shortcuts.sh
```

---

## 3. RÉSULTATS ATTENDUS (machine saine)

```
[OK] menu-deepseek_hub   → /opt/trading/student/scripts/deepseek_hub/deepseek_hub_menu.sh
[OK] cmd-deepseek_hub    → /opt/trading/student/scripts/deepseek_hub/deepseek_hub_cmd.sh
[OK] sanity-deepseek_hub → /opt/trading/student/scripts/deepseek_hub/sanity_check_deepseek_hub.sh
[OK] menu-deepseek_student   → /opt/trading/student/scripts/wrappers/deepseek_student_menu.sh
[OK] cmd-deepseek_student    → /opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh
                                                                        [CRITIQUE — OK]
[OK] sanity-deepseek_student → /opt/trading/student/scripts/wrappers/deepseek_student_sanity_check.sh
[OK] menu-student   → /opt/trading/student/scripts/student_menu.sh
[OK] cmd-student    → /opt/trading/student/scripts/student_cmd.sh
[OK] sanity-student → /opt/trading/student/scripts/student_sanity_check.sh

✓ VALIDATION RÉUSSIE — 0 erreur, 0 avertissement
```

---

## 4. SI `cmd-deepseek_student` ÉCHOUE

```bash
# Diagnostic exact
readlink -f /usr/local/bin/cmd-deepseek_student
# Attendu : /opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh
# Si différent → shortcut pointe encore vers les modules (régression)
```

**Réparation :**

```bash
bash /opt/trading/student/bin/install_shortcuts.sh
bash /opt/trading/student/validation/validate_student_live.sh
```

Si la réparation échoue après deux tentatives : noter le résultat exact de `readlink` et
ouvrir `GO_STUDENT_LIVE_REPAIR_01` avec PM — ne pas forcer davantage.

---

## 5. FICHIERS D'AUDIT À METTRE À JOUR APRÈS RETOUR LIVE

Transmettre les résultats au PM (ChatGPT) pour mise à jour des fichiers suivants :

| Fichier | Section | Quoi renseigner |
|---|---|---|
| `audit/2026-03-20/94_student_cleanup_duplicates.md` | §5 | Résultat exact de `readlink -f /usr/local/bin/cmd-deepseek_student` |
| `audit/2026-03-20/93_student_phase2_migration.md` | §6 | H01 : shortcuts canoniques confirmés ou non / H02 : deepseek_student_cmd.sh appelé en prod ou non |
| `audit/2026-03-20/97_cross_project_master_kanban.md` | §3 et §12 | "À CONFIRMER" → CONFIRMÉ (si OK) — §12 : statut GO_STUDENT_LIVE_VALIDATION_PACK_01 |

---

## 6. POINT DE REPRISE SUIVANT

**Si validation OK (0 erreur) :**

```
GO_STUDENT_PHASE2_MIGRATION_01 : PARTIEL → ÉTABLI (validation PM requise)
GO_STUDENT_CLEANUP_DUPLICATES_01 : cleanup physique des doublons activable
  → supprimer deepseek_student/deepseek_student_cmd.sh comme entrypoint opérateur
     (garder comme backend narrow scope — cf. 94_student_cleanup_duplicates.md §4.2)
```

**Si validation KO (après réparation) :**

```
GO_STUDENT_LIVE_REPAIR_01 — nouveau chantier à ouvrir avec PM
  → transmettre : résultat readlink exact, output validate_student_live.sh complet
```
