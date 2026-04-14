# TRAE MISSION STARTER PACK (2026-03-12)

Ce pack définit le standard de démarrage pour toute nouvelle mission Trae sur le projet `opt-trading`.
Il garantit que l'agent part des bonnes sources de vérité et évite les pièges connus.

## 0. OUVERTURE DE SESSION (POINT D’ENTRÉE UNIQUE)
Ordre canonique de lecture (machine-first) :
1.  **Règles / standards** : `docs/master_pack/00_current_state_and_standards.md`
2.  **Dernière clôture pertinente** : le dernier `docs/ot/closings/OT_*_CLOSING*.txt` lié au chantier concerné
3.  **Kanban (source of truth)** : `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
    **Synthèse kanban** : `docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md`
4.  **Point de reprise actif** : le `GO_...` indiqué par la clôture et/ou le kanban
5.  **Scan réel (repo)** : `git rev-parse --short HEAD` + `git status` (détecter un tree “dirty” avant d’agir)
6.  **Matrices runtime** (si la mission touche au runtime) :
    - `docs/ot/trae/OT_OPS_05_RUNTIME_EXCEPTION_MATRIX.md`
    - `docs/ot/trae/OT_OPS_05B_DESK_PRO_ENTRYPOINT_MATRIX.md`

Règle : une clôture n’est pas considérée propre tant que **doc canonique + kanban + point de reprise** ne sont pas alignés (voir aussi `workflow_ai/WORKFLOW.md`).

Priorité canonique en cas de conflit :
1.  État réel prouvé (repo/runtime/logs/sorties récentes)
2.  Workflow canonique projet (`workflow_ai/WORKFLOW.md`)
3.  Starter pack mission (`docs/master_pack/mission_starter_pack/*`)
4.  Kanban (source of truth)
5.  Packs TRAE (helpers)

Packs TRAE (helpers, non canoniques repo) :
- `trae_pack_texts/trae_pack/TRAE_SESSION_OPENING_PACK_V1.1.txt`
- `trae_pack_texts/trae_pack/TRAE_CLOSURE_TEMPLATE_V1.1.txt`
Ils servent de support “transport / cadrage / continuité” et ne doivent pas contredire le starter pack repo.

## 1. SOURCES DE VÉRITÉ ABSOLUES (À LIRE EN PREMIER)
Avant toute action, l'agent **DOIT** lire :
1.  **`docs/master_pack/00_current_state_and_standards.md`** : L'état canonique du projet (Modules, Wrappers, Exceptions).
2.  Si la mission touche au runtime / aux scripts machine / aux entrypoints : lire
    - `docs/ot/trae/OT_OPS_05_RUNTIME_EXCEPTION_MATRIX.md` (divergences Runtime/Repo)
    - `docs/ot/trae/OT_OPS_05B_DESK_PRO_ENTRYPOINT_MATRIX.md` (entrypoints Desk Pro)

## 2. RÈGLES D'OR (ANTI-DÉRIVE)
1.  **Respecter le Runtime Machine** : Ne jamais supprimer ou modifier `scripts/student/`, `scripts/admin_trading/`, `scripts/reseau_ssh/` sans preuve absolue. Ce sont les couches d'intégration actives.
2.  **Méfiance sur les Modules** : Un dossier dans `modules/` n'est pas forcément un exécutable (Ex: `modules/desk_pro/` est une librairie core, `modules/deepseek_student/` est incomplet).
3.  **Pas de Wrapper Spéculatif** : Ne jamais créer de wrapper distant (admin -> student) tant que le besoin n'est pas prouvé par un ticket opérateur.
4.  **Usage du Hub** : L'entrypoint opérateur par défaut est `menu-ops_menu_hub`.

## 3. CLASSIFICATION DE MISSION
Chaque mission doit être classée dans l'un des types suivants :
- **AUDIT** : Observation sans modification (Livrable : Rapport + Matrice).
- **PATCH LOCAL** : Correction ciblée sur un script/module existant (Pas de refactor large).
- **MODULE DURABLE** : Création/Mise à jour d'un module standard (Doit respecter le `workflow_post_change_v2`).
- **SIGNALISATION** : Ajout de documentation/README pour figer un état (Ex: Freeze Note).
- **RUNBOOK** : Création de procédure opérateur (Doit être testé sur cible).

Continuité canonique (obligatoire avant exécution) :
- besoin initial
- objectif final visé
- plan validé
- état réel de départ
- gap
- prochain GO
- fils / rôles (machine / IA / IDE / repo-produit)

## 4. FORMAT DE LIVRABLE STANDARD
Toute mission doit se conclure par :
1.  **Rapport de Clôture** (`docs/ot/closings/OT_XXX_CLOSING.txt`) : Résumé des actions, statut final, prochain point de reprise.
2.  **Mise à jour du Master Pack** (Si applicable) : Refléter les changements d'architecture ou de standard.
3.  **Mise à jour Kanban / Source of Truth** : Statut de la mission + point de reprise alignés avec la clôture.
4.  **Preuve de Validation** : Trace d'exécution ou analyse statique confirmant le résultat.
5.  **Preuve gating GO/STOP** : Mentionner explicitement dans la clôture l’un des statuts suivants : `prouvée`, `partielle`, ou `non prouvable par lecture repo seule`.

## 5. POINT DE REPRISE (NEXT STEP)
Toujours indiquer clairement quelle est l'étape logique suivante.
Si une zone est laissée floue, créer une note "TODO" explicite ou un ticket virtuel.
