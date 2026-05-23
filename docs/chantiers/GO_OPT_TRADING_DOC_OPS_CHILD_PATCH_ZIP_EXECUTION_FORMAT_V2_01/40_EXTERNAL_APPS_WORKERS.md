---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_EXTERNAL_APPS_WORKERS
doc_type: external_apps_workers
repo: opt-trading
project: opt-trading
module: external_apps
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
status: draft_canonical
lifecycle_stage: opening
surface: chantier
source_kind: canonical
updated_at: 2026-05-22
topic_keys:
  - external_apps
  - workers
  - gates
  - bridge_contracts
---

# 40_EXTERNAL_APPS_WORKERS

## 1_ROLE

Les apps externes sont des workers de surface, pas des sources souveraines de gouvernance.

## 2_APPS_UTILISABLES

| App | Usage possible | Gate | Statut pour ce GO |
| --- | --- | --- | --- |
| ClickUp | creer/suivre tache humaine | human_approve | OPTIONAL |
| Telegram | notifier l'ouverture ou le resultat | none pour notification | OPTIONAL |
| LocalCMS | afficher statut cockpit | human_approve selon action | OPTIONAL |
| Airtable | inventaire leger | human_approve pour write | SKIP |
| Google Sheets | export tableau | human_approve pour write | SKIP |
| Gmail | rapport email | human_approve | SKIP |
| Calendar | planification rappel | human_approve | SKIP |
| Drive | stocker artefact | human_approve | SKIP |
| Figma | commentaire/design | human_approve | SKIP |
| Botpress | interface conversationnelle | human_approve | SKIP |

## 3_CONTRACT_RULES

Pour chaque app :

- respecter allowed_reads ;
- respecter allowed_writes ;
- bloquer forbidden_actions ;
- utiliser dry-run si defini ;
- exiger approval_gate si defini ;
- produire audit_log ;
- definir rollback ou compensation ;
- produire evidence_ref.

## 4_APP_WORKER_OUTPUT

Tout worker app externe doit produire :

```yaml
app_id: <app>
action: <read|write|notify|skip>
gate: <none|dry_run|human_approve|dual_confirm>
input_ref: <path or id>
output_ref: <path or id>
evidence_ref: <path or url>
rollback_ref: <path or procedure>
status: <SKIPPED|DRY_RUN_PASS|PASS|BLOCKED>
```

## 5_VERDICT_FOR_THIS_GO

Aucune app externe n'est requise pour appliquer ce patch. Les apps peuvent etre utilisees seulement pour suivi ou notification, avec gates appropries.
