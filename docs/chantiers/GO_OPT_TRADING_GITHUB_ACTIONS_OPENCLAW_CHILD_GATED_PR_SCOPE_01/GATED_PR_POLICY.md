# GATED_PR_POLICY — GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_SCOPE_01

## Rôle

```text
PR -> GitHub Actions gated-pr -> review/merge humain -> OpenClaw peut orchestrer
```

## Gates

| Gate | Rôle |
|---|---|
| `gate/preflight` | vérifier la cible `sot/mainline` et lister les fichiers modifiés |
| `gate/file-scope` | vérifier qu'un seul GO existe dans `docs/chantiers/` et que chaque fichier est dans `FILE_SCOPE.txt` |
| `gate/no-lock-overlap` | vérifier qu'aucun autre `FILE_SCOPE.txt` ne revendique les fichiers de la PR |
| `gate/tests` | vérifier l'hygiène de diff |

## Règles

1. Une PR de chantier doit cibler `sot/mainline`.
2. Une PR de chantier doit contenir un seul GO dans `docs/chantiers/GO_*/`.
3. Le GO doit avoir `docs/chantiers/<GO_ID>/FILE_SCOPE.txt`.
4. Tout fichier modifié doit être explicitement couvert par le scope.
5. Si un autre GO revendique le même fichier, la PR est bloquée.

## Limites

- Ne merge pas.
- Ne modifie pas le repo.
- Ne touche pas `admin-trading`.
- Ne remplace pas CODEOWNERS ni branch protection.
