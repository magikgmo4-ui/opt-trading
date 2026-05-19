---
doc_id: STRICT_WORKERS_AUTONOMIE_ETROITE_01
doc_type: agent_governance
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
status: draft_canonical
lifecycle_stage: opening
topic_keys:
  - strict_workers
  - auto_workers
  - opencode
  - openclaw
  - ai_workers
  - task_index
surface: docs/agents
source_kind: canonical
reference_canonique_principale: docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
point_de_reprise: "Construire la matrice des modèles workers"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/BRANCH_STATE.md
---

# STRICT_WORKERS_AUTONOMIE_ETROITE_01

## Objet

Définir la doctrine `strict_workers / auto_workers` pour encadrer une équipe de modèles IA spécialisés.

## Définition

```text
Strict worker = agent IA spécialisé pouvant entreprendre seul une micro-tâche bornée,
dans un couloir fermé, sans secrets, sans autonomie de décision durable,
et avec validation externe obligatoire avant effet repo durable.
```

## Architecture recommandée

```text
Prompt standard -> task index -> runner sécurisé -> rapport DRAFT_ONLY -> consolidation externe
```

## Couches

| Couche | Rôle |
| --- | --- |
| Prompts | contrat de comportement |
| Index de tâches | liste fermée des actions autorisées |
| Scripts runners | rails d'exécution reproductibles |
| Permissions | garde-fous par outil/surface |
| Consolidateur | validation modèle fort / humain / tests / git diff |

## Modes initiaux autorisés

| Mode | Description | Write durable |
| --- | --- | --- |
| READ_INVENTORY | lire et inventorier des fichiers ciblés | non |
| PATCH_DRAFT | proposer un diff théorique | non |
| DOC_DRAFT | produire une documentation brouillon | non |
| TESTPLAN | lister tests et critères PASS/FAIL | non |
| CHERRY_PICK_INVENTORY | classer commits et dépendances | non |
| CLOSEOUT_DRAFT | préparer un closeout sans verdict final | non |

## Interdits permanents

```text
.env
tokens
clés SSH/API
secrets exchange
configs prod sensibles
stratégies trading privées complètes
git add
git commit
git push
git rebase
git merge
migration destructive
rm -rf
chmod/chown global
```

## Format de sortie obligatoire

Tout strict worker doit produire au minimum :

```text
13_ESTABLISHED
14_HYPOTHESIS
15_REMAINING_GAP
16_TODO
FICHIERS_LUS
FICHIERS_TOUCHES
RISQUES
TESTS_A_EXECUTER
VERDICT_DRAFT_ONLY
```

## Règle de consolidation

Aucune sortie worker n'est validée tant que les trois conditions ne sont pas réunies :

```text
1. revue par modèle fort ou humain
2. test réel ou preuve explicite
3. git diff / état repo réel vérifié
```

## Premier worker pilote

```text
worker_id: big-pickle-worker
model: opencode/big-pickle
role: extraction / inventaire / brouillon
authority: non_souverain
status: pilote
```

## Prochaine étape

Recevoir la liste de modèles à qualifier et créer une matrice multi-worker.
