# OT JOURNAL GO MATRIX V1

Date (America/Montreal) : 2026-04-09
Statut : ACTIVE
Classe : PATCH_LOCAL

## 1. Objet
Définir une matrice compacte des `GO_...` actifs ou candidats, générée depuis les sources canoniques déjà opposables, afin de rendre la reprise opératoire plus lisible sans créer une seconde source de vérité.

## 2. Doctrine
- `journal.md` reste la chronologie brute append-only.
- `journal/steps/*` restent les preuves détaillées de sessions.
- `docs/ot/kanban/*` restent la source de vérité statut/gouvernance.
- `sot/mainline` reste l’unique branche canonique de continuité.
- `journal/index/ACTIVE_GO_MATRIX.*` est une vue générée de lecture/reprise, pas un pilotage manuel.

## 3. Sources de génération
- `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
- `docs/ot/trae/OT_TRAE_SESSION_REPRISE.md`
- `docs/ot/closings/OT_*_CLOSING*.txt` liés au `GO`
- Contexte machine/git d’exécution : hostname + branche courante

## 4. Règles minimales
- Un `GO` est `ACTIVE` s’il apparaît dans un point de reprise courant ou un point actif conservé.
- Un `GO` est `CANDIDATE` s’il n’est vu que dans un point candidat.
- `last_established` prend la date documentaire canonique la plus récente trouvée parmi les références retenues.
- `next_step` est dérivé des bullets explicites de reprise quand elles existent.
- `canonical_docs` liste les docs canoniques à relire pour reprendre.
- `evidence_refs` pointe vers des références `path:line` observables dans le repo.

## 5. Champs V1
- `go_id`
- `title`
- `nature`
- `owner_machine`
- `repo`
- `continuity_branch`
- `work_branch`
- `state`
- `last_established`
- `next_step`
- `canonical_docs`
- `evidence_refs`
- `updated_at`
- `tags`

## 6. Sorties attendues
- `journal/index/ACTIVE_GO_MATRIX.md`
- `journal/index/ACTIVE_GO_MATRIX.json`

## 7. Surface opérateur
- `cmd-journal_de_bord go_matrix`
- `cmd-journal_de_bord go_matrix_refresh`

## 8. Non-objectifs
- Aucun statut manuel doublonné.
- Aucun stockage DB.
- Aucun service long-run.
- Aucun déplacement du rôle canonique du kanban.
