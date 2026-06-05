---
doc_id: STRICT_WORKERS_MODELS_MATRIX_01
doc_type: agent_model_matrix
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
status: draft_canonical
lifecycle_stage: validation
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
  - docs/agents/strict_workers/OPENCODE_ZEN_MODEL_ID_AUDIT_01.md
  - scripts/ai/workers/tasks.index.json
---

# MODELS_MATRIX_01 — Strict workers OpenCode Zen

## 1. Objet

Créer une matrice de modèles pour une équipe de `strict_workers / auto_workers` à autonomie étroite.

Cette matrice ne donne pas une autorité finale aux modèles. Elle sert à choisir quel worker peut préparer quelle micro-tâche.

## 2. Source utilisateur — quotas fournis

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

## 3. Source externe officielle

Voir audit :

```text
docs/agents/strict_workers/OPENCODE_ZEN_MODEL_ID_AUDIT_01.md
```

Règle OpenCode :

```text
opencode/<model-id>
```

## 4. Niveaux d'autonomie étroite

| Niveau | Nom | Description |
| --- | --- | --- |
| A0 | DISABLED | Ne pas utiliser tant que non vérifié |
| A1 | READ_ONLY | Lecture / extraction / inventaire uniquement |
| A2 | DRAFT_ONLY | Brouillon de patch, doc ou testplan sans write |
| A3 | SANDBOX_TEST | Peut proposer/lancer tests sandbox si runner autorisé |
| A4 | WRITE_GATED | Write possible seulement via runner verrouillé et validation externe |

Statut initial du chantier : aucun modèle n'est A4.

## 5. Statuts de vérification

| Statut | Sens |
| --- | --- |
| CONFIRMED_OFFICIAL_DOC | ID trouvé dans la doc OpenCode Zen officielle consultée |
| CONFIRMED_BY_USER_UI_ONLY | vu côté utilisateur, mais non retrouvé dans doc officielle consultée |
| A_VERIFIER_ENDPOINT | à confirmer via endpoint `/zen/v1/models` ou interface locale |
| DISABLED_UNTIL_VERIFIED | ne pas utiliser avant confirmation |

## 6. Matrice modèle -> worker

| Modèle | ID OpenCode config | Statut ID | Quota 5h | Profil conseillé | Autonomie max initiale | Tâches autorisées | Validation |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| GLM-5.1 | `opencode/glm-5.1` | CONFIRMED_OFFICIAL_DOC | 880 | raisonnement / patch draft / revue forte intermédiaire | A2 | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, REVIEW_DRAFT | modèle fort + tests |
| GLM-5 | `opencode/glm-5` | CONFIRMED_OFFICIAL_DOC | 1,150 | worker raisonnement général / patch draft | A2 | PATCH_DRAFT, DOC_DRAFT, TESTPLAN | modèle fort + tests |
| Kimi K2.5 | `opencode/kimi-k2.5` | CONFIRMED_OFFICIAL_DOC | 1,850 | long contexte / code reading / inventaire commits | A2 | READ_INVENTORY, PATCH_DRAFT, CHERRY_PICK_INVENTORY | revue externe |
| Kimi K2.6 | `opencode/kimi-k2.6` | CONFIRMED_OFFICIAL_DOC | 1,150 | patch complexe / cherry-pick inventory | A2 | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY | revue externe stricte |
| MiniMax M2.7 | `opencode/minimax-m2.7` | CONFIRMED_OFFICIAL_DOC | 3,400 | patch simple / docs / testplan | A2 | READ_INVENTORY, DOC_DRAFT, PATCH_DRAFT léger, TESTPLAN | revue externe |
| MiniMax M2.5 | `opencode/minimax-m2.5` | CONFIRMED_OFFICIAL_DOC | 6,300 | volume / inventaire / docs | A2 | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | revue échantillonnée + diff |
| MiniMax M2.5 Free | `opencode/minimax-m2.5-free` | CONFIRMED_OFFICIAL_DOC | A_COMPLETER | volume gratuit / tri non sensible | A1 | READ_INVENTORY, FAST_TRIAGE | revue externe |
| Qwen3.6 Plus | `opencode/qwen3.6-plus` | CONFIRMED_OFFICIAL_DOC | 3,300 | testplan / doc structurée / patch léger | A2 | DOC_DRAFT, TESTPLAN, PATCH_DRAFT léger, REVIEW_DRAFT | modèle fort + tests |
| Qwen3.5 Plus | `opencode/qwen3.5-plus` | CONFIRMED_OFFICIAL_DOC | 10,200 | haut volume / extraction / docs | A2 | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | revue par échantillon |
| Ling 2.6 Flash | `opencode/ling-2.6-flash` | CONFIRMED_OFFICIAL_DOC | A_COMPLETER | flash / tri rapide | A1 | FAST_TRIAGE, READ_INVENTORY | test read-only |
| Hy3 Preview Free | `opencode/hy3-preview-free` | CONFIRMED_OFFICIAL_DOC | A_COMPLETER | preview expérimental | A1 | READ_INVENTORY très limité | revue stricte |
| Nemotron 3 Super Free | `opencode/nemotron-3-super-free` | CONFIRMED_OFFICIAL_DOC | A_COMPLETER | brouillon général non sensible | A1 | READ_INVENTORY, DOC_DRAFT | revue externe |
| GPT-5 Nano | `opencode/gpt-5-nano` | CONFIRMED_OFFICIAL_DOC | A_COMPLETER | classification / tri très court | A1 | FAST_TRIAGE, READ_INVENTORY, formats courts | revue externe |
| Big Pickle | `opencode/big-pickle` | CONFIRMED_OFFICIAL_DOC | A_COMPLETER | stealth worker pilote | A2 | READ_INVENTORY, PATCH_DRAFT, DOC_DRAFT, TESTPLAN | modèle fort + tests |
| MiMo-V2-Pro | A_VERIFIER | CONFIRMED_BY_USER_UI_ONLY | 1,290 | pro draft / analyse bornée | A0 | aucun avant confirmation endpoint | test read-only après ID confirmé |
| MiMo-V2-Omni | A_VERIFIER | CONFIRMED_BY_USER_UI_ONLY | 2,150 | omni / multimodal draft | A0 | aucun avant confirmation endpoint | test read-only après ID confirmé |
| MiMo-V2.5-Pro | A_VERIFIER | CONFIRMED_BY_USER_UI_ONLY | 1,290 | pro draft à vérifier | A0 | aucun avant confirmation endpoint | test read-only après ID confirmé |
| MiMo-V2.5 | A_VERIFIER | CONFIRMED_BY_USER_UI_ONLY | 2,150 | worker général à volume moyen | A0 | aucun avant confirmation endpoint | test read-only après ID confirmé |
| DeepSeek V4 Pro | A_VERIFIER | CONFIRMED_BY_USER_UI_ONLY | 1,300 | code reasoning / patch draft à vérifier | A0 | aucun avant confirmation endpoint | test read-only après ID confirmé |
| DeepSeek V4 Flash | A_VERIFIER | CONFIRMED_BY_USER_UI_ONLY | 7,450 | tri rapide / doc masse à vérifier | A0 | aucun avant confirmation endpoint | test read-only après ID confirmé |

## 7. Sélection par type de tâche — après correction IDs

### READ_INVENTORY

```text
Qwen3.5 Plus
MiniMax M2.5
Kimi K2.5
Big Pickle
GPT-5 Nano
Ling 2.6 Flash
```

### PATCH_DRAFT

```text
GLM-5.1
Kimi K2.6
GLM-5
Qwen3.6 Plus
MiniMax M2.7
Big Pickle
```

### DOC_DRAFT / CLOSEOUT_DRAFT

```text
Qwen3.5 Plus
Qwen3.6 Plus
MiniMax M2.5
Nemotron 3 Super Free
Big Pickle
```

### TESTPLAN

```text
GLM-5.1
Qwen3.6 Plus
Kimi K2.6
GLM-5
MiniMax M2.7
```

### CHERRY_PICK_INVENTORY

```text
Kimi K2.5
Kimi K2.6
GLM-5.1
Qwen3.6 Plus
Big Pickle
```

### FAST_TRIAGE

```text
Qwen3.5 Plus
MiniMax M2.5
GPT-5 Nano
Ling 2.6 Flash
Nemotron 3 Super Free
```

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

```text
Test 1 — READ_ONLY : lire 3 à 5 fichiers non sensibles, sans write.
Test 2 — PATCH_DRAFT : proposer un patch minimal théorique, sans write.
Test 3 — CONSOLIDATION : revue modèle fort/humain + git diff + tests réels.
```

## 10. Verdict initial corrigé

```text
Équipe worker initiale recommandée :
- Qwen3.5 Plus : volume / docs / extraction
- MiniMax M2.5 : volume / inventaire / closeout draft
- GLM-5.1 : patch draft / review draft
- Kimi K2.5/K2.6 : long code reading / cherry-pick inventory
- Qwen3.6 Plus : testplan / doc structurée / patch léger
- Big Pickle : worker pilote expérimental
- GPT-5 Nano : tri très court / classification / titres
- Ling 2.6 Flash : tri rapide confirmé
- Hy3 Preview Free : expérimental strictement read-only
- Nemotron 3 Super Free : brouillon non sensible
```

Aucun modèle n'est promu décideur final.

## RISKS

- À qualifier.
