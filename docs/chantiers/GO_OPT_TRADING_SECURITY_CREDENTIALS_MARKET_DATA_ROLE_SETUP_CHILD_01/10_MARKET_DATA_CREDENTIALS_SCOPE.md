# Market Data Credentials Scope

Les credentials suivants sont nécessaires pour le rôle `market_data_readonly` :

| Credential ID | Env Var | Type | Description |
|---------------|---------|------|-------------|
| `binance_api_key` | `BINANCE_API_KEY` | `api_key` | Clé API publique Binance. |
| `binance_secret_key` | `BINANCE_SECRET_KEY` | `api_key` | Clé API secrète Binance (utilisée pour signer les requêtes). |
| `coinglass_api_key` | `COINGLASS_API_KEY` | `api_key` | Clé API Coinglass pour les métriques de marché. |

## Sécurité des clés
Bien que les clés soient "Readonly", elles permettent d'accéder à des données de compte. Elles doivent être traitées comme des secrets et ne jamais être exposées dans les logs ou Git.
