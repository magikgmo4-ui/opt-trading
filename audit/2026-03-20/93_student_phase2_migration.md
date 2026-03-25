# STUDENT — RAPPORT DE MIGRATION PHASE 2

```
Date     : 2026-03-20
Branche  : audit/opt-trading-20260320a
Mission  : GO_STUDENT_PHASE2_MIGRATION_01
Pivot    : opt-trading / sot/mainline
Statut   : ÉTABLI — items runtime corrigés en amont ; validation live réalisée ;
           H01 confirmé ; résiduels H02/H03 non bloquants et hors clôture Phase 2
```

---

## 1. État réel observé au démarrage de la passe

### 1.1 Façades canoniques top-level — SAINES

| Script | Cible effective | État |
|---|---|---|
| `student/scripts/student_cmd.sh` | `$ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh` avec `ROOT=/opt/trading/student` | CANONIQUE ✓ |
| `student/scripts/student_menu.sh` | `$ROOT/scripts/deepseek_hub/deepseek_hub_menu.sh` | CANONIQUE ✓ |
| `student/scripts/student_sanity_check.sh` | `$ROOT/scripts/deepseek_hub/sanity_check_deepseek_hub.sh` | CANONIQUE ✓ |

### 1.2 Chemins legacy dans les scripts runtime — ÉTAT RÉEL

| Script | Description issue de LEGACY_CALLERS_INVENTORY | État réel observé |
|---|---|---|
| `wrappers/deepseek_student_cmd.sh` | Décrit comme pointant vers `$ROOT_DIR/modules/deepseek_hub/...` | DÉJÀ CORRIGÉ — utilise `$STUDENT_ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh` |
| `wrappers/deepseek_student_run_logged.sh` | Décrit comme pointant vers `$ROOT_DIR/modules/deepseek_hub/...` | DÉJÀ CORRIGÉ — même pattern canonique |
| `scripts/deepseek_hub/install_shortcuts.sh` | Décrit comme écrivant vers `$ROOT/modules/deepseek_hub/scripts/...` | DÉJÀ CORRIGÉ — pointe vers `$ROOT/scripts/deepseek_hub/...` |
| `scripts/deepseek_student/install_shortcuts.sh` | Décrit comme écrivant vers `$ROOT/modules/deepseek_student/scripts/...` | DÉJÀ CORRIGÉ — pointe vers `$ROOT/scripts/wrappers/...` |

**Conclusion** : les 4 items prioritaires du LEGACY_CALLERS_INVENTORY ont été corrigés avant cette passe. La migration runtime Phase 2 est **déjà exécutée**.

### 1.3 Référence PATH externe résiduelle dans `run_logged.sh`

`wrappers/deepseek_student_run_logged.sh` contient :
```bash
export PATH="$PATH:$ROOT_DIR/modules/deepseek_thinking/scripts:$ROOT_DIR/modules/deepseek_response/scripts:..."
```

**Évaluation** : ce n'est pas un chemin legacy student. Ce sont des dépendances vers les modules `deepseek_thinking` et `deepseek_response` d'`opt-trading`, activées uniquement si `cmd-deepseek_thinking` est absent du PATH. C'est une dépendance externe légitime, pas un item de migration student.

**Décision** : conservé tel quel. Ne pas toucher sans chantier dédié module-dependency.

### 1.4 Références legacy dans la documentation — ACCEPTABLES

Toutes les références aux chemins legacy dans les fichiers de documentation (`ARCHITECTURE.md`, `migration_map.md`, `kanban/KANBAN.md`, `kanban_references.md`) sont de nature documentaire/historique. Elles ne constituent pas des callers runtime.

**Décision** : conservées comme mémoire d'audit. Conforme à l'assessment initial du LEGACY_CALLERS_INVENTORY §1.

---

## 2. Changements effectivement appliqués

### 2.1 `student/docs/LEGACY_CALLERS_INVENTORY.md`

- Section §2 : chaque item runtime annoté avec son état réel (`CORRIGÉ` / `NON TRAITÉ`)
- Section §4 : tableau d'état ajouté avec colonne "État" pour chacun des 4 items prioritaires
- La description originale conservée comme mémoire d'audit

### 2.2 `student/docs/PHASE2_MIGRATION.md`

- Section "First Candidates For Replacement" : tableau d'état ajouté avec vérification 2026-03-20
- Les 3 candidats listés marqués comme CORRIGÉ ou TOLÉRÉ selon état observé
- PATH fallback externe marqué NON TRAITÉ avec justification

---

## 3. Changements préparés mais non appliqués

### 3.1 Doublons — décision documentée, cleanup non exécuté

Le `DUPLICATES_AUDIT.md` identifie et tranche clairement :

| Couche | Survivant retenu | Script à rétrécir | Décision |
|---|---|---|---|
| CMD module-level | `wrappers/deepseek_student_cmd.sh` | `deepseek_student/deepseek_student_cmd.sh` → helper backend narrow scope | DOCUMENTÉ — non retiré |
| Installer | `bin/install_shortcuts.sh` | `scripts/deepseek_hub/install_shortcuts.sh`, `scripts/deepseek_student/install_shortcuts.sh` → legacy/internal | DOCUMENTÉ — non retiré |
| Sanity | `student_sanity_check.sh` | Les 4 autres sanity scripts → internes ou scoped | DOCUMENTÉ — non retiré |
| Menu | `student_menu.sh` | Les wrapper menus → reclassifier par purpose | DOCUMENTÉ — non retiré |

**Raison du non-retrait** : suppression non justifiée par preuve que ces scripts ne sont plus appelés en production. Conforme à la contrainte "toute suppression doit être justifiée par preuve locale".

### 3.2 Alias-based fallback logic — déféré

Item 5 de la liste de rewiring du LEGACY_CALLERS_INVENTORY (dépendance aux alias globaux dans `deepseek_hub_cmd.sh`, `sanity_check_deepseek_hub.sh`) : non traité. Déféré à un chantier dédié.

---

## 4. Chemins legacy encore présents — inventaire exhaustif post-passe

| Chemin | Type | Présence dans le repo | Action requise |
|---|---|---|---|
| `/opt/trading/modules/deepseek_hub/scripts/` | legacy source upstream | oui — module opt-trading | conserver comme compatibility source |
| `/opt/trading/modules/deepseek_student/scripts/` | legacy source upstream | oui — module opt-trading | conserver comme compatibility source |
| `/opt/trading/scripts/student/` | legacy source upstream | oui — scripts top-level legacy | conserver comme compatibility source |
| `student/scripts/deepseek_hub/install_shortcuts.sh` | installer module-scoped | oui — canonical paths désormais | conserver comme convenience installer |
| `student/scripts/deepseek_student/install_shortcuts.sh` | installer module-scoped | oui — canonical paths désormais | conserver comme convenience installer |
| `student/scripts/deepseek_student/deepseek_student_cmd.sh` | helper backend narrow scope | oui | conserver — doublon documenté, survivant choisi |
| PATH `$ROOT_DIR/modules/deepseek_thinking/scripts` dans `run_logged.sh` | dépendance externe légitime | oui | ne pas toucher |

---

## 5. Commandes de validation manuelle recommandées

À exécuter sur la machine `student` après la prochaine session de travail live :

```bash
# 1. Vérifier la façade canonique
sanity-student

# 2. Vérifier la commande principale
cmd-student status

# 3. Vérifier les cibles des shortcuts globaux
ls -la /usr/local/bin/menu-student /usr/local/bin/cmd-student /usr/local/bin/sanity-student

# 4. Vérifier que les cibles pointent vers student/ et non modules/
readlink -f /usr/local/bin/cmd-student
# Attendu : /opt/trading/student/scripts/student_cmd.sh

# 5. Vérifier deepseek_student wrapper
cmd-deepseek_student show-paths
# La ligne "Hub Cmd" doit pointer vers /opt/trading/student/scripts/deepseek_hub/deepseek_hub_cmd.sh
```

---

## 6. Hypothèses restantes

| ID | Hypothèse | Impact | Action requise |
|---|---|---|---|
| H01 | Les shortcuts globaux sur la machine `student` live pointent vers les chemins canoniques | MOYEN — vérifiable seulement en live SSH | **CONFIRMÉ 2026-03-23** — 9/9 raccourcis OK. `readlink -f /usr/local/bin/cmd-deepseek_student` → `/opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh` (CONFORME). 2 warnings non bloquants (alias-based fallback item 5 — déféré, cf. §3.2). Exit code 0. |
| H02 | `deepseek_student/deepseek_student_cmd.sh` n'est pas appelé directement en production | FAIBLE — doublon documenté, survivant choisi | **NON VÉRIFIÉ EN LIVE** — shortcut `cmd-deepseek_student` confirmé canonique (pointe vers wrapper, non legacy). Callers directs de `deepseek_student/deepseek_student_cmd.sh` non audités en live. Condition readlink de `94_student_cleanup_duplicates.md` §4.2 remplie — retrait activable sur décision PM. |
| H03 | Les modules `deepseek_thinking` / `deepseek_response` sont bien présents dans `opt-trading/modules/` | FAIBLE — PATH fallback ne s'active que si absent du PATH global | **NON VÉRIFIÉ** — hors périmètre de la validation live 2026-03-23. À confirmer si chantier module-dependency ouvert. |

---

## 7. Point de reprise suivant

```
GO_STUDENT_PHASE2_MIGRATION_01 → ÉTABLI

Ce qui est fait :
  ✓ audit terrain complet des 4 items runtime prioritaires
  ✓ LEGACY_CALLERS_INVENTORY.md mis à jour avec état réel
  ✓ PHASE2_MIGRATION.md mis à jour avec vérification
  ✓ validation live exécutée sur machine student
  ✓ H01 confirmé : raccourcis canoniques OK, `cmd-deepseek_student` conforme
  ✓ `sanity-student`, `cmd-student status`, `cmd-deepseek_student show-paths` OK

Ce qui reste hors clôture Phase 2 :
  → H02 non prouvé : callers directs de `deepseek_student/deepseek_student_cmd.sh`
  → H03 non prouvé : modules `deepseek_thinking` / `deepseek_response`
  → rewiring alias-based fallback — chantier séparé
  → cleanup physique des doublons — chantier séparé, sur décision PM

Prochain point logique :
  GO_STUDENT_CLEANUP_DUPLICATES_01
  → décision PM sur le retrait de `deepseek_student/deepseek_student_cmd.sh`
    comme entrypoint opérateur
```
