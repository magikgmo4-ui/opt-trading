# Google Sheets Credentials Scope

Les credentials suivants sont nécessaires pour le rôle `google_sheets_writer` :

| Credential ID | Env Var | Type | Description |
|---------------|---------|------|-------------|
| `google_service_account_json` | `GOOGLE_SERVICE_ACCOUNT_JSON_PATH` | `file_path` | Chemin vers le fichier JSON de la clé du Service Account. |
| `google_sheets_spreadsheet_id` | `GOOGLE_SHEETS_SPREADSHEET_ID` | `resource_id` | ID de la feuille de calcul cible. |

## Sécurité du fichier JSON
Le fichier JSON contient des clés privées sensibles. Il doit être stocké dans `/etc/opt-trading/secrets/google/` avec des permissions strictes.
