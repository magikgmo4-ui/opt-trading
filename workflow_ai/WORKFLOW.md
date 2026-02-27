# Workflow AI — Institutionnel Light (Gated)

Date de génération: 2026-02-27 10:07:42

## Objectif
Rendre le travail avec Cursor (ou tout agent) **prévisible**, **audit-able**, et **contrôlé** par validation humaine (GO/STOP).

## Gates
### Gate 0 — Cadre
- Objectif (5 lignes max)
- Contraintes (stack, sécurité, perf)
- Définition du "DONE"
- Risques connus

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
1) fichiers
2) résumé diff
3) commandes
4) expected output
5) rollback

## Validation
À la fin de chaque Gate :
- L’agent s’arrête et demande **GO** ou **STOP**.

## Policy 4 machines (rappel)
- `admin-trading` = repo truth + exécution
- `cursor-ai` = édition (Cursor)
- `db-layer` = bases & outils DB
- `student` = compute/tests lourds
