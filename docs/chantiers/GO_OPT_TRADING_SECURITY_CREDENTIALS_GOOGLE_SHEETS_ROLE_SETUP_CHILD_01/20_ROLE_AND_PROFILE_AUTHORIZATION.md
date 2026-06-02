# Role and Profile Authorization

Conformément au registre `machines.yaml`, les profils suivants sont autorisés à porter le rôle `google_sheets_writer` :

## Statuts d'Autorisation

| Profil Machine | Statut | Action |
|----------------|--------|--------|
| `admin-trading` | **AUTHORIZED_ACTIVE** | Activé par défaut (centralisation des rapports). |
| `db-layer` | **ELIGIBLE_DISABLED_BY_DEFAULT** | Éligible mais non actif. |
| `fantome` | **ELIGIBLE_DISABLED_BY_DEFAULT** | Éligible mais non actif. |
| `student` | **FORBIDDEN** | Interdit. |
| `cursor-ai` | **FORBIDDEN** | Interdit. |
