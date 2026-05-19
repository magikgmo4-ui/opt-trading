---
doc_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01_ROLE_DECISION
doc_type: decision
repo: opt-trading
project: opt-trading
module: ui_localcms_figma
go_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01
status: open
lifecycle_stage: role_decision
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - figma
  - role-decision
  - localcms
  - cockpit
  - design-reference
---

# 10_FIGMA_ROLE_DECISION

## Décision

Figma est retenu comme référence design et couche de visualisation préparatoire pour le cockpit LocalCMS mobile/web.

Figma n'est pas retenu comme app opérationnelle de la chaîne externe.

## Rôle retenu

```text
Figma = design reference / wireframes / design system / handoff futur
LocalCMS = cockpit système réel read-only
Desk Pro = cockpit trading actif
Repo = source canonique
```

## Rôle exclu

Figma ne doit pas devenir :
- source canonique ;
- registre GO ;
- base de données ;
- outil de trading ;
- runtime ;
- orchestrateur ;
- surface de validation de trade ;
- remplaçant de LocalCMS, Desk Pro, Airtable, Botpress, Repo KG ou ClickUp.

## Justification

La chaîne apps déjà établie couvre les fonctions opérationnelles :
- Airtable : données, journal, signaux, backtests ;
- Botpress : workflow conversationnel opérateur ;
- Repo KG : graphe et cartographie repo-first ;
- ClickUp : GO, tâches, statuts, reprises.

Figma ajoute une valeur différente : organiser le design et la lisibilité des surfaces que ces apps alimentent.

## Position dans l'architecture

```text
Airtable / Botpress / Repo KG / ClickUp
        ↓ données, workflows, états
LocalCMS cockpit read-only
        ↓ surface web/mobile réelle
Figma
        ↓ référence design + composants + wireframes
Code Connect phase 2 / MCP phase 3
```

## Décision finale

Figma reste utile seulement s'il est rattaché à LocalCMS et au mobile cockpit. Un fichier Figma flottant ou non référencé dans le repo n'a pas de valeur canonique.
