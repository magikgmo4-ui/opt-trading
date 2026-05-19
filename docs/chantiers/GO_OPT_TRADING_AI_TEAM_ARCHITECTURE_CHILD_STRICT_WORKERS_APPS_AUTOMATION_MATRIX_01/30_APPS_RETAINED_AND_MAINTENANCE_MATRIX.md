---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01_APPS_MATRIX
doc_type: app_matrix
repo: opt-trading
project: opt-trading
module: matrix
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01
status: draft_canonical
lifecycle_stage: matrix
topic_keys:
  - opt-trading
  - apps
  - clickup
  - repo_kg
  - airtable
  - botpress
  - tradingview
  - telegram
  - sheets
  - figma
  - localcms
  - openclaw
  - github
  - memory_bricks
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/10_TRACKING_APPS_CORE_TABLE.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/05_OPERATIONAL_RUNTIME_PLAN.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 30_APPS_RETAINED_AND_MAINTENANCE_MATRIX

## Matrice des Apps Retenues et Surfaces Connexes

### Apps Validées (plan product usage atlas)

| App | Rôle produit | Branche parent | Statut courant prouvé | Données à tenir à jour | Source canonique | Fréquence mise à jour proposée | Automatisable | Risques | Garde-fous | GO enfant recommandé |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ClickUp | Cockpit de pilotage GO / machines / branches / statuts / reprises | go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01 | USABLE_LIMITED (Free plan limits) | Statuts GO, champs GO_ID, parent, machine, branche, PR/commit, validation, NEXT_GO, RESUME_POINT | Repo (GO_INDEX.md, BRANCH_STATE.md) | Hebdomadaire ou par closeout de GO | Semi-automatisable (task_tracker worker) | Plan gratuit limite (statuses, dashboards, templates) | Ne pas remplacer GO_INDEX/BRANCH_STATE/REPRISE | GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01 |
| Repo KG | Cartographie repo-first / knowledge graph / navigation multi-angles | go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01 | USABLE_NOW (Producer + bundle, validation.valid=true) | Noeuds APP, edges, vues V1, overlay produit/usage | Repo (graph_bundle.json) | Par changement significatif de structure repo | Automatisable (producer) | Obsolescence du bundle si non regénéré | Ne pas traiter comme source canonique | GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01 |
| Airtable | Cockpit data leger / journal / backtests / signaux / validation humaine | go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01 | DOC_ONLY_READY / GO_LIMITED | Journal, backtests, signaux, exports | Repo (modules/airtable_bridge/ à créer) | Par session d'analyse | Semi-automatisable (datasheet_writer) | Bridge repo non materialise | Ne pas utiliser comme moteur trading live ou DB massive | GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01 |
| Botpress | Routeur conversationnel controlé Telegram → OpenClaw → surfaces trading | go/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01 | SIMULATED_PASS (spec, adapter, smoke adapter, smoke Telegram E2E) | Intents, workflows, safety gate rules, API contract | Repo (spec files, api_contract) | Par changement de contrat API ou d'intents | Semi-automatisable (notification_dispatcher) | Safety gate non connectée à Telegram réel | Safety gate obligatoire, dry-run, zero trade reel automatique V1 | GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01 |

### Surfaces Connexes Opérationnelles ou Prévues

| Surface | Rôle produit | Branche parent | Statut courant prouvé | Données à tenir à jour | Source canonique | Fréquence mise à jour proposée | Automatisable | Risques | Garde-fous |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TradingView | Source de signaux via webhooks | — (webhook opérationnel) | NIVEAU 3 (webhook opérationnel admin-trading) | Templates d'alertes, webhook URL, format signal | Repo (webhook handlers) | Par changement de stratégie | Automatisé (webhook → signal_router) | Signal mal formé, webhook down | Validation format, healthcheck |
| Telegram | Notifications / interface conversationnelle | — (notification enable PASS) | NIVEAU 3 (notification enable PASS) | Chat IDs, tokens, templates de messages | .env (token, hors repo) | Continu | Automatisé (notification_dispatcher) | Token exposé, message non formaté | Token dans .env uniquement, jamais commit |
| Google Sheets | Datasheet secondaire / suivi manuel | — | NIVEAU 0 (non initié) | Aucune (à définir si activation) | — | N/A | Manuel uniquement (si activé) | Confusion avec Airtable, duplication | Différer, ne pas ouvrir sans besoin documenté |
| Figma | Maquettes UI / design system | — | NIVEAU 0 (différé) | Aucune (à définir si activation) | — | N/A | Manuel | Périmètre non défini, dérive UX sans besoin | Différer — pas dans le pipeline trade |
| LocalCMS consumer | UI lecture générale (db-layer) | go/GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01 | NIVEAU 1 (realignment done, cockpit à produire) | Cockpit lecture db-layer | Repo (spec, alignment docs) | Par changement db-layer | Semi-automatisable | Confusion avec desk_pro (UI trading réelle) | Distinguer desk_pro (admin-trading) vs LocalCMS (db-layer) |
| OpenClaw Gateway | Orchestrateur IA / builder / gateway | go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | NIVEAU 3 (opérationnel, ws://127.0.0.1:18789) | Healthcheck, routes API, prompts factory | Repo (gateway_openclaw/) | Continu | Entièrement automatisé | Exposition WAN, user openclaw utilisé hors norme | NO_WAN_EXPOSURE, user dédié openclaw (jamais sudo) |
| GitHub / PR / commits | Preuve canonique du travail | — | Continu (opérationnel) | PR status, commit history, reviews | Repo Git | Continu | Automatisé (Git hooks, CI) | Force push, secret leak, merge non revu | Branch protection, PR review, git diff avant merge |
| memory_bricks | Mémoire persistante / store learning | — | NIVEAU 3 (cmd.sh sanity PASS) | Bricks de mémoire, états, décisions | Repo (memory_bricks/) | Par closeout de GO ou décision notable | Automatisé (learning_feeder) | Surcharge de données, doublons | Ne pas remplacer la doc canonique |

## Ordre d'Activation Validé

```
ClickUp → Repo KG → Airtable → Botpress
```

Cet ordre est validé par GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01. Les surfaces connexes (TradingView, Telegram, Google Sheets, Figma, LocalCMS) s'activent selon les besoins des workers pipeline, pas avant.

## Invariants Apps

- ClickUp/Airtable/Botpress/Repo KG ne sont pas des sources canoniques — le repo est la source de vérité
- Ne pas remplacer GO_INDEX.md, BRANCH_STATE.md, REPRISE.md ou les docs parent par une app externe
- Ne pas inventer de GO depuis une app externe
- Ne pas autoriser Botpress à trader, pousser Git ou modifier production automatiquement
- Airtable n'est pas un moteur trading live ou DB massive
- Les apps sont des couches d'usage, pas des sources canoniques
