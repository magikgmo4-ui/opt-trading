# STUDENT — LIVE RESULT CAPTURE

```
Mission  : GO_STUDENT_LIVE_VALIDATION_PACK_01
Template : GO_STUDENT_LIVE_RESULT_CAPTURE_01
Pivot    : opt-trading / sot/mainline
À remplir après exécution SSH sur la machine student
```

---

## A. CONTEXTE D'EXÉCUTION

```
Date / heure     :
Machine cible    : student — Debian 12 — 192.168.16.103
Opérateur        :
Branche repo     : (git branch --show-current)
Dernier commit   : (git log --oneline -1)
Résultat pull    : OK / Rien à tirer / Erreur →
```

---

## B. RACCOURCI CRITIQUE — `cmd-deepseek_student`

```bash
readlink -f /usr/local/bin/cmd-deepseek_student
```

```
Résultat obtenu  :
Attendu          : /opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh
Statut           : [ ] CONFORME   [ ] NON CONFORME
```

---

## C. LES 9 RACCOURCIS GLOBAUX

Remplir `OK` / `FAIL` / `ABSENT` pour chaque ligne.

```
menu-deepseek_hub    :          → cible :
cmd-deepseek_hub     :          → cible :
sanity-deepseek_hub  :          → cible :
menu-deepseek_student:          → cible :
cmd-deepseek_student :          → cible :   ← CRITIQUE
sanity-deepseek_student:        → cible :
menu-student         :          → cible :
cmd-student          :          → cible :
sanity-student       :          → cible :
```

---

## D. RÉSULTAT `validate_student_live.sh`

```bash
bash /opt/trading/student/validation/validate_student_live.sh
```

```
Exit code        : (0 = OK, 1 = erreurs)
Erreurs          : (nombre)
Avertissements   : (nombre)
Résumé sortie    :
```

Coller ici les dernières lignes de sortie (section RÉSUMÉ) :

```
[coller sortie ici]
```

---

## E. RÉPARATION (si nécessaire)

_Remplir uniquement si des erreurs ont été détectées en section D._

```bash
bash /opt/trading/student/bin/install_shortcuts.sh
# ou : sudo bash /opt/trading/student/bin/install_shortcuts.sh
```

```
Commande lancée  :
Résultat         : OK / Erreur →
```

Re-validation après réparation :

```bash
bash /opt/trading/student/validation/validate_student_live.sh
```

```
Exit code après réparation :
Erreurs restantes          :
```

---

## F. VERDICT FINAL

```
[ ] OK               — 0 erreur, 0 avertissement, tous raccourcis conformes
[ ] OK avec warnings — 0 erreur, avertissements non bloquants
[ ] KO réparé        — erreurs détectées, réparation appliquée, re-validation OK
[ ] KO persistant    — erreurs après réparation → ouvrir GO_STUDENT_LIVE_REPAIR_01
```

---

## G. FICHIERS D'AUDIT À METTRE À JOUR (rôle PM)

Cocher et renseigner après retour live.

```
[ ] audit/2026-03-20/94_student_cleanup_duplicates.md  §5
    → inscrire le résultat exact de readlink cmd-deepseek_student (section B ci-dessus)
    → noter : CONFORME ou NON CONFORME

[ ] audit/2026-03-20/93_student_phase2_migration.md  §6 Hypothèses
    → H01 : shortcuts globaux canoniques ?    OUI / NON
    → H02 : deepseek_student_cmd.sh appelé en prod ?   OUI / NON / INCONNU
    → H03 : modules deepseek_thinking/response présents ?   OUI / NON / NON VÉRIFIÉ

[ ] audit/2026-03-20/97_cross_project_master_kanban.md
    §3 "À CONFIRMER" → passer à CONFIRMÉ si verdict OK
    §12 "POINT ACTIF CONSERVÉ" → mettre à jour statut GO_STUDENT_LIVE_VALIDATION_PACK_01
```

---

## H. POINT DE REPRISE APRÈS LIVE

```
Si verdict OK ou KO réparé :
  → GO_STUDENT_PHASE2_MIGRATION_01 : PARTIEL → ÉTABLI (validation PM)
  → GO_STUDENT_CLEANUP_DUPLICATES_01 : cleanup physique des doublons activable
     (supprimer deepseek_student/deepseek_student_cmd.sh comme entrypoint opérateur)

Si verdict KO persistant :
  → GO_STUDENT_LIVE_REPAIR_01 — transmettre ce fichier complété au PM
```

---

## I. NOTES LIBRES

```
[espace libre pour observations non prévues]
```
