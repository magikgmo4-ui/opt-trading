---
doc_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_INFRA_RANKING_AND_USAGE

doc_type: infra_ranking_usage_matrix
repo: opt-trading
project: opt-trading
module: local-ai

go_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
status: draft
lifecycle_stage: decision_matrix
topic_keys:
  - ollama
  - infra-ranking
  - local-ai
  - student
  - admin-trading
  - db-layer
  - cursor-ai
  - usage-map
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/05_INFRA_RANKING_AND_USAGE.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/01_SYNTHESE_OLLAMA_LOCAL.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/02_MACHINE_QUALIFICATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/03_SECURITY_BASELINE.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/04_INTEGRATION_MAP.md
  - https://docs.ollama.com/api
  - https://docs.ollama.com/openai
  - https://docs.ollama.com/capabilities/structured-outputs
  - https://docs.ollama.com/capabilities/tool-calling
  - https://docs.ollama.com/capabilities/embeddings
  - https://docs.ollama.com/capabilities/vision
  - https://docs.ollama.com/context-length
  - https://docs.ollama.com/gpu
---

# 05_INFRA_RANKING_AND_USAGE

## 1_MASTER_TARGET

Classer les possibilités Ollama selon les infrastructures disponibles et traduire ce classement en usages concrets pour `opt-trading`.

Ce document sert à décider :

- quelle machine doit porter Ollama ;
- quels usages démarrer ;
- quels usages garder en laboratoire ;
- quels usages interdire ou repousser ;
- quels sous-GO ouvrir ensuite.

## 3_INITIAL_NEED

Demande utilisateur :

> Observe toutes les possibilités selon les infras et fait un classement ensuite dans ce classement élabore mon utilisation possible.

## 4_MASTER_PROJECT_PLAN

Méthode de classement :

1. partir des rôles réels des machines ;
2. distinguer calcul local, orchestration, stockage, trading runtime et interface opérateur ;
3. scorer chaque usage Ollama selon valeur, risque, complexité et dépendance matériel ;
4. produire un ordre de déploiement ;
5. transformer l'ordre en usages possibles pour l'utilisateur.

## 7_CANONICAL_STATE

Machines prises en compte :

| Machine | Rôle connu | Lecture initiale |
|---|---|---|
| `student` | Debian 12 / lab possible / upgrade RAM envisagé | meilleure cible laboratoire local IA |
| `admin-trading` | serveur trading `/opt/trading`, systemd, services sensibles | ne pas charger avec IA lourde par défaut |
| `db-layer` | MSI Ubuntu / backend data / OpenClaw exploré | bonne cible backend RAG/agents si ressources OK |
| `cursor-ai` | Windows IDE / GUI / dev | bonne cible client, orchestration et tests IDE |

État : aucune mesure machine réelle n'a encore été exécutée dans ce parent. Les verdicts ci-dessous sont donc un classement de cadrage, à confirmer par `02_MACHINE_QUALIFICATION_PLAN.md`.

## 8_VALIDATED_PLAN

Le classement est construit avec 5 critères :

| Critère | Sens |
|---|---|
| `VALUE` | valeur directe pour le workflow |
| `RISK` | risque sécurité/runtime/trading |
| `COMPLEXITY` | difficulté d'intégration |
| `HARDWARE_DEPENDENCY` | dépendance RAM/VRAM/GPU |
| `MATURITY` | maturité d'usage dans le chantier |

Échelle :

- `HIGH` = fort ;
- `MEDIUM` = moyen ;
- `LOW` = faible.

## 11_KEY_DECISIONS

- Ne pas commencer par trading vision ni Telegram.
- Commencer par qualification machine, scripts Python, puis RAG documentaire.
- Garder `admin-trading` comme machine protégée.
- Utiliser `student` comme laboratoire IA local si ressources suffisantes.
- Utiliser `db-layer` comme candidat backend RAG/agent si qualification positive.
- Utiliser `cursor-ai` comme surface opérateur/IDE, pas forcément comme serveur permanent.

## 12_INVARIANTS

- Aucune exposition publique d'Ollama.
- Pas de serveur Ollama lourd sur `admin-trading` sans preuve d'absence d'impact.
- Pas de trading live déclenché par modèle local.
- Pas d'agent shell libre.
- Pas de RAG sans hiérarchie documentaire et citations locales.
- Pas de vision trading sans validation humaine.
- Le benchmark réel prime sur cette matrice.

## 13_ESTABLISHED — Contraintes Ollama utiles au classement

- API locale par défaut autour de `localhost:11434`.
- Compatibilité partielle OpenAI utile pour brancher des clients existants.
- Structured outputs utiles pour JSON, extraction, vision structurée et pipelines.
- Tool calling possible, mais à traiter comme surface risquée si reliée à des outils système.
- Embeddings utiles pour RAG et recherche documentaire.
- Vision possible selon modèle, mais fiabilité variable pour graphes/prix/textes fins.
- Le contexte augmente fortement la mémoire requise.
- La VRAM est déterminante pour agents, long contexte, gros modèles et vitesse.

## 20_CLASSEMENT_INFRA_GLOBAL

### Rang 1 — `student` comme laboratoire IA local

Verdict : `BEST_LAB_FIRST`.

Pourquoi :

- machine moins critique que `admin-trading` ;
- Linux/Debian adapté aux tests ;
- bon endroit pour apprendre, casser, benchmarker ;
- upgrade RAM possible ;
- cible naturelle pour modèles légers/moyens, embeddings et vision lab.

Usages recommandés :

1. installation Ollama locale ;
2. test modèles légers ;
3. test embeddings/RAG ;
4. test structured outputs ;
5. test vision lab ;
6. benchmark DeepSeek/Qwen/Gemma/Llama selon ressources.

Interdits au départ :

- exposition publique ;
- serveur partagé LAN sans firewall ;
- agent shell libre ;
- trading live.

### Rang 2 — `db-layer` comme backend RAG/agent contrôlé

Verdict : `BEST_BACKEND_CANDIDATE`.

Pourquoi :

- rôle backend/data cohérent ;
- OpenClaw déjà exploré ;
- peut devenir surface RAG/vector DB ;
- bonne séparation possible entre données, agents et clients.

Usages recommandés :

1. embeddings + vector store ;
2. RAG documentaire opt-trading ;
3. provider Ollama pour clients internes ;
4. OpenClaw local avec outils limités ;
5. traitements batch de logs/docs.

Conditions :

- qualification CPU/RAM/GPU ;
- sécurité LAN stricte ;
- logs ;
- reverse proxy si accès distant ;
- pas de droits shell larges.

### Rang 3 — `cursor-ai` comme poste opérateur/dev et client Ollama

Verdict : `BEST_OPERATOR_CLIENT`.

Pourquoi :

- surface naturelle IDE/GUI ;
- bonne pour tester OpenCode, scripts, notebooks ;
- peut consommer Ollama local ou distant ;
- utile pour comparer cloud/local rapidement.

Usages recommandés :

1. client OpenAI-compatible vers Ollama ;
2. tests OpenCode/Codex provider ;
3. scripts Python Windows ;
4. interface Open WebUI ;
5. revue humaine de sorties RAG/vision.

Limites :

- serveur permanent moins idéal si machine éteinte ;
- GPU Windows à mesurer ;
- éviter agents qui modifient repo sans diff/revue.

### Rang 4 — `admin-trading` comme client léger seulement

Verdict : `PROTECT_RUNTIME`.

Pourquoi :

- machine critique trading ;
- services systemd existants ;
- risque de contention CPU/RAM/disque ;
- mauvais candidat pour expérimentation lourde.

Usages acceptables :

1. client vers Ollama hébergé ailleurs ;
2. appels très limités hors horaires critiques ;
3. analyse de logs copiés vers autre machine ;
4. intégration read-only si besoin futur.

Interdits par défaut :

- gros modèle ;
- vision lourde ;
- RAG complet ;
- agent shell ;
- serveur LAN exposé ;
- usage pendant services trading sensibles.

## 21_CLASSEMENT_USAGES_GLOBAL

### P0 — Qualification machine

Verdict : `FIRST_REQUIRED_STEP`.

Pourquoi : impossible de décider modèles/infra sans RAM/VRAM/CPU/disque réels.

Sous-GO : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_MACHINE_QUALIFICATION_01`.

### P0 — Scripts Python contrôlés

Verdict : `BEST_FIRST_USAGE`.

Pourquoi : faible risque, forte valeur, test API simple, facile à journaliser.

Usages :

- `ollama_chat.py` ;
- `ollama_json_extract.py` ;
- `ollama_log_analyze.py` ;
- `ollama_embed_doc.py` ;
- `ollama_vision_describe.py` en lab.

### P0 — RAG documentaire opt-trading

Verdict : `BEST_PRODUCT_VALUE`.

Pourquoi : ton repo dépend fortement de docs, GO, closeouts, reprises, gouvernance et mémoire projet.

Usages :

- retrouver un GO ;
- résumer un chantier ;
- comparer une règle à la matrice ;
- produire un point de reprise ;
- assister une session IDE ;
- répondre avec chemins/sources.

### P1 — OpenCode / IDE local

Verdict : `HIGH_VALUE_AFTER_BENCHMARK`.

Pourquoi : utile pour dev local, mais risque de mauvais patch si modèle faible.

Usage : assistant de suggestion, pas auto-apply.

### P1 — OpenClaw provider local

Verdict : `POWERFUL_BUT_CONTROLLED`.

Pourquoi : peut devenir orchestrateur local, mais surface risque plus grande.

Usage : après sécurité stricte seulement.

### P2 — Telegram read-only

Verdict : `USEFUL_LATER`.

Pourquoi : intégration pratique, mais entrée externe et prompt injection à gérer.

Usage : résumé/classification, pas action système.

### P2 — Trading vision lab

Verdict : `LAB_ONLY_FIRST`.

Pourquoi : valeur possible, mais risque d'erreur visuelle élevé.

Usage : pré-analyse et journal, pas signal final.

## 22_CLASSEMENT_MODELES_PAR_USAGE

### Classe A — Embeddings/RAG

Priorité : très haute.

Modèles à tester :

- `embeddinggemma` ;
- `qwen3-embedding` ;
- `all-minilm` ;
- éventuellement `nomic-embed-text` si disponible localement.

Usage : recherche documentaire locale.

### Classe B — Chat/code léger

Priorité : haute.

Modèles à tester :

- `llama3.2` ;
- `gemma3` ;
- `qwen3` ;
- modèles code disponibles selon machine.

Usage : scripts, résumé, aide au code, logs.

### Classe C — Tool calling / agents

Priorité : moyenne.

Modèles à tester seulement après sécurité :

- modèles officiellement ou empiriquement bons en tool calling ;
- commencer sans outils système dangereux.

Usage : agents contrôlés.

### Classe D — Vision

Priorité : basse au départ.

Modèles à tester :

- modèles vision compatibles Ollama ;
- test sur captures connues avec vérité terrain.

Usage : description, classification, aide au journal.

## 23_UTILISATION_POSSIBLE_PERSONNALISEE

### Utilisation 1 — Assistant local de reprise GO

Machine recommandée : `student` ou `db-layer`.

Interface : script Python ou RAG local.

Fonction :

- lire docs/chantiers ;
- retrouver le dernier `17_RESUME_POINT` ;
- produire `ETABLI / HYPOTHESE / TODO` ;
- générer un `GO_PROMPT` ;
- comparer avec `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`.

Valeur : très haute.

Risque : faible si read-only.

### Utilisation 2 — RAG gouvernance opt-trading

Machine recommandée : `db-layer` si ressources OK, sinon `student`.

Fonction :

- indexer `docs/governance`, `docs/index`, `docs/chantiers` ;
- répondre aux questions de continuité ;
- citer fichiers ;
- éviter les contradictions ;
- assister les ouvertures/fermetures de GO.

Valeur : très haute.

Risque : moyen si corpus mal filtré.

### Utilisation 3 — Analyse locale de logs

Machine recommandée : `student` ou `db-layer`.

Fonction :

- lire logs copiés depuis `admin-trading` ;
- classifier erreur ;
- proposer smoke checks ;
- résumer incident ;
- générer checklist de correction.

Valeur : haute.

Risque : faible si logs filtrés.

### Utilisation 4 — Copilote IDE local

Machine recommandée : `cursor-ai` comme client, `student/db-layer` comme serveur possible.

Fonction :

- aider dans OpenCode ou outil compatible OpenAI ;
- générer patchs proposés ;
- expliquer diffs ;
- préparer commandes ;
- ne jamais appliquer sans revue.

Valeur : moyenne/haute.

Risque : moyen.

### Utilisation 5 — Bot Telegram read-only

Machine recommandée : `db-layer` ou `student`.

Fonction :

- recevoir message/capture ;
- classifier type de demande ;
- produire résumé JSON ;
- renvoyer analyse courte ;
- journaliser.

Valeur : moyenne.

Risque : élevé si non borné.

### Utilisation 6 — Trading vision lab

Machine recommandée : `student` lab.

Fonction :

- analyser screenshot TradingView ;
- produire checklist visuelle ;
- indiquer incertitude ;
- alimenter journal de bord ;
- comparer avec analyse humaine.

Valeur : expérimentale.

Risque : élevé si utilisé comme signal.

### Utilisation 7 — Fallback offline IA

Machine recommandée : `cursor-ai` ou `student`.

Fonction :

- continuer à travailler sans cloud ;
- générer commandes ;
- résumer docs ;
- travailler sur prompts ;
- préparer plans.

Valeur : moyenne.

Risque : faible.

## 24_ARCHITECTURES_POSSIBLES

### Architecture A — Lab local simple

```text
student
  -> Ollama localhost
  -> scripts Python
  -> tests modèles
```

Verdict : meilleure première architecture.

### Architecture B — RAG backend

```text
db-layer
  -> Ollama localhost
  -> embeddings
  -> vector store
  -> API interne protégée
cursor-ai/student
  -> client RAG
```

Verdict : meilleure valeur produit après qualification.

### Architecture C — Client IDE Windows vers serveur local

```text
cursor-ai
  -> OpenCode / scripts / WebUI
    -> Ollama sur student ou db-layer
```

Verdict : utile si sécurité LAN maîtrisée.

### Architecture D — Admin-trading client seulement

```text
admin-trading
  -> script client read-only
    -> Ollama ailleurs
```

Verdict : protéger runtime trading.

### Architecture E — Telegram read-only

```text
Telegram
  -> bot allowlist
    -> API locale protégée
      -> Ollama
        -> JSON read-only
```

Verdict : plus tard, après baseline.

## 25_RANKING_FINAL

| Rang | Choix | Machine | Usage | Verdict |
|---:|---|---|---|---|
| 1 | Lab Ollama | `student` | tests modèles/API/JSON/vision | `START_HERE` |
| 2 | RAG docs | `db-layer` ou `student` | gouvernance + reprises + docs | `BEST_VALUE` |
| 3 | Scripts Python | `student` puis `cursor-ai` | clients contrôlés | `LOW_RISK_HIGH_VALUE` |
| 4 | IDE local | `cursor-ai` client | OpenCode/Codex provider | `AFTER_BENCHMARK` |
| 5 | Backend agent | `db-layer` | OpenClaw contrôlé | `SECURITY_REQUIRED` |
| 6 | Telegram read-only | `student/db-layer` | résumé/classification | `LATER` |
| 7 | Trading vision | `student` | lab journal visuel | `LAB_ONLY` |
| 8 | Admin-trading server | `admin-trading` | serveur Ollama local | `AVOID_BY_DEFAULT` |

## 26_RECOMMENDED_NEXT_SEQUENCE

Séquence concrète :

```text
1. Ouvrir GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_MACHINE_QUALIFICATION_01
2. Qualifier student en premier
3. Qualifier db-layer ensuite
4. Tester API locale et JSON strict
5. Tester embeddings sur mini corpus docs
6. Construire prototype RAG read-only
7. Tester cursor-ai comme client
8. Évaluer OpenCode/OpenClaw seulement après
9. Garder Telegram et trading vision en lab tardif
```

## 27_SELECTED_SOLUTION

Solution recommandée actuelle :

```text
student = laboratoire Ollama initial
db-layer = futur backend RAG/agent si qualification OK
cursor-ai = client opérateur/IDE
admin-trading = protégé, client léger seulement
```

## 28_SELECTED_SETUP

Setup cible P0 :

```text
student
  Ollama localhost only
  modèles légers + embeddings
  scripts Python contrôlés
  benchmark

db-layer
  pas encore actif
  candidat RAG/backend après qualification

cursor-ai
  client futur
  pas serveur obligatoire

admin-trading
  aucun serveur Ollama lourd
```

## 29_NEXT_GO

Sous-GO immédiat recommandé :

```text
GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_MACHINE_QUALIFICATION_01
```

Objectif : prouver ou invalider le classement par mesures réelles.

## 30_GO_PROMPT

```text
GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_MACHINE_QUALIFICATION_01

Objectif : qualifier les machines student, db-layer, cursor-ai et admin-trading pour décider où Ollama peut tourner.

Sources :
- docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/02_MACHINE_QUALIFICATION_PLAN.md
- docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/03_SECURITY_BASELINE.md
- docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/05_INFRA_RANKING_AND_USAGE.md

Contraintes :
- commencer par student ;
- ne pas installer sur admin-trading sans validation explicite ;
- localhost only ;
- pas de tool calling système ;
- mesurer CPU/RAM/GPU/disque/port/version/modèles ;
- produire verdict ADOPT_NOW / ADOPT_WITH_LIMITS / LAB_ONLY / REJECT_FOR_NOW.
```

## 17_RESUME_POINT

Reprise :

- fichier : `05_INFRA_RANKING_AND_USAGE.md` ;
- état : classement infra + usages produit créé ;
- prochaine action : ouvrir `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_MACHINE_QUALIFICATION_01` ;
- première machine : `student` ;
- usage P0 : scripts Python + RAG documentaire read-only ;
- invariant : `admin-trading` protégé, pas serveur Ollama lourd par défaut.
