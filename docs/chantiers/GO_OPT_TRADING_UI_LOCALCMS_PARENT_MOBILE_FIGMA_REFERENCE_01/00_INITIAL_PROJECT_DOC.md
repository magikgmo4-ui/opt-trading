---
doc_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: ui_localcms_figma
go_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01
status: open
lifecycle_stage: parent_opening
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-05-19
topic_keys:
  - opt-trading
  - localcms
  - figma
  - mobile-cockpit
  - web-cockpit
  - stream-deck
  - external-apps
  - rustdesk
  - rdp
  - mcp
  - code-connect
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/07_UI_APP_VISUALIZATION_MAP.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/08_LOCALCMS_CENTRAL_UI_GAP_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md
  - docs/index/inbox/GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01.md
---

# GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01 — 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Figer Figma comme référence design doc-only pour le cockpit mobile/web LocalCMS, le profil Stream Deck safe, les vues des apps externes Airtable / Botpress / Repo KG / ClickUp, et le support visuel RustDesk / RDP / Web cockpit.

Le parent ne connecte pas Figma au runtime. Il définit une couche de design, de wireframes et de handoff futur pour LocalCMS.

## 2_INITIAL_PROJECT_DOC

Ce fichier est le document transporteur initial du parent. Il fige le plan validé, l'état canonique, les décisions, les invariants et le point de reprise. Il reste la fiche de référence obligatoire du chantier.

## 3_INITIAL_NEED

Besoin validé par l'opérateur :
- cadrer Figma après comparaison avec la chaîne apps déjà établie ;
- intégrer le bloc mobile/cockpit/support visuel ;
- figer Figma comme référence design, non comme app pipeline ;
- prévoir explicitement : Code Connect = phase 2, MCP Figma = phase 3 ;
- créer un chantier parent complet doc-only, indépendant de la session.

## 4_MASTER_PROJECT_PLAN

Direction validée :
1. garder le repo comme source canonique ;
2. traiter Figma comme référence design LocalCMS/mobile/web ;
3. conserver la chaîne apps opérationnelle : Airtable, Botpress, Repo KG, ClickUp ;
4. intégrer Stream Deck, Unified Remote, RustDesk, RDP et Web cockpit comme surfaces d'usage/support ;
5. créer une séquence en trois phases :
   - Phase 1 : Figma design reference / wireframes / design system ;
   - Phase 2 : Code Connect seulement après composants LocalCMS réels ;
   - Phase 3 : MCP Figma seulement en read-only / patch-draft après cadrage sécurité.

## 5_GO_PLAN

Workstreams du parent :
- cadrage Figma role decision ;
- wireframe scope mobile/web LocalCMS ;
- mapping visuel apps externes ;
- profil Stream Deck safe ;
- support visuel RustDesk/RDP/Web cockpit ;
- gates Code Connect et MCP Figma ;
- sécurité et invariants ;
- séquence de child GO.

## 6_FINAL_TARGET

Livrable final de ce parent : une base documentaire prête à ouvrir des GO enfants sans ambiguïté : design Figma, composants LocalCMS, Code Connect, MCP Figma, Stream Deck profile, mobile cockpit et support visuel.

## 7_CANONICAL_STATE

État retenu :
- LocalCMS = cockpit système/gouvernance read-only ;
- Desk Pro = cockpit trading actif ;
- Figma = design tool / wireframes / dashboards reporting / différé ;
- Airtable = data/journal/backtests/signaux ;
- Botpress = workflow conversationnel opérateur ;
- Repo KG = cartographie repo-first ;
- ClickUp = suivi GO/tâches/statuts/reprises ;
- Stream Deck = panneau de commandes safe ;
- Unified Remote = télécommande mobile secondaire ;
- RustDesk/RDP = support visuel/intervention ;
- Web cockpit/LocalCMS = supervision permanente.

## 8_VALIDATED_PLAN

Plan validé : créer un parent doc-only dédié, sans runtime, sans secret, sans index global, avec dossier chantier complet et entrée inbox courte.

## 9_SELECTED_SOLUTION

Solution retenue : Figma devient une couche de référence design pour LocalCMS et les surfaces opérateur, pas une application d'orchestration.

## 10_SELECTED_SETUP

Setup documentaire :
- dossier : docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01/
- branche : go/GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01
- entrée inbox : docs/index/inbox/GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01.md
- statut : doc-only parent opening.

## 11_KEY_DECISIONS

- Figma reste utile.
- Figma ne rejoint pas la chaîne opérationnelle Airtable/Botpress/Repo KG/ClickUp.
- Figma sert à cadrer LocalCMS mobile/web, Stream Deck safe profile et les visualisations des apps externes.
- Code Connect est différé en phase 2.
- MCP Figma est différé en phase 3.
- Aucun MCP tiers sans audit.
- Aucun token Figma dans Git.

## 12_INVARIANTS

- Repo > Figma.
- Docs chantiers > commentaires Figma.
- LocalCMS reste read-only au démarrage.
- Desk Pro reste UI trading active.
- Aucune action destructive via Stream Deck.
- Aucun trade live via Figma, MCP, Stream Deck ou Botpress sans validation_gate.
- Aucun secret, token, .env ou credential dans ce chantier.
- Aucun index global modifié sans instruction explicite.

## 13_ESTABLISHED

Le rôle Figma est établi comme couche design/reference. Les apps externes gardent leur rôle fonctionnel. Le support visuel RustDesk/RDP sert à intervenir, pas à gouverner. Le Web cockpit/LocalCMS gouverne la lecture système.

## 14_HYPOTHESIS

- Les wireframes Figma permettront d'accélérer LocalCMS sans forcer une implémentation prématurée.
- Code Connect deviendra pertinent quand les composants LocalCMS seront stables.
- MCP Figma deviendra pertinent quand la sécurité et les droits seront bornés.

## 15_REMAINING_GAP

- Aucun fichier Figma canonique n'est référencé.
- Aucun design system cockpit n'est créé.
- Aucun mapping Code Connect n'existe.
- Aucun MCP Figma n'est validé.
- Les composants LocalCMS réels restent à stabiliser avant handoff.

## 16_TODO

1. Produire les fichiers du parent.
2. Définir la décision de rôle Figma.
3. Définir les vues mobile/web LocalCMS.
4. Définir les mappings apps externes.
5. Définir le profil Stream Deck safe.
6. Définir gates Code Connect/MCP.
7. Définir les invariants sécurité.
8. Proposer les child GO.

## 17_RESUME_POINT

Reprendre depuis `7_CANONICAL_STATE`, puis lire :
- `10_FIGMA_ROLE_DECISION.md`
- `20_MOBILE_WEB_COCKPIT_WIREFRAME_SCOPE.md`
- `30_EXTERNAL_APPS_VISUAL_MAPPING.md`
- `40_STREAM_DECK_AND_VISUAL_SUPPORT_SPEC.md`
- `50_CODE_CONNECT_MCP_PHASE_GATES.md`
- `60_SECURITY_INVARIANTS_AND_NEXT_GO.md`
