---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01_TRACKING_APPS_CORE_TABLE
doc_type: tracking_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
---

# 10_TRACKING_APPS_CORE_TABLE - Suivi explicite des 4 apps du plan initial

Ce fichier suit explicitement le plan valide :

```text
ClickUp -> Repo KG -> Airtable -> Botpress
```

## Matrice canonique initiale

| Produit | Branche parent | Produit / role final prevu | Utilisation prevue dans le setup | Etat actuel recroise | Gap restant vers produit fini |
| --- | --- | --- | --- | --- | --- |
| ClickUp | `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | Cockpit de pilotage operationnel des GO, branches, machines, PR, commits, validations et points de reprise. | Piloter humainement les GO actifs sans remplacer les preuves repo. | `USABLE_LIMITED`. Cockpit operationnel, custom fields actifs et remplis, navigation OK. Limites plan gratuit encore presentes sur statuses, dashboards et template. | Les limites UI du plan gratuit restent documentees. Ouvrir un child dedie seulement si un besoin reel ou un upgrade plan l'exige. |
| Repo KG | `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` | Projection repo-first du systeme via `graph_bundle.json`. | Naviguer vite entre GO, docs, modules, branches, gaps et resume points. | `USABLE_NOW`. Producer et bundle prouves, `validation.valid=true`, vues V1 rejouables, noeuds `APP` et edges utiles exposes. | Ajouter une vue produit / usage reel au-dessus du bundle et maintenir cette lecture comme overlay doc. |
| Airtable | `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` | Couche legere de journal, review humaine, signaux et exports. | Orchestration humaine optionnelle sans remplacer le coeur Python ni le repo. | `DOC_ONLY_READY / GO_LIMITED`. Le role produit, le schema et le chemin de finition sont documentes. Le bridge repo n'est pas encore materialise. | Creer `modules/airtable_bridge/`, finaliser les tables produit et ajouter un guide seulement apres preuve d'usage borne. |
| Botpress | `go/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01` | Routeur conversationnel controle entre Telegram, Botpress, OpenClaw et les surfaces trading. | Classifier les intentions, appliquer la safety gate, router et renvoyer un verdict structure. | `SIMULATED_PASS`. Parent, spec, adapter, smoke adapter et smoke Telegram E2E passent en simulation. | Connecter Telegram reel, webhook reel et credentials hors repo avant toute promotion au-dessus de la simulation. |

## NEXT_GO attendus

| Produit | NEXT_GO |
| --- | --- |
| ClickUp | Pas de GO obligatoire. Ouvrir un child UI completion seulement si besoin reel ou upgrade plan. |
| Repo KG | `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01` |
| Airtable | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` |
| Botpress | `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` |

## Acceptance specifique

Ce parent n'est pas PASS si :
- les 4 apps ne sont pas suivies explicitement ;
- la branche parent n'est pas indiquee ;
- l'utilisation prevue dans le setup n'est pas indiquee ;
- l'etat actuel est confondu avec le produit fini ;
- le gap restant vers produit fini n'est pas explicite ;
- Botpress est presente comme fini alors qu'il reste simule ;
- Airtable est presente comme utilisable maintenant alors que le bridge produit manque ;
- ClickUp est presente comme bloquee alors qu'elle est utilisable avec limites ;
- Repo KG est reduit a un graphe technique sans lecture produit.
