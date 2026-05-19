---
doc_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01_EXTERNAL_APPS_MAPPING
doc_type: visual_mapping
repo: opt-trading
project: opt-trading
module: ui_localcms_figma
go_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01
status: open
lifecycle_stage: mapping
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - airtable
  - botpress
  - repo-kg
  - clickup
  - figma
  - localcms
---

# 30_EXTERNAL_APPS_VISUAL_MAPPING

## Objectif

Définir comment Figma représente visuellement la chaîne apps externe déjà établie sans la remplacer.

## Chaîne apps retenue

```text
Airtable → Botpress → Repo KG → ClickUp
```

La chaîne garde ses rôles fonctionnels. Figma représente les vues, les états, les parcours et les surfaces d'opérateur.

## Airtable

Rôle fonctionnel : data légère, journal, backtests, signaux, propositions, résultats.

Représentation Figma :
- table `signals` ;
- table `propositions` ;
- table `trades` ;
- table `learning_sessions` ;
- card `last write` ;
- badge `table missing / ready / stale`.

Vues LocalCMS concernées :
- `Apps Connectors Status` ;
- `Datasheet PnL Central` ;
- `External Apps Mobile`.

## Botpress

Rôle fonctionnel : bot conversationnel, workflows opérateur, interface commandée au-dessus de Telegram.

Représentation Figma :
- flow approval `proposition → approve/reject` ;
- état bot `online/offline/simulated/pass` ;
- écran mobile de proposition formatée ;
- fallback si Telegram E2E non fermé.

Vues LocalCMS concernées :
- `Apps Connectors Status` ;
- `Strict Workers Board` ;
- `Mobile Operator Snapshot`.

## Repo KG

Rôle fonctionnel : graphe repo-first, navigation multi-angles, cartographie surfaces/modules.

Représentation Figma :
- graphe simplifié `machines → modules → GO → apps` ;
- vue `KG Repo Explorer` ;
- liens entre LocalCMS, Desk Pro, OpenClaw, workers, apps externes ;
- légende source canonique vs support.

Vues LocalCMS concernées :
- `KG Repo Explorer` ;
- `GO Roadmap Cockpit` ;
- `Health Aggregator`.

## ClickUp

Rôle fonctionnel : tâches, GO, statuts, reprises, suivi machine/branche.

Représentation Figma :
- kanban GO ;
- roadmap cockpit ;
- cartes `GO_ID / machine / branch / PR / status / NEXT_GO` ;
- badges `open / blocked / merged / closeout`.

Vues LocalCMS concernées :
- `GO Roadmap Cockpit` ;
- `External Apps Mobile` ;
- `Mobile Operator Snapshot`.

## Mapping global

| App | Fonction | Vue Figma | Vue LocalCMS |
| --- | --- | --- | --- |
| Airtable | data/journal | tables + last write | apps status / PnL |
| Botpress | workflow opérateur | approval flow | workers / mobile |
| Repo KG | cartographie | graph explorer | KG repo |
| ClickUp | GO/tasks | roadmap cards | GO cockpit |

## Invariant

Figma montre la forme et les parcours. Les données réelles restent dans les apps, le repo ou LocalCMS. Figma n'a aucune autorité de mise à jour.
