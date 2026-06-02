# LLM Cloud Credentials Scope

Les credentials suivants sont nécessaires pour le rôle `llm_cloud` :

| Credential ID | Env Var | Type | Description |
|---------------|---------|------|-------------|
| `openai_api_key` | `OPENAI_API_KEY` | `api_key` | Clé API pour les services OpenAI. |
| `anthropic_api_key` | `ANTHROPIC_API_KEY` | `api_key` | Clé API pour les services Anthropic (Claude). |
| `gemini_api_key` | `GEMINI_API_KEY` | `api_key` | Clé API pour les services Google Gemini. |

## Sécurité des clés
Ces clés permettent d'effectuer des appels facturés. Elles doivent être strictement protégées et ne jamais être partagées ou logguées.
