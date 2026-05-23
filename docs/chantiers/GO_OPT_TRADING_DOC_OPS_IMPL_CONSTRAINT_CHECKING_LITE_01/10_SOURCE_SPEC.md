# 10_SOURCE_SPEC

## Sources canoniques
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01/30_SELECTED_AUTOMATION_SHORTLIST.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01/50_NEXT_IMPLEMENTATION_GO_SPEC.md`

## Besoins fonctionnels
1. **Détection des changements** : Utiliser `git` pour lister les fichiers modifiés, ajoutés, supprimés ou non suivis.
2. **Analyse des contraintes** :
   - Lire le frontmatter du `00_INITIAL_PROJECT_DOC.md` du chantier courant.
   - Chercher des tags ou des champs spécifiques (ex: `CONSTRAINTS: [DOC_ONLY]`).
   - Priorité aux arguments CLI si fournis.
3. **Logique de validation** :
   - `DOC_ONLY` : 
     - OK : `docs/**/*`
     - FAIL : tout le reste (`scripts/`, `modules/`, `tests/`, etc.)
   - `READ_ONLY` :
     - FAIL : tout changement détecté par Git.
4. **Reporting** :
   - Afficher la liste des fichiers en violation.
   - Résumer le statut (PASS/FAIL).
   - Support optionnel du JSON pour intégration future.

## Besoins techniques
- Python 3.x (sans dépendances externes lourdes si possible, privilégier la bibliothèque standard).
- Utilisation de `subprocess` pour appeler Git.
- Parsing simple du YAML frontmatter (via regex pour éviter `PyYAML` si on veut rester "lite", ou bien assumer sa présence si déjà utilisé dans le repo).
