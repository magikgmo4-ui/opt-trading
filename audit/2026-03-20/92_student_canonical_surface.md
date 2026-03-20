# STUDENT — FICHE CANONIQUE DE SURFACE

```
Date     : 2026-03-20
Branche  : audit/opt-trading-20260320a
Mission  : GO_STUDENT_CANONICAL_SURFACE_01
Pivot    : opt-trading / sot/mainline
Sources  : student/README.md, student/INDEX.md, student/docs/ARCHITECTURE.md
           student/docs/MASTER_INDEX.md, student/scripts/legacy/migration_map.md
           student/docs/LEGACY_CALLERS_INVENTORY.md
```

---

## 1. Définition canonique

`student` est un **sous-projet intégré à `opt-trading`**, non un repo Git séparé.

Il constitue la surface opérateur dédiée à l'environnement de calcul étudiant (IA locale, DeepSeek, lab compute) dans l'écosystème `opt-trading`.

Décision canonique formalisée dans le repo :
- racine officielle : `/opt/trading/student/`
- ce dossier est la **cible de consolidation** : les locations legacy restent en place comme sources de compatibilité jusqu'à la fin de la migration (Phase 2).

`student` ≠ machine `student` (Debian 12 headless) : la machine est une cible runtime documentée dans `infra_context_sanitized/machines/student/`. Le workstream `student` est le code et la documentation, pas la machine.

---

## 2. Surfaces et composants principaux

| Surface / Composant | Chemin dans `sot/mainline` | Statut | Rôle |
|---|---|---|---|
| Façade top-level | `student/scripts/student_cmd.sh` | CANONIQUE | Entrypoint commande global opérateur |
| Façade top-level | `student/scripts/student_menu.sh` | CANONIQUE | Entrypoint menu global opérateur |
| Façade top-level | `student/scripts/student_sanity_check.sh` | CANONIQUE | Entrypoint sanity global opérateur |
| Wrappers deepseek_student | `student/scripts/wrappers/deepseek_student_*.sh` | CANONIQUE | Façade officielle deepseek_student pour l'opérateur |
| Wrappers desk_pro_student | `student/scripts/wrappers/desk_pro_student_*.sh` | CANONIQUE | Façade officielle desk_pro côté student |
| DeepSeek hub | `student/scripts/deepseek_hub/` | CANONIQUE / TOLÉRÉ | Hub runtime commands et menu — entrypoint de second niveau |
| DeepSeek student (backend) | `student/scripts/deepseek_student/` | TOLÉRÉ / BACKEND SCOPE | Helpers backend — pas l'entrypoint opérateur privilégié |
| Installers | `student/bin/install_shortcuts.sh` | CANONIQUE | Installeur canonical des raccourcis globaux |
| Installers (repair, migrate, publish) | `student/bin/` | CANONIQUE | Outillage cycle de vie du workstream |
| Config | `student/config/shortcut_map.env` | CANONIQUE | Carte des raccourcis globaux |
| Documentation core | `student/README.md`, `student/INDEX.md`, `student/docs/` | CANONIQUE | Référence documentaire officielle |
| Exports kanban | `student/exports/kanban/` | CANONIQUE | Suivi planning et gouvernance |
| Migration map | `student/scripts/legacy/migration_map.md` | CANONIQUE | Référence de migration Phase 1 → Phase 2 |

---

## 3. Raccourcis globaux canoniques

| Raccourci | Cible canonique | Statut |
|---|---|---|
| `menu-student` | `/opt/trading/student/scripts/student_menu.sh` | CANONIQUE |
| `cmd-student` | `/opt/trading/student/scripts/student_cmd.sh` | CANONIQUE |
| `sanity-student` | `/opt/trading/student/scripts/student_sanity_check.sh` | CANONIQUE |

---

## 4. Frontière : canonique vs toléré vs legacy

### 4.1 Canonique — à utiliser

| Périmètre | Chemin | Note |
|---|---|---|
| Façade top-level | `student/scripts/student_*.sh` | entrypoints officiels stables |
| Wrappers opérateur | `student/scripts/wrappers/` | couche facade officielle deepseek_student |
| Installers | `student/bin/install_shortcuts.sh` | installer canonical (remplace les copies internes) |
| Config | `student/config/shortcut_map.env` | source de vérité des raccourcis |
| Documentation | `student/docs/` core | référence documentaire courante |

### 4.2 Toléré — valide mais pas preferred entrypoint

| Périmètre | Chemin | Raison |
|---|---|---|
| DeepSeek hub (scripts) | `student/scripts/deepseek_hub/` | hub runtime actif, mais entrypoint de second niveau |
| DeepSeek student (backend) | `student/scripts/deepseek_student/` | backend helper scope — pas l'entrypoint opérateur |
| Installers legacy internes | `student/scripts/deepseek_hub/install_shortcuts.sh`, `student/scripts/deepseek_student/install_shortcuts.sh` | toujours pointés vers l'ancien chemin modules ; remplacés par `student/bin/install_shortcuts.sh` |
| Docs legacy dans `student/` | kanban, références historiques | conservés comme mémoire de migration, pas comme guides opérateurs |

### 4.3 Legacy — sources de compatibilité uniquement, dépréciées comme entrypoints primaires

| Périmètre | Chemin | Décision |
|---|---|---|
| Scripts student legacy | `/opt/trading/scripts/student/` | déprécié — compatibility source jusqu'à Phase 2 complète |
| DeepSeek hub module legacy | `/opt/trading/modules/deepseek_hub/scripts/` | déprécié — compatibility source |
| DeepSeek student module legacy | `/opt/trading/modules/deepseek_student/scripts/` | déprécié — compatibility source |
| Docs historiques opt-trading | `/opt/trading/docs/student_deepseek_*.md`, `student_desk_pro_*.md` | référence historique uniquement — ne pas utiliser comme runbook courant |

---

## 5. Usage / rôle

`student` dans `opt-trading` couvre trois rôles opérateurs distincts :

**5.1 — Compute IA local (DeepSeek)**
Exécution de modèles DeepSeek sur la machine `student`. Entrypoint : `cmd-student`, `menu-student`.

**5.2 — Rapport et monitoring**
Rapports IA quotidiens (`daily_ai_report`), logs thinking, résumés, roadmap from events. Tous accessibles via les wrappers `student/scripts/wrappers/`.

**5.3 — Pont Desk Pro → student**
La famille `desk_pro_student_*` dans les wrappers assure la liaison entre la surface Desk Pro et la machine student (commandes, menu, sanity, infos partagées).

---

## 6. Ce qui reste à faire (Phase 2 — hors périmètre de cette fiche)

| Chantier | Statut | Référence |
|---|---|---|
| Migration Phase 2 : nettoyage des legacy locations | OUVERT / NON DÉMARRÉ | `student/docs/PHASE2_MIGRATION.md` |
| Audit des doublons | OUVERT | `student/docs/DUPLICATES_AUDIT.md` |
| Inventaire callers legacy encore actifs | PARTIELLEMENT FAIT | `student/docs/LEGACY_CALLERS_INVENTORY.md` |
| Repointer installers internes vers canonical | IDENTIFIÉ / NON FAIT | `student/docs/LEGACY_CALLERS_INVENTORY.md` §2 |

Ces chantiers ne sont pas traités dans cette passe — ils nécessitent un chantier dédié de migration Phase 2.

---

## 7. Point de reprise suivant

```
GO_STUDENT_CANONICAL_SURFACE_01 → LIVRÉ ✓

Prochain chantier student si besoin :
  GO_STUDENT_PHASE2_MIGRATION_01
  → exécuter la Phase 2 de migration (cleanup legacy locations, repoint installers,
    purge doublons) — nécessite un chantier dédié avec périmètre limité

Prochain chantier portefeuille recommandé (suite topologie) :
  GO_API_COLLECTOR_CANONICAL_MODULE_01
  → qualifier le module api collector : état fonctionnel réel, nom canonique,
    runbook minimal, décision module opt-trading ou projet séparé

  GO_RUNTIME_SURFACES_CANONICAL_MAP_01
  → carte canonique minimale admin-trading / db-layer / cursor-ai
    → rôle → surface active → repo associé
```
