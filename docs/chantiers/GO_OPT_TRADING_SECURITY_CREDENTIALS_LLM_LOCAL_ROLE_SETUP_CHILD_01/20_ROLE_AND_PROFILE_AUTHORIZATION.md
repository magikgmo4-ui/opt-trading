# Role and Profile Authorization

Le rôle `llm_local` est destiné aux machines effectuant des tâches d'IA sans dépendance aux APIs cloud.

## Statuts d'Autorisation

| Profil Machine | Statut | Action |
|----------------|--------|--------|
| `student` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `fantome` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `db-layer` | **ELIGIBLE_DISABLED_BY_DEFAULT** | Éligible pour analyse locale. |
| `admin-trading` | **FORBIDDEN** | Interdit (utilisation prod cloud privilégiée). |
| `cursor-ai` | **FORBIDDEN** | Interdit. |
