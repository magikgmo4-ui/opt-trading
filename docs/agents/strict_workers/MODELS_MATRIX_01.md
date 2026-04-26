---
doc_id: STRICT_WORKERS_MODELS_MATRIX_01
doc_type: agent_model_matrix
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
status: draft_canonical
lifecycle_stage: opening
topic_keys:
  - strict_workers
  - auto_workers
  - opencode_zen
  - model_matrix
  - worker_team
surface: docs/agents
source_kind: canonical
reference_canonique_principale: docs/agents/strict_workers/MODELS_MATRIX_01.md
point_de_reprise: "Qualifier chaque modèle par test read-only puis patch-draft"
updated_at: 2026-04-26
links:
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - scripts/ai/workers/tasks.index.json
---

# MODELS_MATRIX_01 — Strict workers OpenCode Zen

## 1. Objet

Créer une première matrice de modèles pour une équipe de `strict_workers / auto_workers` à autonomie étroite.

Cette matrice ne donne pas une autorité finale aux modèles. Elle sert à choisir quel worker peut préparer quelle micro-tâche.

## 2. Sources retenues

### 2.1 Source utilisateur

Table fournie en session avec quotas :

| Modèle | Requêtes / 5h | Requêtes / semaine | Requêtes / mois |
| --- | ---: | ---: | ---: |
| GLM-5.1 | 880 | 2,150 | 4,300 |
| GLM-5 | 1,150 | 2,880 | 5,750 |
| Kimi K2.5 | 1,850 | 4,630 | 9,250 |
| Kimi K2.6 | 1,150 | 2,880 | 5,750 |
| MiMo-V2-Pro | 1,290 | 3,225 | 6,450 |
| MiMo-V2-Omni | 2,150 | 5,450 | 10,900 |
| MiMo-V2.5-Pro | 1,290 | 3,225 | 6,450 |
| MiMo-V2.5 | 2,150 | 5,450 | 10,900 |
| MiniMax M2.7 | 3,400 | 8,500 | 17,000 |
| MiniMax M2.5 | 6,300 | 15,900 | 31,800 |
| Qwen3.6 Plus | 3,300 | 8,200 | 16,300 |
| Qwen3.5 Plus | 10,200 | 25,200 | 50,500 |
| DeepSeek V4 Pro | 1,300 | 3,250 | 6,500 |
| DeepSeek V4 Flash | 7,450 | 18,600 | 37,300 |

Modèles ajoutés par liste utilisateur sans quota chiffré fourni dans l'image :

```text
Hy3 preview
Ling 2.6 Flash
MiniMax M2.5
Nemotron 3 Super
GPT-5 Nano
```

### 2.2 Source OpenCode Zen à vérifier à l'exécution

OpenCode Zen est en beta et expose une liste de modèles testés/vérifiés par OpenCode. Le format de configuration est `opencode/<model-id>`.

Le endpoint officiel à vérifier au moment d'exécution est :

```text
https://opencode.ai/zen/v1/models
```

## 3. Niveaux d'autonomie étroite

| Niveau | Nom | Description |
| --- | --- | --- |
| A0 | DISABLED | Ne pas utiliser tant que non vérifié |
| A1 | READ_ONLY | Lecture / extraction / inventaire uniquement |
| A2 | DRAFT_ONLY | Brouillon de patch, doc ou testplan sans write |
| A3 | SANDBOX_TEST | Peut proposer/lancer tests sandbox si runner autorisé |
| A4 | WRITE_GATED | Write possible seulement via runner verrouillé et validation externe |

Statut initial du chantier : aucun modèle n'est A4.

## 4. Rôles workers initiaux

| Rôle worker | Usage |
| --- | --- |
| INVENTORY_WORKER | lire et inventorier |
| DOC_DRAFT_WORKER | produire documentation brouillon |
| PATCH_DRAFT_WORKER | proposer patch minimal non appliqué |
| TESTPLAN_WORKER | lister tests et critères PASS/FAIL |
| CHERRY_PICK_WORKER | préparer inventaire cherry-pick |
| FAST_Triage_WORKER | tri rapide faible coût |
| REVIEW_DRAFT_WORKER | revue préliminaire non souveraine |
| MULTIMODAL_DRAFT_WORKER | brouillon si inputs multi-modaux, jamais secrets |

## 5. Matrice modèle -> worker

| Modèle | ID OpenCode proposé | Quota 5h | Profil conseillé | Autonomie max initiale | Tâches autorisées | Tâches interdites | Validation |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| GLM-5.1 | `opencode/glm-5.1` | 880 | raisonnement / patch draft / revue forte intermédiaire | A2 | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, REVIEW_DRAFT | secrets, write durable, push, merge | modèle fort + tests |
| GLM-5 | `opencode/glm-5` | 1,150 | worker raisonnement général / patch draft | A2 | PATCH_DRAFT, DOC_DRAFT, TESTPLAN | secrets, push, décisions finales | modèle fort + tests |
| Kimi K2.5 | `opencode/kimi-k2.5` | 1,850 | long contexte / code reading / inventaire de commits | A2 | READ_INVENTORY, PATCH_DRAFT, CHERRY_PICK_INVENTORY | secrets, write durable | revue externe |
| Kimi K2.6 | `opencode/kimi-k2.6` | 1,150 | version plus chère/forte présumée pour patch complexe | A2 | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY | secrets, push, merge | revue externe stricte |
| MiMo-V2-Pro | `opencode/mimo-v2-pro-free` ou `opencode/mimo-v2-pro` | 1,290 | pro draft / analyse bornée | A2 | DOC_DRAFT, REVIEW_DRAFT, PATCH_DRAFT léger | secrets, write durable | modèle fort |
| MiMo-V2-Omni | `opencode/mimo-v2-omni-free` ou `opencode/mimo-v2-omni` | 2,150 | omni / multimodal draft si disponible | A1 | MULTIMODAL_DRAFT, DOC_DRAFT | secrets, images sensibles, write | humain + modèle fort |
| MiMo-V2.5-Pro | `opencode/mimo-v2.5-pro` | 1,290 | pro draft à vérifier | A1 | DOC_DRAFT, REVIEW_DRAFT | secrets, write, architecture finale | test read-only d'abord |
| MiMo-V2.5 | `opencode/mimo-v2.5` | 2,150 | worker général à volume moyen | A1 | READ_INVENTORY, DOC_DRAFT | secrets, patch autonome | test read-only d'abord |
| MiniMax M2.7 | `opencode/minimax-m2.7` | 3,400 | worker coût/qualité pour patch simple et docs | A2 | READ_INVENTORY, DOC_DRAFT, PATCH_DRAFT léger, TESTPLAN | secrets, gros refactor | revue externe |
| MiniMax M2.5 | `opencode/minimax-m2.5` | 6,300 | worker volume / docs / tri / inventaire | A2 | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | secrets, patch risqué, push | revue échantillonnée + diff |
| Qwen3.6 Plus | `opencode/qwen3.6-plus` | 3,300 | bon généraliste structuré / docs / tests | A2 | DOC_DRAFT, TESTPLAN, PATCH_DRAFT léger, REVIEW_DRAFT | secrets, validation finale | modèle fort + tests |
| Qwen3.5 Plus | `opencode/qwen3.5-plus` | 10,200 | haut volume / synthèse / extraction / docs | A2 | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | secrets, patch autonome | revue par échantillon |
| DeepSeek V4 Pro | `opencode/deepseek-v4-pro` | 1,300 | code reasoning / patch draft à vérifier | A2 | PATCH_DRAFT, TESTPLAN, REVIEW_DRAFT | secrets, write durable, push | modèle fort + tests |
| DeepSeek V4 Flash | `opencode/deepseek-v4-flash` | 7,450 | tri rapide / lecture / doc de masse | A2 | FAST_TRIAGE, READ_INVENTORY, DOC_DRAFT | secrets, patch critique | revue par échantillon |
| Hy3 Preview | `A_VERIFIER` | A_COMPLETER | preview / expérimental | A0 | aucun avant vérification | tout write / secrets | vérifier ID + test read-only |
| Ling 2.6 Flash | `opencode/ling-2.6-flash-free` ou `opencode/ling-2.6-flash` | A_COMPLETER | flash / tri rapide | A1 | FAST_TRIAGE, READ_INVENTORY | secrets, patch, write | test read-only |
| Nemotron 3 Super | `opencode/nemotron-3-super-free` | A_COMPLETER | free worker / brouillon général | A1 | READ_INVENTORY, DOC_DRAFT | secrets, patch critique | revue externe |
| GPT-5 Nano | `opencode/gpt-5-nano` | A_COMPLETER | mini worker très rapide / classification / titres / tri | A1 | FAST_TRIAGE, READ_INVENTORY, formats courts | secrets, patch complexe, décision finale | revue externe |
| Big Pickle | `opencode/big-pickle` | A_COMPLETER | stealth worker pilote déjà documenté | A2 | READ_INVENTORY, PATCH_DRAFT, DOC_DRAFT, TESTPLAN | secrets, write durable, push | modèle fort + tests |

## 6. Sélection par type de tâche

### READ_INVENTORY

Priorité :

```text
Qwen3.5 Plus
MiniMax M2.5
DeepSeek V4 Flash
Kimi K2.5
Big Pickle
GPT-5 Nano
```

### PATCH_DRAFT

Priorité :

```text
GLM-5.1
Kimi K2.6
DeepSeek V4 Pro
GLM-5
Qwen3.6 Plus
MiniMax M2.7
Big Pickle
```

### DOC_DRAFT / CLOSEOUT_DRAFT

Priorité :

```text
Qwen3.5 Plus
Qwen3.6 Plus
MiniMax M2.5
DeepSeek V4 Flash
MiMo-V2.5
Big Pickle
```

### TESTPLAN

Priorité :

```text
GLM-5.1
Qwen3.6 Plus
Kimi K2.6
DeepSeek V4 Pro
GLM-5
MiniMax M2.7
```

### CHERRY_PICK_INVENTORY

Priorité :

```text
Kimi K2.5
Kimi K2.6
GLM-5.1
Qwen3.6 Plus
Big Pickle
```

### FAST_TRIAGE

Priorité :

```text
Qwen3.5 Plus
DeepSeek V4 Flash
MiniMax M2.5
GPT-5 Nano
Ling 2.6 Flash
Nemotron 3 Super
```

## 7. Modèles à vérifier avant usage

| Modèle | Raison |
| --- | --- |
| Hy3 Preview | ID exact et disponibilité non confirmés dans cette session |
| MiMo-V2.5-Pro | ID OpenCode exact à confirmer |
| MiMo-V2.5 | ID OpenCode exact à confirmer |
| DeepSeek V4 Pro | ID OpenCode exact à confirmer |
| DeepSeek V4 Flash | ID OpenCode exact à confirmer |
| Ling 2.6 Flash | confirmer suffixe `-free` ou non |
| GPT-5 Nano | confirmer si utiliser `gpt-5-nano` ou version 5.4 Nano selon workspace |

## 8. Politique de sécurité commune

Tous les workers restent soumis aux invariants :

```text
- pas de .env
- pas de tokens
- pas de clés SSH/API
- pas de secrets exchange
- pas de stratégie trading privée complète
- pas de git add/commit/push/rebase/merge autonome
- pas de migration destructive
- sortie DRAFT_ONLY tant que non validée
```

## 9. Méthode de qualification réelle

Chaque modèle doit passer trois tests avant montée en niveau :

### Test 1 — READ_ONLY

```text
Lire 3 à 5 fichiers non sensibles.
Produire ETABLI / HYPOTHESE / TODO.
Aucun write.
```

### Test 2 — PATCH_DRAFT

```text
Proposer un patch minimal théorique.
Lister fichiers touchés.
Aucun write.
```

### Test 3 — CONSOLIDATION

```text
Comparer avec modèle fort.
Vérifier git diff réel si patch appliqué par un autre agent.
Exécuter tests réels.
```

## 10. Verdict initial

```text
Équipe worker initiale recommandée :
- Qwen3.5 Plus : volume / docs / extraction
- MiniMax M2.5 : volume / inventaire / closeout draft
- DeepSeek V4 Flash : tri rapide / doc de masse
- GLM-5.1 : patch draft / review draft
- Kimi K2.5/K2.6 : long code reading / cherry-pick inventory
- Qwen3.6 Plus : testplan / doc structurée / patch léger
- Big Pickle : worker pilote expérimental
- GPT-5 Nano : tri très court / classification / titres
```

Aucun modèle n'est promu décideur final.
