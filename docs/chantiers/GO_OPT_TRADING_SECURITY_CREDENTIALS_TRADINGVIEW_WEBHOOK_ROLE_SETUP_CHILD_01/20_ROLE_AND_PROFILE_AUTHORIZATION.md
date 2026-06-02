# Role and Profile Authorization

Le rôle `webhook_receiver` est restreint aux machines capables d'exposer un endpoint public ou de traiter les alertes entrantes.

## Statuts d'Autorisation

| Profil Machine | Statut | Action |
|----------------|--------|--------|
| `admin-trading` | **AUTHORIZED_ACTIVE** | Activé par défaut (serveur de prod). |
| `db-layer` | **ELIGIBLE_DISABLED_BY_DEFAULT** | Éligible pour tests ou backup. |
| `fantome` | **ELIGIBLE_DISABLED_BY_DEFAULT** | Éligible pour développement local. |
| `student` | **FORBIDDEN** | Interdit. |
| `cursor-ai` | **FORBIDDEN** | Interdit. |
