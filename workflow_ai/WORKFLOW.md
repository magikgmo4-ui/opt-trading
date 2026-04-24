# Workflow AI — Institutionnel Light (Gated)

Date de génération: 2026-02-27 10:07:42

## Objectif
Rendre le travail avec Cursor (ou tout agent) **prévisible**, **audit-able**, et **contrôlé** par validation humaine (GO/STOP).

## Positionnement (repo opt-trading)
- Ouverture de session (point d’entrée unique) : `docs/master_pack/mission_starter_pack/00_mission_start_guide.md`
- Exécution : ce document (`workflow_ai/WORKFLOW.md`) est la doctrine canonique de conduite (gates + GO/STOP)
- Templates d’exécution : `workflow_ai/templates/specs.md` et `workflow_ai/templates/tasks.md`
- Continuité : `docs/ot/kanban/opt_trading_kanban_source_of_truth.md` + dernière clôture pertinente
- Synthèse kanban : `docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md`
- Modèle officiel missions longues / multi-étapes : `docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt`
- Prompt generation : `modules/validated_prompt_factory/README.md`
- Déploiement multi-machine : `docs/deploy_module_multi_machine_continuity.md`
- Legacy Trae/IDE : `docs/ot/trae/trae_pack_texts/README.md`

## Chaîne de responsabilité
- Orchestrator : cadre la mission, borne le scope, fixe la preuve attendue et le rollback.
- Executor : réalise le changement, liste les fichiers touchés et apporte les preuves.
- Reviewer : vérifie scope, preuves, standards et rollback, puis prononce le verdict.
- Si la mission est floue, si la preuve manque, ou si le rollback est absent, la chaîne doit se bloquer ou conclure à `REJECT`.

## Verdicts et statuts
- `ACCEPT` : livrable conforme, prouvé, intégrable sans réserve.
- `ACCEPT_WITH_NOTES` : livrable conforme avec écarts mineurs explicitement tracés.
- `REJECT` : livrable non acceptable en l'état.
- `CLOSE` : état archivé après verdict positif et alignement doc + kanban + point de reprise.
- `POINT DE REPRISE` : prochaine étape logique exploitable pour la continuité.

## Gates
### Gate 0 — Cadre
- Objectif (5 lignes max)
- Contraintes (stack, sécurité, perf)
- Définition du "DONE"
- Risques connus
- Vérification kanban : relire kanban + synthèse, puis cadrer le changement de statut attendu

### Gate 1 — Source de vérité
Créer / mettre à jour :
- `specs.md`
- `tasks.md`
- `db_schema.md` (si DB)
- `api_contract.md` (si API)

### Gate 2 — Plan (petits pas)
- Étapes atomiques
- Fichiers touchés
- Commandes & critères de succès

### Gate 3 — Backup (OBLIGATOIRE)
Avant tout nouveau module / correction :
- export patch (diff)
- état git (status)
- instructions rollback
- (option) commit/tag quand l’humain valide

### Gate 4..N — Implémentation incrémentale
Chaque incrément doit livrer :
1) fichiers touchés
2) résumé diff
3) commandes exécutées
4) preuve observée ou output attendu
5) rollback exact
6) notes ou dettes résiduelles si nécessaire

### Gate N+1 — Clôture (DOC + KANBAN + REPRISE)
Une brique/mission/module n’est pas considérée “clôturée proprement” tant que la même séquence de travail n’a pas produit :
1) mise à jour de la documentation canonique concernée,
2) mise à jour du kanban / source of truth,
3) vérification et mise à jour de la synthèse opérationnelle du kanban si un statut, une preuve, un point de reprise, une interdiction de réouverture ou l’ordre des briques a changé,
4) point de reprise propre (next step explicite),
5) passage éventuel en `CLOSE` uniquement après verdict positif et archivage cohérent.

## Validation
À la fin de chaque Gate :
- L’agent s’arrête et demande **GO** ou **STOP**.

## Policy 4 machines (rappel)
- `admin-trading` = repo truth + exécution
- `cursor-ai` = édition (Cursor)
- `db-layer` = bases & outils DB
- `student` = compute/tests lourds
