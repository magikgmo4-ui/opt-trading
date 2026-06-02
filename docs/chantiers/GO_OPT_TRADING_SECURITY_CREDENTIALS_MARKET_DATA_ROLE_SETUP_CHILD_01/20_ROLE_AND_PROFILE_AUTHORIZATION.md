# Role and Profile Authorization

Le rôle `market_data_readonly` est essentiel pour toute machine effectuant de la collecte ou de l'analyse en temps réel.

## Statuts d'Autorisation

| Profil Machine | Statut | Action |
|----------------|--------|--------|
| `admin-trading` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `db-layer` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `fantome` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `student` | **FORBIDDEN** | Interdit. |
| `cursor-ai` | **FORBIDDEN** | Interdit. |
