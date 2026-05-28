---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: automation_ops
go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
parent_go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
status: open
lifecycle_stage: doc_only_parent
topic_keys:
  - opt-trading
  - automation_ops
  - architecture
  - jobs
  - semi_automation
  - github_actions
  - openclaw
  - operator_handoff
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
base_branch: sot/mainline
working_branch: go/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
links:
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01/10_ARCHITECTURE_REFACTOR_SCOPE.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01/20_JOBS_REGISTRY_SPEC.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01/30_JOBS_DEDUP_PROTOCOL.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01/40_SEMIAUTO_LOOP_PROTOCOL.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01/50_OPERATOR_HANDOFF_FORMAT.md
  - docs/index/inbox/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01.md
---

# GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Créer une architecture semi-automatisée gouvernable où :

- les **jobs** sont répertoriés, testés, non doublonnés ;
- les **flux OpenClaw / GitHub Actions / IDE / ChatGPT** sont lisibles ;
- les responsabilités sont séparées ;
- les automatisations restent contrôlées par un **gate humain** ;
- les sorties sont documentées, récupérables et rejouables.

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche de référence initiale du chantier parent.

Statut :
- `doc-only`
- `audit-first`
- aucune mutation code au démarrage
- aucune suppression de job sans preuve
- aucun changement de workflow sans registre

Ce document est distinct de `GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01` (terminé, mergé, clos).

## 3_INITIAL_NEED

Axes demandés :

| Axe | Nature |
|---|---|
| Refactor architecture | structure globale, modules, flux, dépendances |
| Refactor jobs | GitHub Actions, scripts, jobs OpenClaw, runners, validations |
| Refactor semi-automatisation | boucle opérateur ↔ agent ↔ IDE ↔ repo ↔ PR |

## 4_MASTER_PROJECT_PLAN

### Axe A — Architecture

Cartographier sans mutation :
- produits finaux et modules qui les servent ;
- surfaces OpenClaw (gateway, config, tmux_operator) ;
- jobs GitHub Actions et leurs triggers ;
- scripts opérateurs et leurs consommateurs ;
- entrées / sorties par surface ;
- dépendances croisées ;
- points de contrôle humain ;
- artefacts générés ;
- chemins de reprise.

Livrable principal : `ARCHITECTURE_AUTOMATION_MAP.md`

### Axe B — Jobs

Structurer le registre des jobs :
- job_id, path, type (GHA / shell / Python / OpenClaw) ;
- trigger (push, PR, schedule, manual, webhook) ;
- inputs / outputs ;
- permissions et secrets requis ;
- owner logique ;
- statut : active / candidate / deprecated / blocked ;
- tests associés ;
- logs et artefacts ;
- rollback.

Livrable principal : `JOBS_REGISTRY.md`

### Axe C — Semi-automatisation

Formaliser la boucle :
```
ChatGPT gouvernance
→ GO_PROMPT émis
→ IDE / OpenClaw exécution
→ Git / PR / tests
→ screenshot / export retour
→ décision humaine
→ next GO ou closeout
```

Définir :
- ce qui peut être automatique vs ce qui doit rester manuel ;
- format des instructions (GO_PROMPT) ;
- format des retours (rapport / screenshot / diff) ;
- conditions de stop, de merge, de rollback.

Livrable principal : `SEMI_AUTOMATION_LOOP_PROTOCOL.md`

## 5_GO_PLAN

Child GOs prévus :

```text
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_REGISTRY_01
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_OPERATOR_HANDOFF_FORMAT_01
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLOSE_GATE_01
```

Ces sous-GO sont candidats opératoires. Ils ne sont pas ouverts par ce document.

## 6_FINAL_TARGET

Livrer, au niveau parent :

1. une carte d'architecture automation ;
2. un registre de jobs (GHA + shell + OpenClaw) ;
3. une méthode anti-doublon jobs ;
4. un protocole de boucle semi-automatisée ;
5. un format de handoff opérateur-agent standardisé ;
6. un plan de refactor jobs par batch ;
7. un close-gate avec validations.

## 7_CANONICAL_STATE

État au démarrage :

- repo : `magikgmo4-ui/opt-trading`
- branche base : `sot/mainline` @ `0e32ee15`
- branche chantier : `go/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01`
- Code Ops parent précédent : TERMINÉ (PR #899 + PR #904 merged)
- mode : `doc-only`
- mutation code : interdite dans cette passe

NEXT_GO naturel :
```text
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01
```

## 8_VALIDATED_PLAN

Ordre canonique :

1. Architecture map (inventaire flux, pas de mutation) ;
2. Jobs registry (liste sans suppression) ;
3. Jobs dedup audit (qualification des doublons) ;
4. Semi-automation protocol (formalisation boucle) ;
5. Operator handoff format (standardisation GO_PROMPT / retour) ;
6. Batch refactor jobs (seulement après 1-5) ;
7. Close gate.

## 9_SELECTED_SOLUTION

> Architecture → Jobs Registry → Semi-Automation Protocol → Batch Refactor

Pas l'inverse. Les jobs ne se refactorisent pas sans carte.

## 11_KEY_DECISIONS

| Sujet | Décision |
|---|---|
| Rouvrir Code Ops refactor | non |
| Nouveau parent | oui |
| Premier child | architecture map |
| Jobs avant architecture | non |
| Semi-auto avant jobs registry | non |
| Suppression de jobs | interdite au départ |
| GitHub Actions | à inventorier en child |
| OpenClaw jobs | à inventorier en child |
| Handoff ChatGPT ↔ IDE | à standardiser en child |

## 12_INVARIANTS

- Ne pas supprimer de job sans preuve.
- Ne pas modifier les workflows avant registre.
- Ne pas automatiser sans stop condition.
- Ne pas bypasser le gate humain.
- Ne pas confondre job technique et finalité produit.
- Ne pas rouvrir le parent Code Ops fermé.
- Ne pas créer une boucle agentique sans format de retour vérifiable.

## 15_REMAINING_GAP

Manquent encore après ouverture parent :

- carte d'architecture automation ;
- registre des jobs rempli ;
- doublons qualifiés ;
- protocole semi-auto formalisé ;
- format de handoff standardisé ;
- plan de batch refactor.

## 16_TODO

1. Ouvrir `GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01` ;
2. Cartographier les flux sans mutation ;
3. Construire le registre des jobs ;
4. Qualifier les doublons ;
5. Formaliser la boucle semi-auto ;
6. Standardiser le handoff.

## 17_RESUME_POINT

```text
Parent ouvert en doc-only.
NEXT_GO = GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01
```
