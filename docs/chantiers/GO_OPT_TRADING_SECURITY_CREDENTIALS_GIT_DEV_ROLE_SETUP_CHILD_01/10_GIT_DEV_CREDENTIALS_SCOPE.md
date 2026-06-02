# Git Dev Credentials Scope

Les credentials suivants sont nécessaires pour le rôle `git_dev` :

| Credential ID | Env Var | Type | Description |
|---------------|---------|------|-------------|
| `gh_token` | `GH_TOKEN` | `auth_token` | Token d'accès GitHub pour les opérations CLI (`gh pr create`, etc.). |
| `git_author_name` | `GIT_AUTHOR_NAME` | `string` | Nom de l'auteur des commits Git. |
| `git_author_email` | `GIT_AUTHOR_EMAIL` | `string` | Email de l'auteur des commits Git. |

## Sécurité du Token
Le `GH_TOKEN` doit avoir le périmètre minimal nécessaire (repo, workflow) et ne jamais être exposé.
