# STUDENT VALIDATION PACK — RUNBOOK OPÉRATEUR

```
Date     : 2026-03-20
Mission  : GO_STUDENT_LIVE_VALIDATION_PACK_01
Pivot    : opt-trading / sot/mainline
Machine  : machine Linux cible où /opt/trading/student est effectivement déployé et où les shortcuts /usr/local/bin doivent être validés
```

---

## 1. PRÉREQUIS

| Prérequis | Détail |
|---|---|
| Machine | machine Linux cible où `/opt/trading/student` est effectivement déployé |
| Accès | SSH ou terminal local avec droits `sudo` |
| Repo déployé | `/opt/trading/` présent sur la machine cible |
| PATH | `/usr/local/bin` dans le PATH (standard Debian) |

---

## 2. COMMANDES DE LANCEMENT RAPIDE

### 2a — Validation live complète (recommandée en premier)

```bash
bash /opt/trading/student/validation/validate_student_live.sh
```

Exit 0 = tout OK. Exit 1 = erreurs détectées.

### 2b — Validation avec auto-repair

```bash
bash /opt/trading/student/validation/validate_student_live.sh --repair
```

Auto-réparation : appelle `install_shortcuts.sh` si des erreurs de raccourcis sont détectées. Re-lancer sans `--repair` après pour vérifier.

### 2c — Menu interactif

```bash
bash /opt/trading/student/validation/student_validation_menu.sh
```

Menu guidé avec toutes les options de vérification.

### 2d — Sanity check structurel uniquement

```bash
bash /opt/trading/student/validation/student_validation_sanity_check.sh
```

Vérification statique des fichiers et répertoires — ne lance aucune commande live.

### 2e — Via cmd dispatcher

```bash
bash /opt/trading/student/validation/student_validation_cmd.sh help
bash /opt/trading/student/validation/student_validation_cmd.sh status
bash /opt/trading/student/validation/student_validation_cmd.sh shortcuts
```

---

## 3. VÉRIFICATIONS EFFECTUÉES PAR `validate_student_live.sh`

### §1 — Les 9 raccourcis globaux

| Raccourci | Cible attendue |
|---|---|
| `menu-deepseek_hub` | `$ROOT/scripts/deepseek_hub/deepseek_hub_menu.sh` |
| `cmd-deepseek_hub` | `$ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh` |
| `sanity-deepseek_hub` | `$ROOT/scripts/deepseek_hub/sanity_check_deepseek_hub.sh` |
| `menu-deepseek_student` | `$ROOT/scripts/wrappers/deepseek_student_menu.sh` |
| **`cmd-deepseek_student`** | **`$ROOT/scripts/wrappers/deepseek_student_cmd.sh` ← CRITIQUE** |
| `sanity-deepseek_student` | `$ROOT/scripts/wrappers/deepseek_student_sanity_check.sh` |
| `menu-student` | `$ROOT/scripts/student_menu.sh` |
| `cmd-student` | `$ROOT/scripts/student_cmd.sh` |
| `sanity-student` | `$ROOT/scripts/student_sanity_check.sh` |

`ROOT = /opt/trading/student`

### §2 — Raccourci critique `cmd-deepseek_student`

Vérification dédiée (RISQUE ÉLEVÉ identifié en audit 2026-03-20) :

```bash
readlink -f /usr/local/bin/cmd-deepseek_student
# Doit retourner : /opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh
```

Si ce raccourci pointe vers les modules au lieu des wrappers, les fonctions
deepseek_student et deepseek_hub sont défaillantes.

### §3 — Callers legacy (item 5 LEGACY_CALLERS_INVENTORY)

- `deepseek_hub_cmd.sh` doit contenir la référence à `cmd-deepseek_student` (fallback alias-based)
- `sanity_check_deepseek_hub.sh` doit vérifier la présence de `cmd-deepseek_student`

### §4 — Entrypoints canoniques fonctionnels

```bash
sanity-student
cmd-student status
cmd-deepseek_student show-paths
```

### §5 — Structure répertoire student/

Présence de tous les fichiers sources critiques (scripts, wrappers, bin, config).

---

## 4. INTERPRÉTATION DES RÉSULTATS

| Sortie | Signification |
|---|---|
| `[OK]` vert | Vérification réussie |
| `[WARN]` jaune | Avertissement — à investiguer, non bloquant |
| `[FAIL]` rouge | Erreur bloquante |
| `[CRITIQUE — OK]` | Raccourci critique conforme |
| `[CRITIQUE — MAUVAISE CIBLE]` | Raccourci critique défaillant — réparer immédiatement |

---

## 5. PROCÉDURE DE RÉPARATION

### Réparation des raccourcis (tous les 9)

```bash
bash /opt/trading/student/bin/install_shortcuts.sh
```

Puis re-valider :

```bash
bash /opt/trading/student/validation/validate_student_live.sh
```

### Si `install_shortcuts.sh` échoue (droits sudo)

```bash
sudo bash /opt/trading/student/bin/install_shortcuts.sh
```

### En cas de regression structurelle (fichiers sources manquants)

```bash
cd /opt/trading
git status
git checkout sot/mainline
git pull origin sot/mainline
```

---

## 6. POINTS DE REPRISE ASSOCIÉS

| Point | État |
|---|---|
| `GO_STUDENT_LIVE_VALIDATION_PACK_01` | LIVRÉ — pack créé le 2026-03-20 |
| Items 1–4 LEGACY_CALLERS_INVENTORY | CORRIGÉ (passe précédente) |
| Item 5 LEGACY_CALLERS_INVENTORY | EN ATTENTE — vérifiable par ce pack |
| `GO_STUDENT_PHASE2_MIGRATION_01` | PARTIEL — validation live différée à ce pack |

---

## 7. LIMITE DE CE PACK

Ce pack valide la structure et les raccourcis. Il ne valide **pas** :
- L'exécution réelle des modèles DeepSeek (dépendance réseau/API)
- Le bon fonctionnement des modules `deepseek_thinking` / `deepseek_response` (dépendances externes)
- L'état des sessions actives (tmux, screen)
- La cohérence de l'environnement Python/virtualenv

Pour ces vérifications approfondies, utiliser `GO_STUDENT_DEEP_RUNTIME_AUDIT_01` (chantier différé).
