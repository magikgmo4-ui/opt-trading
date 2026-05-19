---
doc_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_SYNTHESE_OLLAMA_LOCAL

doc_type: chantier_synthesis
repo: opt-trading
project: opt-trading
module: local-ai

go_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
status: draft
lifecycle_stage: research_synthesis
topic_keys:
  - ollama
  - local-llm
  - local-ai
  - api
  - rag
  - vision
  - agents
  - security
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/01_SYNTHESE_OLLAMA_LOCAL.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md
  - https://docs.ollama.com/api
  - https://docs.ollama.com/openai
  - https://docs.ollama.com/capabilities/structured-outputs
  - https://docs.ollama.com/capabilities/tool-calling
  - https://docs.ollama.com/capabilities/vision
  - https://docs.ollama.com/context-length
  - https://docs.ollama.com/modelfile
  - https://docs.ollama.com/faq
---

# 01_SYNTHESE_OLLAMA_LOCAL

## 1_MASTER_TARGET

Synthèse complète et actionnable d'Ollama en local pour décider comment l'utiliser dans `opt-trading` sans confondre expérimentation, production, sécurité réseau, agents et trading.

## 2_POSITIONNEMENT

Ollama est un runtime local pour exécuter des modèles IA open-weight ou compatibles via :

- CLI `ollama` ;
- serveur HTTP local ;
- API native Ollama ;
- API partiellement compatible OpenAI ;
- SDK Python ;
- SDK JavaScript ;
- intégrations externes : Open WebUI, OpenCode, OpenClaw, scripts, bots, RAG.

Lecture correcte : Ollama n'est pas seulement une interface de chat. C'est un serveur d'inférence local qui charge des modèles, sert des requêtes, gère le téléchargement de modèles et expose des endpoints consommables par des outils.

## 3_CAPACITES_PRINCIPALES

### 3.1 Chat et génération

Capacités :

- conversation locale ;
- génération de texte ;
- résumé ;
- extraction ;
- transformation de texte ;
- aide au code ;
- analyse de logs ;
- génération de commandes ;
- réponses structurées.

Endpoints utiles :

- `/api/generate` ;
- `/api/chat` ;
- `/v1/chat/completions` via compatibilité OpenAI ;
- `/v1/responses` selon version Ollama récente.

### 3.2 API native

Fonctions API documentées :

- generate completion ;
- chat completion ;
- create model ;
- list local models ;
- show model information ;
- copy model ;
- delete model ;
- pull model ;
- push model ;
- generate embeddings ;
- list running models ;
- version ;
- image generation expérimentale.

### 3.3 Compatibilité OpenAI

Ollama expose une compatibilité partielle avec l'API OpenAI.

Exemple logique :

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama",
)

response = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "test"}],
)
```

Utilité : connecter des outils déjà conçus pour OpenAI en changeant seulement `base_url` et `model`.

Limite : compatibilité partielle. Toutes les fonctions OpenAI ne sont pas forcément supportées, et certains paramètres peuvent être ignorés ou différents.

### 3.4 Structured outputs

Ollama supporte des sorties structurées via `format` :

- `format: "json"` ;
- JSON Schema ;
- validation Pydantic/Zod côté client.

Usage recommandé dans `opt-trading` :

- extraction de signaux ;
- analyse de logs en JSON ;
- classification d'incidents ;
- analyse de screenshots en schéma strict ;
- résumés de fichiers projet avec champs normalisés.

Règle : utiliser `temperature: 0` pour les extractions déterministes.

### 3.5 Tool calling

Ollama supporte le tool calling si le modèle utilisé le supporte correctement.

Capacités :

- single tool call ;
- parallel tool calling ;
- agent loop ;
- tool calling streaming ;
- génération d'appels de fonctions avec arguments structurés.

Usage possible :

- appeler un script local ;
- lire un fichier ;
- interroger un endpoint interne ;
- déclencher une analyse ;
- appeler une fonction Python contrôlée.

Limite critique : tool calling ne doit pas être traité comme sûr par défaut. Le modèle propose l'appel ; le code hôte décide réellement quoi exécuter.

### 3.6 Vision

Ollama supporte les modèles vision capables de recevoir image + texte.

Modes :

- API REST avec images en base64 ;
- SDK Python avec chemin fichier, bytes ou base64 ;
- SDK JavaScript avec chemin image.

Usages `opt-trading` :

- pré-analyse screenshot TradingView ;
- lecture d'éléments visuels simples ;
- classification de capture ;
- extraction approximative de setup ;
- description structurée d'une image.

Limites vision :

- précision variable selon modèle ;
- mauvaise lecture possible des petits textes, prix, axes, niveaux ;
- risque d'interprétation incorrecte d'un graphique dense ;
- validation humaine requise pour toute décision trading.

### 3.7 Embeddings et RAG

Ollama supporte les modèles d'embeddings.

Usage RAG :

1. découper les documents ;
2. générer des embeddings ;
3. stocker dans une base vectorielle ;
4. retrouver les passages pertinents ;
5. injecter les passages dans un modèle chat ;
6. forcer citations et limites.

Modèles embeddings cités dans la documentation/blog Ollama :

- `mxbai-embed-large` ;
- `nomic-embed-text` ;
- `all-minilm`.

Usages `opt-trading` :

- recherche dans docs/chantiers ;
- reprise de session ;
- assistant gouvernance ;
- assistant modules ;
- indexation de logs ;
- base locale de prompts/closeouts.

### 3.8 Modèles personnalisés / Modelfile

Ollama permet de créer un modèle dérivé via `Modelfile`.

Paramètres utiles :

- `FROM` ;
- `SYSTEM` ;
- `PARAMETER num_ctx` ;
- `PARAMETER temperature` ;
- `PARAMETER seed` ;
- `PARAMETER repeat_penalty` ;
- templates et stop tokens selon usage.

Usage `opt-trading` :

- modèle spécialisé `opt-doc-reader` ;
- modèle `opt-log-analyst` ;
- modèle `opt-trading-vision-reviewer` ;
- modèle `opt-go-governance-helper`.

## 4_LIMITES_REELLES

### 4.1 Qualité modèle

Ollama ne crée pas la qualité. Il exécute un modèle donné.

La qualité dépend de :

- taille du modèle ;
- famille du modèle ;
- quantization ;
- contexte disponible ;
- instruction système ;
- données fournies ;
- capacité tool calling/vision native du modèle.

Un modèle local 7B/8B peut être utile, mais ne doit pas être assimilé à GPT/Claude haut de gamme pour raisonnement profond.

### 4.2 Performance matériel

Variables principales :

- RAM système ;
- VRAM GPU ;
- bande passante mémoire ;
- CPU ;
- GPU compatible ;
- taille modèle ;
- quantization ;
- contexte `num_ctx` ;
- concurrence de requêtes.

CPU-only : possible, mais lent pour gros modèles.

GPU : beaucoup plus fluide si le modèle et le contexte rentrent en VRAM.

### 4.3 Contexte

Le contexte est limité par modèle et mémoire.

La documentation récente indique des règles automatiques liées à la VRAM :

- moins de 24 GiB VRAM : contexte par défaut plus petit ;
- 24-48 GiB VRAM : contexte intermédiaire ;
- 48 GiB et plus : contexte très large possible.

Pour agents, recherche, coding tools et gros documents, viser un contexte élevé, mais chaque hausse augmente la mémoire requise.

### 4.4 Hallucination

Les modèles locaux hallucinent aussi.

Règles :

- ne pas demander une vérité externe sans source ;
- injecter contexte local ;
- forcer JSON Schema pour extraction ;
- valider par tests ;
- garder logs ;
- distinguer `ETABLI` / `HYPOTHESE`.

### 4.5 Sécurité

Ollama doit rester local par défaut.

Risque majeur : exposition réseau involontaire du port `11434`, surtout si bind sur `0.0.0.0` ou publication Docker/reverse proxy mal configurée.

Risque aggravé avec :

- tool calling ;
- accès fichiers ;
- agents autonomes ;
- endpoints sans authentification ;
- serveur exposé sur réseau public ;
- modèles non filtrés ;
- absence de firewall/logs.

## 5_MODELES — STRATEGIE DE CHOIX

### 5.1 Familles d'usage

| Usage | Type de modèle |
|---|---|
| Chat général | modèle instruct/chat |
| Code | modèle code/instruct performant |
| Extraction JSON | modèle stable + structured outputs |
| RAG | chat model + embedding model |
| Vision | modèle multimodal/vision |
| Agent tool calling | modèle explicitement bon en tool calling |
| Machine faible | petit modèle quantized |
| Machine GPU forte | modèle moyen/gros avec contexte plus large |

### 5.2 Modèles à tester sans figer

À tester selon disponibilité Ollama et ressources machine :

- `llama3.2` / `llama3.3` si disponible ;
- `qwen3` pour tool calling/raisonnement selon modèle ;
- `gemma3` pour vision/structured outputs selon doc ;
- `mistral` / `mixtral` selon machine ;
- `deepseek-r1` ou variantes locales pour raisonnement, avec prudence ;
- `nomic-embed-text` pour embeddings légers ;
- `mxbai-embed-large` pour embeddings plus solides.

Règle : ne pas choisir par popularité. Choisir par benchmark local réel sur tâches `opt-trading`.

## 6_USAGE_MAP_OPT_TRADING

### 6.1 Usages immédiatement crédibles

- résumé de docs/chantiers ;
- analyse de logs ;
- génération de checklist ;
- extraction JSON depuis fichiers texte ;
- aide Bash/PowerShell ;
- assistant local pour reprise de GO ;
- RAG sur documentation stable ;
- prétri de captures trading.

### 6.2 Usages expérimentaux

- agent local OpenClaw ;
- analyse TradingView via screenshots ;
- bot Telegram local avec images ;
- copilote IDE offline ;
- génération de patchs contrôlés ;
- assistant multi-machine.

### 6.3 Usages à éviter au démarrage

- décision de trading autonome ;
- autotrading ;
- exposition publique ;
- agent shell sans allowlist ;
- modification repo automatique sans revue ;
- analyse financière sans données vérifiées.

## 7_API_MINIMALE

### 7.1 Commandes CLI

```bash
ollama --version
ollama list
ollama pull llama3.2
ollama run llama3.2
ollama ps
ollama show llama3.2
```

### 7.2 Chat API

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [
    {"role": "user", "content": "Réponds en une phrase."}
  ],
  "stream": false
}'
```

### 7.3 JSON strict

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{"role":"user","content":"Retourne un statut JSON."}],
  "format": "json",
  "stream": false,
  "options": {"temperature": 0}
}'
```

### 7.4 Embeddings

```bash
ollama pull nomic-embed-text
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "texte à indexer"
}'
```

### 7.5 Vision

```bash
IMG=$(base64 < capture.jpg | tr -d '\n')
curl http://localhost:11434/api/chat -d '{
  "model": "gemma3",
  "messages": [{
    "role": "user",
    "content": "Décris cette image de façon structurée.",
    "images": ["'"$IMG"'"]
  }],
  "stream": false
}'
```

## 8_DECISION_MATRIX

| Question | Verdict si oui | Verdict si non |
|---|---|---|
| Besoin offline/local ? | Ollama pertinent | Cloud/API peut suffire |
| Données sensibles locales ? | Ollama pertinent | Cloud possible |
| Machine assez forte ? | tester modèles moyens | rester petit/RAG léger |
| Besoin raisonnement très fort ? | comparer cloud | ne pas surpromettre local |
| Besoin intégration OpenAI-like ? | API `/v1` utile | API native suffit |
| Besoin agents/outils ? | tool calling possible | chat simple suffisant |
| Besoin sécurité forte ? | localhost/firewall obligatoire | ne pas exposer |

## 9_VERDICT_INITIAL

Ollama est pertinent comme couche locale IA dans `opt-trading`, mais seulement avec séparation stricte :

- `CHAT_LOCAL` : autorisable rapidement ;
- `RAG_DOCS` : très pertinent après plan d'indexation ;
- `LOG_ANALYSIS` : très pertinent ;
- `VISION_TRADING` : expérimental avec validation humaine ;
- `AGENT_TOOL_CALLING` : puissant mais risqué ;
- `NETWORK_EXPOSURE` : interdit sans baseline sécurité ;
- `AUTOTRADING` : hors périmètre.

## 12_INVARIANTS

- Ollama local ne supprime pas le besoin de validation.
- Ollama local ne doit pas être exposé publiquement.
- Tool calling ne doit jamais donner accès libre au shell.
- Vision trading ne doit pas déclencher d'ordre.
- RAG doit citer les sources locales injectées.
- Les benchmarks réels priment sur les fiches modèles.

## 16_TODO

- Valider les machines avec `02_MACHINE_QUALIFICATION_PLAN.md`.
- Appliquer la baseline sécurité de `03_SECURITY_BASELINE.md` avant toute exposition LAN.
- Choisir un premier sous-GO : machine qualification ou RAG docs.
- Produire un mini benchmark local par modèle et par machine.

## 17_RESUME_POINT

Reprise :

- fichier : `01_SYNTHESE_OLLAMA_LOCAL.md` ;
- état : synthèse initiale complète créée ;
- prochaine action : exécuter le plan de qualification machine, sans runtime patch depuis le parent ;
- sous-GO logique : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_MACHINE_QUALIFICATION_01`.
