# Role and Profile Authorization

Le rôle `deskpro_user` est destiné aux profils d'étudiants et de développement local pour l'analyse de données.

## Statuts d'Autorisation

| Profil Machine | Statut | Action |
|----------------|--------|--------|
| `student` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `fantome` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `db-layer` | **ELIGIBLE_DISABLED_BY_DEFAULT** | Éligible pour debug data. |
| `admin-trading` | **FORBIDDEN** | Interdit (utilisation prod non recommandée). |
| `cursor-ai` | **FORBIDDEN** | Interdit. |
