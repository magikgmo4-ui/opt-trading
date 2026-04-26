---
doc_id: OPT_TRADING_MULTI_AGENTS_CHILD_OPENCLAW_BOUNDARY_01
doc_type: crosswalk
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CHILD_OPENCLAW_BOUNDARY_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - multi_agents
  - openclaw
  - boundary
  - orchestrator
  - operator_bridge
  - workflow_ai
  - validated_prompt_factory
search_tags:
  - surface:chantier
  - doc_role:crosswalk
  - parent:GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
  - child:GO_OPT_TRADING_MULTI_AGENTS_CHILD_OPENCLAW_BOUNDARY_01
  - family:openclaw_agents_prompt_factory
  - boundary:openclaw_runtime_vs_multi_agents_doctrine
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - workflow_ai/WORKFLOW.md
  - modules/validated_prompt_factory/README.md
  - docs/deploy_module_multi_machine_continuity.md
---

# GO_OPT_TRADING_MULTI_AGENTS_CHILD_OPENCLAW_BOUNDARY_01

## 1_MASTER_TARGET

Définir la frontière stricte entre OpenClaw runtime et la doctrine multi-agents `opt-trading`.

Ce document ne déplace pas le chantier OpenClaw runtime dans le parent multi-agents. Il crée uniquement un recroisement canonique pour que la doctrine multi-agents puisse référencer OpenClaw sans rouvrir les décisions runtime.

## 3_INITIAL_NEED

Besoin utilisateur : recroiser le nouveau chantier parent multi-agents avec OpenClaw sur branche dédiée et évaluer si OpenClaw peut être intégré comme sous-GO.

Verdict retenu : intégration partielle sous forme de sous-GO de frontière, pas absorption du parent OpenClaw.

## 4_MASTER_PROJECT_PLAN

1. Conserver le parent multi-agents comme surface doctrine.
2. Conserver le parent OpenClaw comme surface runtime, sécurité, Gateway, SSH, Telegram, tmux et bridge.
3. Créer un CHILD de recroisement sous multi-agents.
4. Définir ce qui remonte dans la doctrine multi-agents.
5. Définir ce qui reste dans le chantier OpenClaw runtime.
6. Préparer le GO suivant côté OpenClaw pour le bridge réel.

## 5_GO_PLAN

Parent : `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`

Child : `GO_OPT_TRADING_MULTI_AGENTS_CHILD_OPENCLAW_BOUNDARY_01`

Type : doc-only / crosswalk / boundary.

## 6_FINAL_TARGET

Cible du child : clarifier la place d'OpenClaw dans la matrice agents / skills / providers / orchestrateur / deployer / prompt generator sans modifier runtime.

## 7_CANONICAL_STATE

- Parent multi-agents : doctrine, frontmatter, search tags, naming, matrice agentique.
- Parent OpenClaw : runtime, sécurité, Gateway, remote access, Telegram, SSH/tmux, module `openclaw_operator_bridge`.
- OpenClaw : opérateur, interface, agent runner, Gateway expérimental contrôlé.
- `opt-trading` : orchestrateur canonique, source de vérité, validation, GO_XXXX, logs, modules, preuves repo.

## 8_VALIDATED_PLAN

Le recroisement est autorisé uniquement comme document de frontière. Toute implémentation réelle reste dans un GO enfant du parent OpenClaw.

## 9_SELECTED_SOLUTION

Mapping retenu :

| Layer | Responsable canonique |
| --- | --- |
| Interface agentique | OpenClaw |
| Gateway / channel | Parent OpenClaw runtime |
| Doctrine multi-agents | Parent multi-agents |
| Validation / gates | `workflow_ai` + GO_XXXX |
| Prompt generation | `validated_prompt_factory` |
| Déploiement multi-machine | `deploy_module_multi_machine` |
| Exécution module | modules `opt-trading` |
| Source de vérité | repo `opt-trading` |

## 10_SELECTED_SETUP

Setup conceptuel :

```text
Telegram / CLI / Android
        -> OpenClaw Gateway
        -> openclaw_operator_bridge
        -> GO_XXXX validé
        -> module opt-trading
        -> journal / preuve / closeout
```

## 11_KEY_DECISIONS

- OpenClaw ne devient pas l'orchestrateur canonique.
- OpenClaw ne décide pas seul.
- OpenClaw ne contourne pas `GO_XXXX`.
- OpenClaw ne reçoit pas de shell libre vers les machines sensibles.
- Le bridge réel reste à concevoir dans un GO dédié côté parent OpenClaw.
- Ce child sert à aligner la doctrine multi-agents, pas à modifier runtime.

## 12_INVARIANTS

- Pas de trading live automatique.
- Pas de bypass de validation humaine.
- Pas de skills non audités dans les flux sensibles.
- Pas d'exposition publique directe du Gateway.
- Pas de confusion entre provider, agent, orchestrateur, deployer et prompt generator.
- Pas de mutation runtime dans ce child.

## 13_ESTABLISHED

- Le parent multi-agents existe sur branche dédiée.
- Le parent OpenClaw orchestrator existe sur branche dédiée.
- Les deux parents ont des rôles différents.
- Le recroisement est utile, mais l'absorption serait une erreur de gouvernance.

## 14_HYPOTHESIS

- Le futur module `openclaw_operator_bridge` pourra devenir la frontière technique principale entre OpenClaw et `opt-trading`.
- La matrice multi-agents devra probablement intégrer une colonne `boundary_owner` pour distinguer doctrine et runtime.
- Le parent OpenClaw devra porter un GO enfant d'audit runtime avant toute implémentation.

## 15_REMAINING_GAP

- Contrat JSON du bridge.
- Whitelist des commandes autorisées.
- Statut réel OpenClaw sur `db-layer`.
- Auth réelle et canaux configurés.
- Journalisation des actions OpenClaw dans `opt-trading`.
- Alignement final avec `workflow_ai`.

## 16_TODO

1. Ajouter ce child dans la continuité locale du parent multi-agents.
2. Préparer le GO runtime côté OpenClaw : `GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_SPEC_01`.
3. Définir le contrat minimal `request -> validation -> execution -> proof`.
4. Définir les rôles `agent / skill / provider / orchestrator / deployer / prompt_generator` dans la matrice multi-agents.
5. Ne lancer aucun runtime avant audit `db-layer`.

## 17_RESUME_POINT

Reprise :

```text
Parent doctrine : GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
Child recroisement : GO_OPT_TRADING_MULTI_AGENTS_CHILD_OPENCLAW_BOUNDARY_01
Parent runtime parallèle : GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
Décision : OpenClaw intégré comme frontière conceptuelle dans multi-agents, runtime conservé autonome.
Next : GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_SPEC_01 côté parent OpenClaw.
```

## 18_TO_DOCUMENT

- `OPENCLAW_BOUNDARY_CROSSWALK_CHILD_01`
- `MULTI_AGENTS_OPENCLAW_ROLE_MAPPING_01`
- `OPENCLAW_OPERATOR_BRIDGE_NEXT_GO_01`

## 19_TO_REMEMBER

- OpenClaw est intégré dans la doctrine multi-agents comme frontière et opérateur.
- Le runtime OpenClaw reste dans son parent autonome.
- Le bridge technique doit être traité côté OpenClaw, pas dans le child doctrine.
