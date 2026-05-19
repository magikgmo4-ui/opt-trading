---
doc_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01_WIREFRAME_SCOPE
doc_type: wireframe_scope
repo: opt-trading
project: opt-trading
module: ui_localcms_figma
go_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01
status: open
lifecycle_stage: design_scope
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - localcms
  - mobile-cockpit
  - web-cockpit
  - wireframes
  - figma
---

# 20_MOBILE_WEB_COCKPIT_WIREFRAME_SCOPE

## Objectif

Définir les vues Figma à produire pour figer le cockpit LocalCMS mobile et desktop avant implémentation.

## Principe

```text
Mobile = snapshot opérateur rapide
Desktop = cockpit système complet
LocalCMS = read-only au départ
Desk Pro = trading actif séparé
```

## Vues mobile prioritaires

1. `Mobile Operator Snapshot`
   - état global OK/WARN/BLOCKED ;
   - machines principales ;
   - dernier healthcheck ;
   - alerte critique ;
   - liens rapides vers Desk Pro, RustDesk, Telegram.

2. `OpenClaw Runtime Mobile`
   - gateway LIVE/DOWN ;
   - builder disponible/occupé ;
   - dernier appel ;
   - bridge MISSING/READY.

3. `TMUX Sessions Mobile`
   - sessions attendues ;
   - sessions actives ;
   - session manquante ;
   - lien attach/read-only.

4. `Strict Workers Mobile`
   - worker ;
   - état ;
   - dernière activité ;
   - prochain blocage.

5. `External Apps Mobile`
   - Airtable ;
   - Botpress ;
   - Repo KG ;
   - ClickUp ;
   - Telegram ;
   - TradingView ;
   - Google Sheets.

## Vues desktop prioritaires

1. `LocalCMS Overview`
2. `OpenClaw Runtime Status`
3. `TMUX Sessions Map`
4. `Strict Workers Board`
5. `Apps Connectors Status`
6. `Datasheet PnL Central`
7. `KG Repo Explorer`
8. `GO Roadmap Cockpit`
9. `Health Aggregator`
10. `Mobile Layout Reference`

## Design system minimal

Composants à prévoir :
- `StatusBadge`
- `HealthTile`
- `MachineCard`
- `WorkerRow`
- `GoCard`
- `PipelineStep`
- `AlertBanner`
- `MetricCard`
- `DecisionGateCard`
- `ConnectorStatusRow`

## États visuels obligatoires

```text
PASS
BLOCKED
DOWN
LIVE
MISSING
READY
DRAFT
MERGED
NIVEAU_0
NIVEAU_1
NIVEAU_2
NIVEAU_3
```

## Machines à représenter

```text
db-layer
admin-trading
cursor-ai
student
fantome
mobile
```

## DONE Figma phase 1

- un fichier Figma unique ou espace identifié ;
- pages mobile et desktop séparées ;
- composants de base nommés ;
- états visuels standardisés ;
- lien documenté dans un child GO ou closeout futur ;
- aucune dépendance runtime.
