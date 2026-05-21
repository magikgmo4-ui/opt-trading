---
doc_id: GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01_CONTRACTS
doc_type: bridge_contracts
go_id: GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01
status: draft
---

# 20_BRIDGE_CONTRACTS

## Airtable

```yaml
app_id: airtable
purpose: Base de données légère pour inventaires, status, configurations
source_of_truth_rank: 3
allowed_reads:
  - bases partagées (read-only)
  - enregistrements par vue
allowed_writes:
  - mise à jour de champs prédéfinis (via API token)
forbidden_actions:
  - suppression de bases
  - modification de schéma
  - écriture sans approval_gate
required_env_vars:
  - AIRTABLE_API_TOKEN
  - AIRTABLE_BASE_ID
dry_run_mode: true
approval_gate: human_approve
audit_log: true
rollback_or_compensating_action: snap avant écriture, restore possible dans les 24h
evidence_ref: modules/airtable_bridge/
```

## ClickUp

```yaml
app_id: clickup
purpose: Gestion de tâches humaines, planification, suivi
source_of_truth_rank: 2
allowed_reads:
  - tâches, listes, espaces (read-only)
allowed_writes:
  - création/mise à jour de tâches (via API)
forbidden_actions:
  - suppression d'espaces
  - modification des permissions
  - archivage de listes sans approval
required_env_vars:
  - CLICKUP_API_TOKEN
  - CLICKUP_TEAM_ID
dry_run_mode: true
approval_gate: human_approve
audit_log: true
rollback_or_compensating_action: annotation de l'état précédent dans le task description
evidence_ref: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md
```

## Botpress

```yaml
app_id: botpress
purpose: Chatbot, interface utilisateur pour automation
source_of_truth_rank: 4
allowed_reads:
  - conversations, logs, users
allowed_writes:
  - envoi de messages
  - mise à jour de variables de conversation
forbidden_actions:
  - suppression de bot
  - modification des workflows
  - export de données utilisateur
required_env_vars:
  - BOTPRESS_API_TOKEN
  - BOTPRESS_BOT_ID
dry_run_mode: true
approval_gate: human_approve
audit_log: true
rollback_or_compensating_action: historique de conversation permet de restaurer un état
evidence_ref: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md
```

## Google Sheets

```yaml
app_id: google_sheets
purpose: Export de données, tableaux de bord, reporting
source_of_truth_rank: 3
allowed_reads:
  - plages de cellules, feuilles entières
allowed_writes:
  - mise à jour de cellules (plages définies)
forbidden_actions:
  - suppression de feuilles
  - modification des permissions de partage
  - écriture en dehors des plages définies
required_env_vars:
  - GOOGLE_SHEETS_CREDENTIALS
  - GOOGLE_SHEETS_SPREADSHEET_ID
dry_run_mode: true
approval_gate: human_approve
audit_log: true
rollback_or_compensating_action: snap des données avant écriture, restore via historique Sheets
evidence_ref: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md
```

## Telegram

```yaml
app_id: telegram
purpose: Notifications, alertes, signaux, contrôle opérateur
source_of_truth_rank: 4
allowed_reads:
  - messages (chat_id autorisé)
  - commandes utilisateur
allowed_writes:
  - envoi de messages, photos, documents
forbidden_actions:
  - suppression de messages (sauf les nôtres)
  - modification des permissions de groupe
  - envoi de fichiers depuis des chemins non autorisés
required_env_vars:
  - TELEGRAM_BOT_TOKEN
  - TELEGRAM_CHAT_ID
  - ALLOWED_CHAT_ID
dry_run_mode: false
approval_gate: none (notification only)
audit_log: true
rollback_or_compensating_action: N/A (notification, pas d'état persistant à rollbacker)
evidence_ref: config/machine_runtime_map.yml (required_env)
```

## Gmail

```yaml
app_id: gmail
purpose: Envoi de rapports, alertes par email, ingestion de données
source_of_truth_rank: 4
allowed_reads:
  - messages (boîte de réception, libellés)
allowed_writes:
  - envoi de messages
  - marquage de messages (lu, libellés)
forbidden_actions:
  - suppression de messages
  - modification des filtres
  - accès aux pièces jointes non autorisées
required_env_vars:
  - GMAIL_CREDENTIALS
  - GMAIL_USER_ID
dry_run_mode: true
approval_gate: human_approve
audit_log: true
rollback_or_compensating_action: messages envoyés dans "Sent" non modifiables ; compensation par envoi de correction
evidence_ref: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md
```

## Google Calendar

```yaml
app_id: google_calendar
purpose: Planification d'événements, rappels, cron humain
source_of_truth_rank: 4
allowed_reads:
  - événements, calendriers (read-only scope)
allowed_writes:
  - création d'événements
forbidden_actions:
  - suppression d'événements
  - modification des calendriers partagés
  - accès aux calendriers non autorisés
required_env_vars:
  - GOOGLE_CALENDAR_CREDENTIALS
  - GOOGLE_CALENDAR_ID
dry_run_mode: true
approval_gate: human_approve
audit_log: true
rollback_or_compensating_action: événement supprimable manuellement dans les 24h
evidence_ref: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md
```

## Google Drive

```yaml
app_id: google_drive
purpose: Stockage de documents, rapports, artefacts
source_of_truth_rank: 3
allowed_reads:
  - fichiers (par ID ou dossier partagé)
allowed_writes:
  - upload de nouveaux fichiers
  - mise à jour de fichiers existants
forbidden_actions:
  - suppression de fichiers
  - modification des permissions de partage
  - accès aux fichiers en dehors du dossier partagé
required_env_vars:
  - GOOGLE_DRIVE_CREDENTIALS
  - GOOGLE_DRIVE_FOLDER_ID
dry_run_mode: true
approval_gate: human_approve
audit_log: true
rollback_or_compensating_action: versionning Drive natif ; fichier précédent récupérable dans les 30 jours
evidence_ref: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md
```

## Figma

```yaml
app_id: figma
purpose: Design, maquettes, UI references
source_of_truth_rank: 5
allowed_reads:
  - fichiers et composants (read-only)
allowed_writes:
  - commentaires
forbidden_actions:
  - modification de designs
  - suppression de fichiers
  - export de ressources non autorisées
required_env_vars:
  - FIGMA_API_TOKEN
  - FIGMA_FILE_KEY
dry_run_mode: true
approval_gate: human_approve
audit_log: true
rollback_or_compensating_action: N/A (lecture seule, commentaires seulement)
evidence_ref: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md
```

## LocalCMS

```yaml
app_id: localcms
purpose: Cockpit opérateur, état système, contrôles
source_of_truth_rank: 2
allowed_reads:
  - toutes les pages (automation, workers, jobs, approvals, ledger, signals)
allowed_writes:
  - mise à jour de pages (contenu contrôlé)
  - activation de safe buttons
forbidden_actions:
  - modification des routes
  - modification des permissions
  - activation de kill switch sans double confirmation
required_env_vars:
  - LOCALCMS_URL
  - LOCALCMS_API_KEY
dry_run_mode: true
approval_gate: dual_confirm (pour kill switch)
audit_log: true
rollback_or_compensating_action: état précédent conservé dans le ledger ; restore via page d'historique
evidence_ref: registry/ui_surfaces_registry.yaml
```
