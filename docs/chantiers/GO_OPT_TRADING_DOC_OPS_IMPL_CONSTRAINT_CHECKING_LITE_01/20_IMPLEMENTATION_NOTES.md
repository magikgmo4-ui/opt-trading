# 20_IMPLEMENTATION_NOTES

## Architecture du script
Le script `doc_ops_constraint_check.py` sera structuré comme suit :
1. **Parser d'arguments** : `argparse`.
2. **Git Wrapper** : Fonctions simples pour extraire les fichiers changés.
3. **Constraint Engine** : Cœur de la logique de filtrage.
4. **Formatter** : Sortie console colorée (si possible) et JSON.

## Stratégie de parsing Frontmatter
Pour rester léger et éviter une dépendance obligatoire à `PyYAML` (si non présente), on utilisera une approche par regex pour extraire le bloc `--- ... ---` et chercher les mots-clés `DOC_ONLY` ou `READ_ONLY`.

## Gestion du périmètre DOC_ONLY
On autorisera :
- `docs/**`
- `docs/index/inbox/**` (déjà inclus dans `docs/**` mais mentionné pour clarté).

On bloquera explicitement :
- `.github/**`
- `scripts/**`
- `modules/**`
- `tests/**` (Sauf si le chantier est technique, mais ici on vise les chantiers purement documentaires).
- `config/**`, `data/**`, `runtime/**`
- Fichiers racines (`.gitignore`, `requirements.txt`, etc.)

## Gestion de READ_ONLY
Toute ligne retournée par `git status --porcelain` ou `git diff` est une violation.
