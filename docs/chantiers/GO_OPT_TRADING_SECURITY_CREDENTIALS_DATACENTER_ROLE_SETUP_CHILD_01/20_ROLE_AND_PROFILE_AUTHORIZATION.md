# Role and Profile Authorization

Le rôle `datacenter` est réservé aux machines effectuant des opérations de maintenance, de stockage ou d'analyse lourde.

## Statuts d'Autorisation

| Profil Machine | Statut | Action |
|----------------|--------|--------|
| `admin-trading` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `db-layer` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `fantome` | **ELIGIBLE_DISABLED_BY_DEFAULT** | Éligible pour debug local. |
| `student` | **FORBIDDEN** | Interdit. |
| `cursor-ai` | **FORBIDDEN** | Interdit. |
