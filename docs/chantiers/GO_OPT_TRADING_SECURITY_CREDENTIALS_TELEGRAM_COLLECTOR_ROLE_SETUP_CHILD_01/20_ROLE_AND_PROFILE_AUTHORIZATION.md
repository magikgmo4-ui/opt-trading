# Role and Profile Authorization

Le projet `opt-trading` utilise un modèle d'autorisation à trois niveaux pour chaque rôle de sécurité.

## Statuts d'Autorisation
1.  **AUTHORIZED_ACTIVE** : Le profil machine est autorisé et le rôle est activé par défaut.
2.  **ELIGIBLE_DISABLED_BY_DEFAULT** : Le profil machine est autorisé (éligible), mais le rôle est désactivé par défaut.
3.  **FORBIDDEN** : Le profil machine n'est pas autorisé à porter ce rôle.

## Application au Rôle `telegram_collector`

| Profil Machine | Statut | Action |
|----------------|--------|--------|
| `fantome` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `db-layer` | **AUTHORIZED_ACTIVE** | Activé par défaut. |
| `admin-trading` | **ELIGIBLE_DISABLED_BY_DEFAULT** | Éligible mais non actif par défaut. |
| `student` | **FORBIDDEN** | Interdit. |
| `cursor-ai` | **FORBIDDEN** | Interdit. |

## Gestion de l'Éligibilité
Pour activer un rôle `ELIGIBLE_DISABLED_BY_DEFAULT`, il suffit de déplacer le rôle de la liste `eligible_roles` vers la liste `roles` dans le registre `machines.yaml`.
