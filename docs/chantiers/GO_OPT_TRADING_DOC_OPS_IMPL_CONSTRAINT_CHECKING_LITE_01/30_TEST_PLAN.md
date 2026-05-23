# 30_TEST_PLAN

## Tests unitaires (`tests/ai/workers/test_doc_ops_constraint_check.py`)
Utilisation de `pytest`.

### Scénarios de test :
1. **Validation Git** : Mock de `subprocess.run` pour simuler différents états Git.
   - `git diff` vide + `git ls-files` vide => PASS (tous modes).
   - `git diff` avec `docs/test.md` => PASS en `DOC_ONLY`.
   - `git diff` avec `scripts/test.py` => FAIL en `DOC_ONLY`.
   - `git diff` non vide => FAIL en `READ_ONLY`.
2. **Validation Parsing Frontmatter** :
   - Fichier avec `DOC_ONLY` dans le texte => Détection correcte.
   - Fichier sans contrainte => PASS par défaut (ou comportement à définir).
3. **Arguments CLI** :
   - `--mode DOC_ONLY` écrase la détection automatique.
   - `--json` produit un JSON valide sur stdout.
4. **Gestion d'erreurs** :
   - Fichier initial doc absent => Exit 2.
   - Git indisponible => Erreur contrôlée.

## Tests d'intégration (Manuels)
1. Créer un fichier bidon dans `docs/`.
2. Lancer le script avec `--mode DOC_ONLY` => Doit passer.
3. Créer un fichier bidon dans `scripts/`.
4. Lancer le script avec `--mode DOC_ONLY` => Doit échouer.
