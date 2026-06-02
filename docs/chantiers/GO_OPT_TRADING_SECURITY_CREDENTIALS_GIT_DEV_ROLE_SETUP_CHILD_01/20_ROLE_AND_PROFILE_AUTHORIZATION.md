# Role and Profile Authorization

Le rôle `git_dev` est destiné aux machines de développement et d'automatisation de dépôt.

## Statuts d'Autorisation

| Profil Machine | Statut | Action |
|----------------|--------|--------|
| `cursor-ai` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `fantome` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `admin-trading` | **ELIGIBLE_DISABLED_BY_DEFAULT** | Éligible pour maintenance repo prod. |
| `db-layer` | **FORBIDDEN** | Interdit. |
| `student` | **FORBIDDEN** | Interdit. |
