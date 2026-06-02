# Data Center Credentials Scope

Les credentials suivants sont nécessaires pour le rôle `datacenter` :

| Credential ID | Env Var | Type | Description |
|---------------|---------|------|-------------|
| `db_host` | `DB_HOST` | `host` | Adresse de l'hôte de la base de données. |
| `db_user` | `DB_USER` | `username` | Nom d'utilisateur pour la connexion DB. |
| `db_password` | `DB_PASSWORD` | `password` | Mot de passe pour la connexion DB. |

## Sécurité des accès
Le rôle `datacenter` donne un accès direct aux données persistantes du projet. Le mot de passe doit être traité comme un secret critique.
