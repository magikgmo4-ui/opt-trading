---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
status: closed
lifecycle_stage: closed
closed_at: 2026-05-31
topic_keys:
  - opt-trading
  - strict_workers
  - auto_workers
  - opencode
  - big_pickle
  - autonomy
  - governance
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Créer le profil strict worker et l'index des workers/modeles"
updated_at: 2026-04-26
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/BRANCH_STATE.md
  - docs/index/inbox/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01.md
---

# GO_OPT_TRADING_STRICT_WORKERS_PARENT_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Mettre en place une méthode canonique pour une équipe de petits workers IA à autonomie étroite, utilisables via OpenCode/OpenClaw/agents, sans dépendre de la mémoire de session.

Résumé stable :

```text
Strict worker = agent spécialisé qui peut entreprendre seul une micro-tâche bornée,
mais uniquement si elle est indexée, filtrée, autorisée, sans secrets,
sans write durable non validé, et avec sortie DRAFT_ONLY consolidée ensuite.
```

## 2_INITIAL_PROJECT_DOC

Ce document est le transporteur initial du chantier parent. Il fige la réponse complète et les éléments pertinents de la session sur Big Pickle / strict workers / auto workers.

Il sert de fiche de référence obligatoire au démarrage du chantier.

## 3_INITIAL_NEED

Besoin utilisateur :

- intégrer Big Pickle comme modèle IA worker ;
- éviter de lui confier des gros chantiers globaux ;
- automatiser des tâches précises en petits blocs ;
- consolider ensuite les sorties ;
- préparer ensuite une petite liste de modèles pour appliquer le même procédé ;
- ouvrir un chantier parent sur une branche dédiée ;
- documenter la session pour ne plus dépendre du chat.

## 4_MASTER_PROJECT_PLAN

Direction retenue :

```text
Prompts = contrat de comportement
Index de tâches = catalogue fermé des actions autorisées
Scripts runners = rails d'exécution reproductibles
Permissions OpenCode = garde-fous
Modèle fort + humain + Git diff + tests = validation finale
```

Le chantier doit produire une base réutilisable pour plusieurs workers, pas seulement Big Pickle.

## 5_GO_PLAN

### GO_STRICT_WORKERS_PARENT_01

Objectif : créer le cadre canonique des workers étroits.

Livrables attendus :

- documentation de méthode ;
- profils workers ;
- matrice des modèles ;
- index de tâches autorisées ;
- runner sécurisé ;
- formats de sortie obligatoires ;
- règles de consolidation.

### GO_PICKLE_AUTONOMIE_ETROITE_01

Objectif : intégrer Big Pickle comme premier worker pilote.

Tâches initiales :

- `GO_PICKLE_READ_INVENTORY_01`
- `GO_PICKLE_PATCH_DRAFT_01`
- `GO_PICKLE_DOC_DRAFT_01`
- `GO_PICKLE_TESTPLAN_01`
- `GO_PICKLE_CHERRY_PICK_INVENTORY_01`
- `GO_PICKLE_CLOSEOUT_DRAFT_01`

### GO_WORKER_TEAM_MODEL_MATRIX_01

Objectif : après réception de la liste de modèles, appliquer la même grille :

- rôle ;
- force ;
- faiblesse ;
- tâches autorisées ;
- tâches interdites ;
- permissions ;
- format de sortie ;
- niveau de validation requis.

## 6_FINAL_TARGET

Cible de phase :

Créer un socle `strict_workers / auto_workers` dans le repo, capable de décrire et encadrer une équipe de modèles IA spécialisés pour micro-tâches.

Le résultat attendu n'est pas un agent libre, mais un système de jobs bornés :

```text
task_id -> scope autorisé -> runner -> sortie DRAFT_ONLY -> consolidation externe
```

## 7_CANONICAL_STATE

État validé dans la session :

```text
Big Pickle = worker secondaire non souverain.
Big Pickle peut préparer, extraire, inventorier, proposer.
Big Pickle ne valide pas, ne pousse pas, ne manipule pas de secrets.
La consolidation se fait par modèle fort + tests + Git diff réel.
```

Concept stabilisé :

```text
Autonome étroit = l'agent peut lancer et compléter seul une micro-tâche,
mais seulement dans une liste fermée de tâches autorisées,
sur une surface limitée,
avec permissions limitées,
et sans effet durable non validé.
```

## 8_VALIDATED_PLAN

### Méthode d'utilisation sûre — Big Pickle

#### Mode 1 — lecture / extraction

Bon usage :

```text
Lis ces fichiers.
Dresse l’inventaire.
Classe en ETABLI / HYPOTHESE / TODO.
Ne modifie rien.
```

#### Mode 2 — patch proposé, non appliqué

Bon usage :

```text
Propose un patch minimal.
Liste les fichiers touchés.
Explique le diff attendu.
Ne lance aucun write.
```

#### Mode 3 — worker contrôlé

Pipeline :

```text
- Big Pickle prépare
- GPT / Claude / Codex vérifie
- humain valide
- Git diff réel tranche
```

#### Mode 4 — interdit / à éviter

```text
- .env
- secrets
- clés
- repo privé complet sans filtrage
- stratégie trading confidentielle
- push autonome
- migration destructive
```

### Architecture validée — autonomie étroite

Les trois couches sont nécessaires :

| Couche | Rôle |
| --- | --- |
| Prompts | définissent le comportement et le format attendu |
| Index de tâches | définit ce que le worker a le droit d'entreprendre |
| Scripts runners | exécutent les tâches dans un cadre reproductible |
| Permissions OpenCode | empêchent les débordements |
| Consolidateur | GPT / Claude / Codex / humain valide ensuite |

## 9_SELECTED_SOLUTION

Solution retenue :

```text
Prompt seul = insuffisant
Script seul = trop mécanique
Index seul = passif

Prompt + index + runner + permissions = bon modèle
```

Le worker devient un `worker transactionnel`, pas un copilote libre.

## 10_SELECTED_SETUP

Nom de chantier retenu :

```text
strict_workers / auto_workers
```

Nom de branche :

```text
go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
```

Premier profil logique :

```text
Nom : big-pickle-worker
Modèle : opencode/big-pickle
Rôle : worker non souverain
Permission : lecture / proposition / diff textuel
Interdits : secrets, .env, tokens, clés, push autonome, migration destructive
Sortie obligatoire : ETABLI / HYPOTHESE / TODO / FICHIERS_TOUCHES / RISQUES
```

Fichiers proposés pour la suite :

```text
docs/agents/strict_workers/
docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
docs/agents/strict_workers/models.matrix.md
.opencode/commands/pickle-inventory.md
.opencode/commands/pickle-patch-draft.md
.opencode/commands/pickle-doc-draft.md
.opencode/commands/pickle-testplan.md
scripts/ai/workers/tasks.index.json
scripts/ai/workers/run_task.sh
reports/ai/workers/.gitkeep
```

## 11_KEY_DECISIONS

```text
Big Pickle ne doit pas être utilisé comme agent généraliste.
Big Pickle doit être utilisé comme micro-worker.
Chaque tâche doit être bornée.
Chaque sortie doit être consolidée par un modèle plus fiable ou par l'humain.
Le Git diff réel reste l'arbitre.
```

Décision centrale :

```text
Un worker IA ne peut entreprendre une tâche que si la tâche existe dans l'index autorisé.
```

## 12_INVARIANTS

```text
Ne jamais donner aux strict workers :
- .env
- tokens
- clés SSH/API
- secrets exchange
- configs prod sensibles
- stratégie trading privée complète
- accès push autonome
- gros chantier transversal sans découpage
```

Invariants opérationnels :

```text
Un strict worker peut entreprendre une tâche seulement si :
- la tâche est dans l'index
- les fichiers sont autorisés
- les secrets sont exclus
- la sortie est structurée
- aucun write durable n'est permis sans validation
- la validation finale est externe
```

## 13_ESTABLISHED

Établi dans la session :

- Big Pickle est un modèle disponible via OpenCode sous `opencode/big-pickle`.
- Big Pickle est adapté aux tâches non sensibles de lecture, extraction, inventaire, brouillon.
- Big Pickle ne doit pas devenir source de vérité.
- Le modèle cible est `autonomie étroite`, pas autonomie générale.
- Le système doit être réutilisable pour plusieurs modèles.

## 14_HYPOTHESIS

À valider dans le repo / OpenCode :

- structure exacte des fichiers `.opencode/commands/` déjà utilisée dans `opt-trading` ;
- niveau de granularité optimal du runner ;
- possibilité de permissions strictes par agent selon la version OpenCode installée ;
- compatibilité OpenClaw avec le futur index de workers ;
- noms définitifs `strict_workers` vs `auto_workers`.

## 15_REMAINING_GAP

Reste à faire :

- recevoir la liste de modèles à intégrer ;
- qualifier chaque modèle ;
- créer une matrice multi-worker ;
- créer les prompts standards ;
- créer ou proposer le runner ;
- décider si write contrôlé est permis dans une phase future ;
- valider par un premier test read-only.

## 16_TODO

Prochaines actions :

1. Lire la liste de modèles fournie par l'utilisateur.
2. Pour chaque modèle, produire une fiche :
   - capacités ;
   - limites ;
   - rôle conseillé ;
   - tâches autorisées ;
   - tâches interdites ;
   - niveau d'autonomie ;
   - validation requise.
3. Consolider dans `models.matrix.md`.
4. Préparer `tasks.index.json`.
5. Préparer les commandes OpenCode.
6. Tester d'abord un job `READ_INVENTORY` sans write.

## 17_RESUME_POINT

Point de reprise opérationnel :

```text
Reprendre depuis GO_OPT_TRADING_STRICT_WORKERS_PARENT_01.
Branche dédiée : go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01.
Le chantier vise une équipe de strict workers IA.
Premier cas pilote : Big Pickle.
Prochaine entrée attendue : liste de modèles à qualifier.
```

## 18_TO_DOCUMENT

Blocs à extraire / maintenir :

```text
TAG: STRICT_WORKERS_PARENT
Bloc: 1_MASTER_TARGET
Bloc: 4_MASTER_PROJECT_PLAN
Bloc: 7_CANONICAL_STATE
Bloc: 8_VALIDATED_PLAN
Bloc: 10_SELECTED_SETUP
Bloc: 12_INVARIANTS
Bloc: 16_TODO
Bloc: 17_RESUME_POINT
```

## 19_TO_REMEMBER

Memory Brick projet candidat :

```text
Les modèles comme Big Pickle doivent être intégrés comme strict workers / auto workers à autonomie étroite : ils peuvent entreprendre seuls des micro-tâches seulement si elles sont indexées, filtrées, sans secrets, sans write durable non validé, avec sortie DRAFT_ONLY, puis consolidation par modèle fort + tests + Git diff.
```
