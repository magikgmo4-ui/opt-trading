---
doc_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01_CODE_CONNECT_MCP_GATES
doc_type: phase_gates
repo: opt-trading
project: opt-trading
module: ui_localcms_figma
go_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01
status: open
lifecycle_stage: phase_gates
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - code-connect
  - mcp
  - figma
  - localcms
  - security
---

# 50_CODE_CONNECT_MCP_PHASE_GATES

## Décision de phases

```text
Phase 1 = Figma design reference / wireframes / design system
Phase 2 = Code Connect
Phase 3 = MCP Figma
```

## Phase 1 — Figma design reference

Objectif : produire les wireframes et composants visuels sans connexion runtime.

Entrées :
- 20_MOBILE_WEB_COCKPIT_WIREFRAME_SCOPE.md ;
- 30_EXTERNAL_APPS_VISUAL_MAPPING.md ;
- 40_STREAM_DECK_AND_VISUAL_SUPPORT_SPEC.md.

Sorties attendues :
- fichier Figma identifié ;
- pages mobile/desktop ;
- design system minimal ;
- profil Stream Deck visuel ;
- lien Figma documenté dans un child GO futur.

Interdits :
- aucun token dans Git ;
- aucune automatisation ;
- aucune écriture runtime ;
- aucune validation de trade.

## Phase 2 — Code Connect

Déclencheur : composants LocalCMS réels et stables.

Objectif : relier les composants Figma aux composants code LocalCMS.

Préconditions :
- LocalCMS skeleton stable ;
- composants nommés ;
- design system minimal validé ;
- chemins de composants réels dans le repo ;
- aucune ambiguïté Desk Pro vs LocalCMS.

Cibles potentielles :
- StatusBadge ;
- HealthTile ;
- MachineCard ;
- WorkerRow ;
- GoCard ;
- PipelineStep ;
- ConnectorStatusRow.

Règle : Code Connect documente et améliore le handoff. Il ne remplace pas review Git, tests ou PR.

## Phase 3 — MCP Figma

Déclencheur : Code Connect stabilisé et politique sécurité validée.

Objectif : permettre à un agent IDE de lire le contexte Figma pour produire des patch drafts.

Préconditions :
- MCP officiel ou outil audité ;
- droits bornés ;
- scope read-only par défaut ;
- aucune clé en repo ;
- pas de MCP tiers non audité ;
- aucun write automatique vers production.

Modes autorisés :
- lire layout/components/tokens ;
- générer un patch draft ;
- proposer un diff ;
- produire une checklist.

Modes interdits :
- pousser Git ;
- modifier runtime ;
- créer trade ;
- modifier secrets ;
- agir hors repo opt-trading sans GO explicite.

## Gate de promotion

| Phase | Condition d'entrée | Sortie | Promotion possible |
| --- | --- | --- | --- |
| 1 | plan doc validé | wireframes | vers composants LocalCMS |
| 2 | composants LocalCMS stables | mapping Figma/code | vers MCP read-only |
| 3 | sécurité validée | patch drafts | jamais vers auto-prod sans nouveau GO |

## Verdict

Code Connect et MCP Figma sont utiles, mais uniquement après la phase design et après stabilisation LocalCMS. Toute activation immédiate est prématurée.
