# GO_OT_TRAE_CONTRADICTOIRE_CADRAGE_01 — DÉCISION CANONIQUE (CADRAGE CONTRADICTOIRE)

Date (America/Montreal) : 2026-03-14

## 1. Objet
Cadrer le bloc CONTRADICTOIRE pour `opt-trading` sans ouvrir la V1, en stabilisant :
1) la table de correspondance “taxonomie repo” ↔ “taxonomie doctrinale Trae” ;
2) la règle canonique de coexistence “standard module récent” ↔ “exceptions legacy”.

## 2. Contradiction A — Taxonomie repo vs taxonomie doctrinale Trae

### 2.1 État réel observé
Le repo porte déjà une gouvernance et un système de preuves versionnés :
- doctrine d’exécution gated : `workflow_ai/WORKFLOW.md` + `.cursorrules`
- point d’entrée unique : `docs/master_pack/mission_starter_pack/00_mission_start_guide.md`
- état canonique + exceptions runtime : `docs/master_pack/00_current_state_and_standards.md`
- preuves et décisions OT : `docs/ot/*` (closings/reports/trae)
- inventaires opposables : `registry/*_registry.yaml`
- outils opérateurs : `modules/*` (dont `validated_prompt_factory`, `trae_module_validator`)

La taxonomie Trae “Rules / Agents / Skills / MCP” n’est pas encore ouverte (V1 manquante).

### 2.2 Standard opposable (règle)
- Le repo (`docs/master_pack`, `workflow_ai`, `docs/ot`, `registry`, `modules`) est la source de vérité du projet.
- Les “packs Trae” (`trae_pack_texts/trae_pack/*`) sont des helpers transport/format, non opposables quand ils contredisent le repo.

### 2.3 Legacy toléré
- Toute formulation Trae (packs) est tolérée si elle ne contredit pas le starter pack, le workflow, le kanban, ou la registry.
- Les artefacts “Trae V1” restent manquants jusqu’à décision explicite d’ouverture.

### 2.4 Table de correspondance (repo ↔ Trae)

| Zone repo | Rôle repo | Couche Trae correspondante | Statut canonique |
|---|---|---|---|
| `docs/master_pack/*` | Standards, exceptions, règles projet | Rules (repo-first) | OPPOSABLE |
| `workflow_ai/WORKFLOW.md` + `.cursorrules` | Doctrine gated + GO/STOP | Rules (process) | OPPOSABLE |
| `workflow_ai/templates/*` | Templates d’exécution | Rules (process templates) | OPPOSABLE |
| `docs/ot/closings/*` | Clôtures (statut + reprise) | Evidence / Audit log | OPPOSABLE |
| `docs/ot/reports/*` | Rapports (preuves) | Evidence / Audit log | OPPOSABLE |
| `docs/ot/trae/*` | Notes/matrices/décisions Trae (repo) | Evidence + Decisions | OPPOSABLE |
| `docs/ot/kanban/*` | Statuts + priorités + suite | Rules (state machine) | OPPOSABLE |
| `registry/*_registry.yaml` | Inventaires modules/wrappers | Rules (inventory) | OPPOSABLE |
| `modules/*` | Capacités versionnées (outils) | Implémentation (hors V1) | OPPOSABLE |
| `scripts/*` | Runtime layers & exceptions (prod) | Runtime (source finale) | OPPOSABLE |
| `trae_pack_texts/trae_pack/*` | Helpers Trae | Helpers (non canonique) | SUPPORT |

### 2.5 Risque si non clarifié
- Confusion “où est la vérité” (packs vs repo) → dérive et missions incohérentes.
- Tentation d’ouvrir V1 (Rules/Agents/Skills/MCP) sans mapping stable → architecture documentaire instable.

## 3. Contradiction B — Standard module récent vs exceptions legacy

### 3.1 État réel observé
Deux générations coexistent :
- modules récents : scripts `cmd.sh/menu.sh/sanity.sh` à la racine du module (standard) ; wrappers déclarés en registry.
- modules legacy : scripts sous `modules/<module>/scripts/*` ou noms `sanity_check.sh` ; acceptés mais signalés comme legacy par le validator.

En parallèle, il existe des couches runtime non-modulaires et/ou gelées :
- `scripts/student/` (GELÉ), `scripts/reseau_ssh/` (EXCEPTION), `scripts/admin_trading/` (runtime layer), `scripts/desk_pro_*.sh` (legacy compat).

### 3.2 Standard opposable (règle)
Un module “standard opposable” est un module qui respecte simultanément :
1) déclaration dans `registry/modules_registry.yaml`,
2) wrappers déclarés dans `registry/wrappers_registry.yaml` (si exposés),
3) scripts compatibles symlink `/usr/local/bin` (règle `readlink -f`),
4) conformité validée par `trae_module_validator` au moins au niveau “OK” (warnings acceptables si legacy explicitement assumé).

### 3.3 Legacy toléré (grandfathering)
Legacy est toléré uniquement si :
- il est explicitement classé (GELÉ/EXCEPTION/LEGACY) dans le master pack ou une matrice OT,
- il n’est pas promu comme entrypoint canonique quand une alternative standard existe,
- toute création/installation de wrapper global passe par la registry (sinon divergence non tolérée).

### 3.4 Règle de coexistence (canonique)
- Ne pas “normaliser” un legacy par déplacement/refactor sans mission dédiée et preuves terrain.
- Si une mission touche un module legacy : on corrige localement, on documente, et on garde le legacy compatible ; migration = chantier séparé.
- Si un wrapper global existe (ou est nécessaire) : il doit être déclaré dans `wrappers_registry.yaml` et testé (sanity/smoke) ; sinon statut “divergent non toléré”.

### 3.5 Risque si non clarifié
- Rupture de prod par “nettoyage” des scripts runtime (zones gelées).
- Installations de wrappers hors registry → gouvernance cassée (impossible de savoir ce qui est réellement exposé).

## 4. Prérequis d’ouverture de la V1 (sans la lancer ici)
V1 peut être ouverte seulement si :
1) cette décision est référencée par le kanban comme cadrage CONTRADICTOIRE,
2) la table repo↔Trae est acceptée (repo-first + rôle des helpers),
3) la règle standard↔legacy est acceptée (grandfathering + registry obligatoire),
4) aucun refactor de normalisation n’est lancé “par défaut” (tout chantier legacy doit être explicite).

## 5. Point de reprise
- Suite recommandée : `GO_OT_NEXT_MISSION_SELECTION_01` (décider explicitement : ouvrir Rules V1 ou traiter une divergence non tolérée prioritaire).
